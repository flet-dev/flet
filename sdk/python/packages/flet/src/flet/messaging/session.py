import asyncio
import logging
import traceback
import weakref
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
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
from flet.pubsub.pubsub_client import PubSubClient
from flet.utils.object_model import patch_dataclass
from flet.utils.strings import random_string

logger = logging.getLogger("flet")

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
        self.__pubsub_client = PubSubClient(conn.pubsubhub, self.__id)
        self.__method_calls: dict[str, asyncio.Event] = {}
        self.__method_call_results: dict[asyncio.Event, tuple[Any, Optional[str]]] = {}

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
        self.__pubsub_client.unsubscribe_all()
        self.__cancel_method_calls()
        asyncio.create_task(self.dispatch_event(self.__page._i, "close", None))

    def patch_control(self, control: BaseControl):
        patch, added_controls, removed_controls = self.__get_update_control_patch(
            control=control, prev_control=control
        )

        # print(f"\n\nremoved_controls: ({len(removed_controls)})")
        # for c in removed_controls:
        #     print(f"\n\nremoved_control: {c._c}({c._i} - {id(c)})")

        for removed_control in removed_controls:
            if not any(added._i == removed_control._i for added in added_controls):
                removed_control.will_unmount()
            self.__index.pop(removed_control._i, None)

        if len(patch) > 1:
            self.__send_message(
                ClientMessage(
                    ClientAction.PATCH_CONTROL, PatchControlBody(control._i, patch)
                )
            )

        # print(f"\n\nadded_controls: ({len(added_controls)})")
        # for ac in added_controls:
        #     print(f"\n\nadded_control: {ac._c}({ac._i} - {id(ac)})")

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
        except Exception as ex:
            tb = traceback.format_exc()
            self.error(f"Exception in 'on_{event_name}': {ex}\n{tb}")

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
            raise Exception(err)
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
            raise Exception(
                f"Error handling invoke method results. Control with ID {control_id} "
                "is not registered."
            )

    def __cancel_method_calls(self):
        for evt in list(self.__method_calls.values()):
            self.__method_call_results[evt] = (None, "Session closed")
            evt.set()

    async def auto_update(self, control: BaseControl | None):
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
        self, control: BaseControl, prev_control: Optional[BaseControl]
    ):
        # calculate patch
        patch, added_controls, removed_controls = ObjectPatch.from_diff(
            prev_control,
            control,
            control_cls=BaseControl,
        )

        # print("\n\npatch:", patch)

        return patch.to_message(), added_controls, removed_controls
