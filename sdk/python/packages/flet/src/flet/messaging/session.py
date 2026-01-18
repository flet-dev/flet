import asyncio
import inspect
import logging
import traceback
import weakref
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from flet.components.hooks.use_effect import EffectHook
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page, context
from flet.controls.object_patch import ObjectPatch
from flet.controls.page import Page
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    InvokeMethodRequestBody,
    PatchControlBody,
    SessionCrashedBody,
)
from flet.messaging.session_store import SessionStore
from flet.pubsub.pubsub_client import PubSubClient
from flet.utils.object_model import patch_dataclass
from flet.utils.strings import random_string

logger = logging.getLogger("flet")
patch_logger = logging.getLogger("flet_object_patch")

__all__ = ["Session"]


class Session:
    def __init__(self, conn: Connection):
        self.__conn = conn
        self.__send_buffer: list[ClientMessage] = []
        self.__id = random_string(16)
        self.__expires_at = None
        self.__index: weakref.WeakValueDictionary[int, BaseControl] = (
            weakref.WeakValueDictionary()
        )
        self.__page = Page(self)
        self.__index[self.__page._i] = self.__page
        self.__store: SessionStore = SessionStore()
        self.__pubsub_client = PubSubClient(conn.pubsubhub, self.__id)
        self.__method_calls: dict[str, asyncio.Event] = {}
        self.__method_call_results: dict[asyncio.Event, tuple[Any, Optional[str]]] = {}
        self.__updates_ready: asyncio.Event = asyncio.Event()
        self.__pending_updates: set[BaseControl] = set()
        self.__pending_effects: list[tuple[weakref.ref[EffectHook], bool]] = []
        self.__closed = False

        session_id = self.__id
        weakref.finalize(
            self, lambda: logger.debug(f"Session was garbage collected: {session_id}")
        )

    @property
    def connection(self) -> Connection:
        return self.__conn

    @property
    def id(self):
        return self.__id

    @property
    def expires_at(self) -> Optional[datetime]:
        return self.__expires_at

    @property
    def index(self):
        return self.__index

    @property
    def page(self):
        return self.__page

    @property
    def pubsub_client(self) -> PubSubClient:
        return self.__pubsub_client

    @property
    def store(self) -> SessionStore:
        return self.__store

    async def connect(self, conn: Connection) -> None:
        logger.debug(f"Connect session: {self.id}")
        _context_page.set(self.__page)
        self.__conn = conn
        self.__expires_at = None
        for message in self.__send_buffer:
            self.__send_message(message)
        self.__send_buffer.clear()
        await self.dispatch_event(self.__page._i, "connect", None)

    async def disconnect(self, session_timeout_seconds: int) -> None:
        logger.debug(f"Disconnect session: {self.id}")
        self.__expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=session_timeout_seconds
        )
        if self.__conn:
            self.__conn.dispose()
            self.__conn = None
        await self.dispatch_event(self.__page._i, "disconnect", None)

    def close(self):
        logger.debug(f"Closing expired session: {self.id}")
        self.__closed = True
        self.__pubsub_client.unsubscribe_all()
        self.__cancel_method_calls()
        asyncio.create_task(self.dispatch_event(self.__page._i, "close", None))

    def patch_control(
        self,
        control: BaseControl,
        prev_control: Optional[BaseControl] = None,
        parent: Any = None,
        path: Optional[list[Any]] = None,
        frozen: bool = False,
    ):
        patch, added_controls, removed_controls = self.__get_update_control_patch(
            control=control,
            prev_control=prev_control or control,
            parent=parent,
            path=path,
            frozen=frozen,
        )

        patch_logger.debug(f"\npatch removed_controls ({len(removed_controls)}):")
        for c in removed_controls:
            patch_logger.debug("   %s", c)

        for removed_control in removed_controls:
            if not any(added._i == removed_control._i for added in added_controls):
                removed_control.will_unmount()
            self.__index.pop(removed_control._i, None)

        if len(patch) > 1:
            self.__send_message(
                ClientMessage(
                    ClientAction.PATCH_CONTROL,
                    PatchControlBody(parent._i if parent else control._i, patch),
                )
            )

        patch_logger.debug(f"\npatch added_controls: ({len(added_controls)})")
        for ac in added_controls:
            patch_logger.debug("   %s", ac)

        for added_control in added_controls:
            self.__index[added_control._i] = added_control
            if not any(removed._i == added_control._i for removed in removed_controls):
                added_control.did_mount()

    def apply_patch(self, control_id: int, patch: dict[str, Any]):
        if control := self.__index.get(control_id):
            patch_dataclass(control, patch)

    def apply_page_patch(self, patch: dict[str, Any]):
        self.apply_patch(self.__page._i, patch)

    def get_page_patch(self):
        patch, added_controls, _ = self.__get_update_control_patch(
            self.__page, prev_control=None
        )

        for added_control in added_controls:
            self.__index[added_control._i] = added_control
            added_control.did_mount()

        # patch format:
        # [[<tree_index>], <operation_1>, <operation_2>, ...]
        # <operation> := [<type>, <tree_node_index>, <property|index>, <value>]
        return patch[1][3]  # [1] - 1st operation -> [3] - Page

    # optimizations:
    # - disable auto-update
    # - auto-update to skip already updated items
    # - add-only list
    # - disable mount/unmount

    async def dispatch_event(
        self,
        control_id: int,
        event_name: str,
        event_data: Any,
    ):
        control = self.__index.get(control_id)
        if not control:
            logger.debug(f"Control with ID {control_id} not found.")
            return

        try:
            await control._trigger_event(event_name, event_data)
        except Exception as e:
            logger.error(f"Unhandled error in 'on_{event_name}' handler", exc_info=True)
            self.error(f"{e}\n{traceback.format_exc()}")

    async def invoke_method(
        self,
        control_id: int,
        method_name: str,
        args: Any,
        timeout: Optional[float] = None,
    ):
        call_id = random_string(10)

        # register callback
        evt = asyncio.Event()
        self.__method_calls[call_id] = evt

        # call method
        self.__send_message(
            ClientMessage(
                ClientAction.INVOKE_METHOD,
                InvokeMethodRequestBody(
                    control_id=control_id, call_id=call_id, name=method_name, args=args
                ),
            )
        )

        try:
            await asyncio.wait_for(evt.wait(), timeout=timeout)
        except TimeoutError:
            if call_id in self.__method_calls:
                del self.__method_calls[call_id]
            raise TimeoutError(
                f"Timeout waiting for invokeMethod {method_name}({args}) call"
            ) from None

        result, err = self.__method_call_results.pop(evt)
        if err:
            raise RuntimeError(err)
        return result

    def handle_invoke_method_results(
        self, control_id: int, call_id: str, result: Any, error: Optional[str]
    ):
        if control_id in self.__index:
            evt = self.__method_calls.pop(call_id, None)
            if evt is None:
                return
            self.__method_call_results[evt] = (result, error)
            evt.set()
        else:
            raise RuntimeError(
                f"Error handling invoke method results. Control with ID {control_id} "
                "is not registered."
            )

    def __cancel_method_calls(self):
        for evt in list(self.__method_calls.values()):
            self.__method_call_results[evt] = (None, "Session closed")
            evt.set()

    async def after_event(self, control: BaseControl | None):
        # call auto-update
        if context.auto_update_enabled():
            await self.__auto_update(control)

        # unregister unreferenced services
        self.page._services.unregister_services()

    async def __auto_update(self, control: BaseControl | None):
        while control:
            if (
                control.is_isolated()
                and not hasattr(control, "_frozen")
                and self.__conn
            ):
                control.update()
                break
            control = control.parent

    def error(self, message: str):
        self.__send_message(
            ClientMessage(ClientAction.SESSION_CRASHED, SessionCrashedBody(message))
        )

    def __send_message(self, message: ClientMessage):
        if self.__conn:
            self.__conn.send_message(message)
        else:
            self.__send_buffer.append(message)

    def __get_update_control_patch(
        self,
        control: BaseControl,
        prev_control: Optional[BaseControl],
        parent: Any = None,
        path: Optional[list[Any]] = None,
        frozen: bool = False,
    ):
        # start_time = datetime.now()

        # calculate patch
        patch, added_controls, removed_controls = ObjectPatch.from_diff(
            prev_control,
            control,
            control_cls=BaseControl,
            parent=parent,
            path=path,
            frozen=frozen,
        )

        # end_time = datetime.now()
        # elapsed_time = end_time - start_time
        # print(
        #     "Time spent calculating patch: "
        #     f"{elapsed_time.total_seconds() * 1000:.3f} ms"
        # )

        # print("\n\npatch:", patch)

        return patch.to_message(), added_controls, removed_controls

    def schedule_update(self, control: BaseControl):
        logger.debug("Schedule_update(%s)", control)
        self.__pending_updates.add(control)
        self.__updates_ready.set()

    def schedule_effect(self, hook: EffectHook, is_cleanup: bool):
        logger.debug("Schedule_effect(%s, %s)", hook, is_cleanup)
        self.__pending_effects.append((weakref.ref(hook), is_cleanup))
        self.__updates_ready.set()

    def start_updates_scheduler(self):
        logger.debug(f"Starting updates scheduler: {self.id}")
        asyncio.create_task(self.__updates_scheduler())

    async def __updates_scheduler(self):
        while not self.__closed:
            await self.__updates_ready.wait()
            self.__updates_ready.clear()

            # Process pending updates
            pending_updates = list(self.__pending_updates)
            self.__pending_updates.clear()

            for control in pending_updates:
                control.update()

            # Process pending effects
            pending_effects = list(self.__pending_effects)
            self.__pending_effects.clear()

            for effect in pending_effects:
                try:
                    hook = effect[0]()
                    is_cleanup = effect[1]
                    # print(f"**** Running effect: {hook} {is_cleanup}")
                    if hook and hook.setup and not is_cleanup:
                        hook.cancel()
                        res = None
                        if inspect.iscoroutinefunction(hook.setup):
                            hook._setup_task = asyncio.create_task(hook.setup())
                        else:
                            res = hook.setup()
                        if callable(res):
                            hook.cleanup = res
                    elif hook and hook.cleanup and is_cleanup:
                        hook.cancel()
                        if inspect.iscoroutinefunction(hook.cleanup):
                            hook._cleanup_task = asyncio.create_task(hook.cleanup())
                        else:
                            hook.cleanup()
                except Exception as ex:
                    tb = traceback.format_exc()
                    self.error(f"Exception in effect: {ex}\n{tb}")
