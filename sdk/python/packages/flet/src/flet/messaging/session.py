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
    """
    Represents a server-side Flet session.

    A session owns the root [`Page`][flet.], tracks mounted controls, dispatches
    control events, synchronizes UI patches with the client connection, and coordinates
    deferred updates/effects.
    """

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
        self.__updates_task: Optional[asyncio.Task] = None
        self.__closed = False

        session_id = self.__id
        weakref.finalize(
            self, lambda: logger.info(f"Session was garbage collected: {session_id}")
        )

    @property
    def connection(self) -> Connection:
        """
        Returns the current messaging connection for this session.

        Returns:
            Active `Connection` instance. It may be `None` after
            [`disconnect()`][(c).disconnect] until a reconnect occurs.
        """
        return self.__conn

    @property
    def id(self):
        """
        Returns the unique session identifier.

        Returns:
            Randomly generated session ID string.
        """
        return self.__id

    @property
    def expires_at(self) -> Optional[datetime]:
        """
        Returns the UTC expiration timestamp for a disconnected session.

        Returns:
            Expiration time in UTC, or `None` when the session is currently connected.
        """
        return self.__expires_at

    @property
    def index(self):
        """
        Returns the live control index for this session.

        Returns:
            Weak mapping of control IDs to mounted [`BaseControl`][flet.] instances.
        """
        return self.__index

    @property
    def page(self):
        """
        Returns the root [`Page`][flet.] associated with this session.
        """
        return self.__page

    @property
    def pubsub_client(self) -> PubSubClient:
        """
        Returns the session-scoped pub/sub client.

        Returns:
            `PubSubClient` bound to this session ID.
        """
        return self.__pubsub_client

    @property
    def store(self) -> SessionStore:
        """
        Returns the key-value store associated with this session.

        Returns:
            `SessionStore` instance for session state persistence.
        """
        return self.__store

    def attach_connection(self, conn: Connection) -> None:
        """
        Attaches or re-attaches this session to an active connection.

        This method resets expiration state and flushes buffered outbound messages.

        Args:
            conn: Active connection to bind to this session.
        """
        logger.debug(f"Connect session: {self.id}")
        _context_page.set(self.__page)
        self.__conn = conn
        self.__expires_at = None
        for message in self.__send_buffer:
            self.__send_message(message)
        self.__send_buffer.clear()

    async def dispatch_connect_event(self) -> None:
        """
        Dispatches the page-level `connect` event for this session.
        """
        await self.dispatch_event(self.__page._i, "connect", None)

    async def connect(self, conn: Connection) -> None:
        """
        Attaches or re-attaches this session to an active connection and then
        dispatches the page-level `connect` event.

        Args:
            conn: Active connection to bind to this session.
        """
        self.attach_connection(conn)
        await self.dispatch_connect_event()

    async def disconnect(self, session_timeout_seconds: int) -> None:
        """
        Marks the session disconnected and schedules its expiration window.

        The current connection is disposed, `expires_at` is set to now plus
        `session_timeout_seconds`, and the page-level `disconnect` event is dispatched.

        Args:
            session_timeout_seconds: Grace period before the disconnected session is
                considered expired.
        """
        logger.debug(f"Disconnect session: {self.id}")
        self.__expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=session_timeout_seconds
        )
        self.__send_buffer.clear()
        self.__pending_updates.clear()
        self.__pending_effects.clear()
        self.__updates_ready.clear()
        if self.__conn:
            self.__conn.dispose()
            self.__conn = None
        await self.dispatch_event(self.__page._i, "disconnect", None)

    def close(self):
        """
        Closes the session and stops background scheduling work.

        This method marks the session as closed, cancels the updates scheduler,
        unsubscribes pub/sub handlers, resolves pending invoke-method calls with
        a closure error, and dispatches the page-level `close` event.
        """
        logger.debug(f"Closing expired session: {self.id}")
        self.__closed = True
        self.__updates_ready.set()
        if self.__updates_task and not self.__updates_task.done():
            self.__updates_task.cancel()
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
        """
        Computes and sends a patch for a control subtree.

        The patch is calculated from `prev_control` to `control`, sent to the client,
        and then applied to the local session index by unmounting removed controls and
        mounting added controls.

        Args:
            control: Current control state to patch from.
            prev_control: Previous control snapshot. If `None`, `control` is used.
            parent: Parent control context used by patch generation.
            path: Tree path used by patch generation.
            frozen: Whether object diff should treat controls as frozen.
        """
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
        """
        Applies a partial property patch to a control in the session index.

        Args:
            control_id: Target control ID.
            patch: Property/value mapping to apply.
        """
        if control := self.__index.get(control_id):
            patch_dataclass(control, patch)

    def apply_page_patch(self, patch: dict[str, Any]):
        """
        Applies a partial patch to the root page control.

        Args:
            patch: Property/value mapping to apply to the page.
        """
        self.apply_patch(self.__page._i, patch)

    def get_page_patch(self):
        """
        Generates a serialized patch payload for the root page.

        During patch generation, newly discovered controls are indexed and mounted.

        Returns:
            Serialized page patch payload suitable for register-client responses.
        """
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
        """
        Dispatches an event to a control by ID.

        Args:
            control_id: Target control ID.
            event_name: Event name without the `on_` prefix.
            event_data: Raw event payload.
        """
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
        """
        Invokes a client-side control method and waits for the response.

        Args:
            control_id: Target control ID.
            method_name: Method name to invoke on the client.
            args: Method arguments payload.
            timeout: Optional timeout in seconds.

        Returns:
            Result returned by the client-side method invocation.

        Raises:
            TimeoutError: If no invoke-method response is received before timeout.
            RuntimeError: If the client reports an invocation error.
        """
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
        """
        Stores and signals completion of a pending invoke-method request.

        Args:
            control_id: Control ID included in the response.
            call_id: Invoke-method call ID.
            result: Returned result payload.
            error: Optional error message returned by the client.

        Raises:
            RuntimeError: If the referenced control is not registered in the session.
        """
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
        """
        Resolves all pending invoke-method waits with a session-closed error.
        """
        for evt in list(self.__method_calls.values()):
            self.__method_call_results[evt] = (None, "Session closed")
            evt.set()

    async def after_event(self, control: BaseControl | None):
        """
        Runs post-event housekeeping operations.

        This currently performs optional auto-update behavior and unregisters
        unreferenced page services.

        Args:
            control: Control that handled the event, or `None`.
        """
        # call auto-update
        if context.auto_update_enabled():
            await self.__auto_update(control)

        # unregister unreferenced services
        self.page._services.unregister_services()

    async def __auto_update(self, control: BaseControl | None):
        """
        Performs auto-update on the nearest eligible isolated ancestor.

        Traverses parent controls until it finds an isolated control that is not
        frozen and an active connection exists, then calls `update()` on that control.

        Args:
            control: Starting control for parent traversal.
        """
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
        """
        Sends a session-crashed message to the connected client.

        Args:
            message: Error message to report.
        """
        self.__send_message(
            ClientMessage(ClientAction.SESSION_CRASHED, SessionCrashedBody(message))
        )

    def __send_message(self, message: ClientMessage):
        """
        Sends a message immediately or buffers it until reconnection.

        Args:
            message: Outbound client message.
        """
        if self.__conn:
            self.__conn.send_message(message)
        elif self.__expires_at is not None:
            # Session is disconnected and waiting for eviction/reconnect.
            # Drop incremental traffic to avoid unbounded buffering.
            return
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
        """
        Computes a serialized object patch and control mount/unmount deltas.

        Args:
            control: Current control state.
            prev_control: Previous control state.
            parent: Parent control context for diff generation.
            path: Tree path for nested patch generation.
            frozen: Whether diff generation should treat controls as frozen.

        Returns:
            Tuple of `(patch_message, added_controls, removed_controls)`.
        """
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
        """
        Queues a control for update by the background scheduler.

        Args:
            control: Control to update.
        """
        logger.debug("Schedule_update(%s)", control)
        if self.__conn is None and self.__expires_at is not None:
            return
        self.__pending_updates.add(control)
        self.__updates_ready.set()

    def schedule_effect(self, hook: EffectHook, is_cleanup: bool):
        """
        Queues an effect hook setup/cleanup operation for scheduler execution.

        Args:
            hook: Effect hook to process.
            is_cleanup: `True` to run cleanup, `False` to run setup.
        """
        logger.debug("Schedule_effect(%s, %s)", hook, is_cleanup)
        if self.__conn is None and self.__expires_at is not None:
            return
        self.__pending_effects.append((weakref.ref(hook), is_cleanup))
        self.__updates_ready.set()

    def start_updates_scheduler(self):
        """
        Starts the deferred updates/effects scheduler task if not already running.
        """
        logger.debug(f"Starting updates scheduler: {self.id}")
        if self.__updates_task and not self.__updates_task.done():
            return
        self.__updates_task = asyncio.create_task(self.__updates_scheduler())

    async def __updates_scheduler(self):
        """
        Background loop that drains queued updates and effect operations.

        The scheduler waits for work signals, updates pending controls, then executes
        pending effect hook setup/cleanup callbacks. Errors inside effect processing
        are reported to the client via [`error()`][(c).error].
        """
        try:
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
        except asyncio.CancelledError:
            pass
