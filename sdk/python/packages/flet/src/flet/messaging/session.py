import asyncio
import copy
import dataclasses
import inspect
import logging
import traceback
import weakref
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Optional

from flet.controls.base_control import BaseControl
from flet.controls.base_page import BasePage
from flet.controls.context import _context_page, context
from flet.controls.core.window import Window
from flet.controls.dialog_control import DialogControl
from flet.controls.object_patch import ObjectPatch, Operation
from flet.controls.page import Page
from flet.controls.services.service import Service
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    InvokeMethodRequestBody,
    Message,
    MessageAction,
    PatchControlBody,
    SessionCrashedBody,
)
from flet.messaging.session_store import SessionStore
from flet.pubsub.pubsub_client import PubSubClient
from flet.utils.object_model import patch_dataclass
from flet.utils.strings import random_string

if TYPE_CHECKING:
    # Annotation-only (quoted at use site): deferred so a Session doesn't eagerly
    # pull the components/hooks subsystem (cold-start import cost).
    from flet.components.hooks.use_effect import EffectHook

logger = logging.getLogger("flet")
patch_logger = logging.getLogger("flet_object_patch")

__all__ = ["Session"]

_PAGE_ENVIRONMENT_FIELDS = frozenset(
    {
        "debug",
        "embedded",
        "multi_view",
        "platform",
        "pwa",
        "pyodide",
        "test",
        "wasm",
        "web",
    }
)
"""`Page` fields describing the client's environment, set when it first registers."""

_PAGE_REGISTRATION_FIELDS = frozenset({"window"})
"""`Page` fields a client sends only when it registers."""

_PATCHABLE_WHEN_HIDDEN = frozenset({"open"})
"""Fields a client can send for a hidden control: a dialog can be closing."""

_HIDDEN_CONTROL_EVENTS = frozenset(
    {
        "animation_end",
        "blur",
        "dismiss",
        "drag_complete",
        "enter",
        "exit",
        "hover",
        "size_change",
    }
)
"""Events a client can send for a hidden control, as they end what a control was doing
when it stopped rendering. A hidden control sends no others, as it isn't rendered."""

_READ_ONLY_INPUTS = frozenset({"change", "value"})
"""Events and fields a client doesn't send for a read-only control."""

_REJECTED_VALUES_INTERVAL = 0.1
"""Seconds between sends of the values rejected from a client, which bounds the traffic
that small frames can cause when a field holds a large value."""

_COMPONENT_CONTROL_TYPE = "C"
"""`_c` of a `Component`, which renders no widget of its own: its `visible` has no
effect on the client."""

_warned_client_fields: set[tuple[type, str]] = set()
"""Control fields already reported by `_warn_ignored_field`."""


def _warn_ignored_field(control: BaseControl, name: str) -> None:
    """
    Logs once that a client's value for a field of a control was ignored.

    A field the control's Dart code updates but `client_writable` doesn't list ends up
    here, so a third-party control gets a message on how to fix it. Only names that are
    fields of the control are reported, which bounds what a client can make the server
    log.

    Args:
        control: The control the value was sent for.
        name: The property name sent by the client.
    """
    cls = type(control)
    if name not in cls.__dataclass_fields__ or (cls, name) in _warned_client_fields:
        return
    _warned_client_fields.add((cls, name))
    logger.warning(
        "Ignored a value a client sent for %s.%s. If the control's Dart code updates "
        "this property, add it to `client_writable` in the @control decorator.",
        cls.__qualname__,
        name,
    )


def _is_hidden(control: BaseControl) -> bool:
    """
    Whether the client renders no widget for a control, because `visible` of the control
    or of an ancestor is `False`, or an ancestor is a closed dialog.

    The walk stops at the page, whose `visible` has no effect on the client.
    """
    current = control
    while current is not None and not isinstance(current, BasePage):
        if current._c != _COMPONENT_CONTROL_TYPE and (
            getattr(current, "visible", True) is False
        ):
            return True
        if (
            current is not control
            and isinstance(current, DialogControl)
            and not current.open
        ):
            return True
        current = current.parent
    return False


def _is_disabled(control: BaseControl) -> bool:
    """Whether `control` or one of its ancestors has `disabled` set to `True`."""
    while control is not None:
        if getattr(control, "disabled", False) is True:
            return True
        control = control.parent
    return False


def _rendering_blocks_input(control: BaseControl, name: str, kept: frozenset) -> bool:
    """
    Whether the state of a control rules out a client's event or value.

    Args:
        control: The target control.
        name: The event or field name sent by the client.
        kept: The names a hidden control can receive.

    Returns:
        `True` if the name can't come from a real client in the control's state: it is
            hidden, it is disabled and the control lists the name in `enabled_only`, or
            it is read-only and the name is an edit. A service and the `Window` render
            nothing of their own, so their state rules out nothing.
    """
    if isinstance(control, (Service, Window)):
        return False
    if name not in kept and _is_hidden(control):
        return True
    if name in control._enabled_only and _is_disabled(control):
        return True
    return name in _READ_ONLY_INPUTS and getattr(control, "read_only", False) is True


class Session:
    """
    Represents a server-side Flet session.

    A session owns the root :class:`~flet.Page`, tracks mounted controls, dispatches
    control events, synchronizes UI patches with the client connection, and coordinates
    deferred updates/effects.
    """

    def __init__(self, conn: Connection):
        self.__conn = conn
        self.__send_buffer: list[Message] = []
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
        self.__pending_effects: list[
            tuple[EffectHook, Callable[[], Any | Awaitable[Any]] | None]
        ] = []
        self.__effect_cleanup_tasks: set[asyncio.Task] = set()
        """Tasks awaiting `async` effect cleanups, held until they finish so they
        aren't garbage collected while pending."""
        self.__updates_task: Optional[asyncio.Task] = None
        self.__closed = False
        # Whether this session's app renders via the declarative components
        # API (page.render/render_views). Tracked per-session — not on the
        # global `context` singleton — so concurrent apps in one process
        # (e.g. an embedded FletApp) keep independent update behavior.
        self.__components_mode = False
        self.__page_registered = False
        """Whether a client has registered with this session, which sets the page's
        environment fields once."""
        self.__rejected_fields: dict[int, set[str]] = {}
        """Names of the fields to send back to the client, by control ID."""
        self.__rejected_fields_timer: Optional[asyncio.TimerHandle] = None
        """The pending send of :attr:`__rejected_fields`, if any."""

        session_id = self.__id
        weakref.finalize(
            self,
            lambda: logger.info("Session was garbage collected: %s", session_id),
        )

    @property
    def components_mode(self) -> bool:
        """
        Whether this session's app uses the declarative components API.

        Set by `Page.render`/`render_views` and read by
        :meth:`flet.context.auto_update_enabled`. Kept on the session so that
        multiple apps sharing one process do not interfere.
        """
        return self.__components_mode

    @components_mode.setter
    def components_mode(self, value: bool) -> None:
        self.__components_mode = value

    @property
    def connection(self) -> Connection:
        """
        Returns the current messaging connection for this session.

        Returns:
            Active `Connection` instance. It may be `None` after
            :meth:`disconnect` until a reconnect occurs.
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
            Weak mapping of control IDs to mounted :class:`~flet.BaseControl` instances.
        """
        return self.__index

    @property
    def page(self):
        """
        Returns the root :class:`~flet.Page` associated with this session.
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
        logger.debug("Connect session: %s", self.id)
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
        await self.__dispatch_page_event("connect")

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
        logger.debug("Disconnect session: %s", self.id)
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
        await self.__dispatch_page_event("disconnect")

    def close(self):
        """
        Closes the session and stops background scheduling work.

        This method marks the session as closed, cancels the updates scheduler,
        unsubscribes pub/sub handlers, resolves pending invoke-method calls with
        a closure error, and dispatches the page-level `close` event.
        """
        logger.debug("Closing expired session: %s", self.id)
        self.__closed = True
        self.__updates_ready.set()
        if self.__updates_task and not self.__updates_task.done():
            self.__updates_task.cancel()
        self.__pubsub_client.unsubscribe_all()
        self.__cancel_method_calls()
        asyncio.create_task(self.__dispatch_page_event("close"))

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

        Every added control is indexed before any of them runs `did_mount()`, so the
        index includes all additions in the submitted patch even if a callback raises.

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

        patch_logger.debug("\npatch removed_controls (%s):", len(removed_controls))
        for c in removed_controls:
            patch_logger.debug("   %s", c)

        if len(patch) > 1:
            self.__send_message(
                Message(
                    MessageAction.PATCH_CONTROL,
                    PatchControlBody(parent._i if parent else control._i, patch),
                )
            )

        patch_logger.debug("\npatch added_controls: (%s)", len(added_controls))
        for ac in added_controls:
            patch_logger.debug("   %s", ac)

        # Commit the entire index before lifecycle callbacks. A failed send must
        # neither unmount existing controls nor remove them from the index, and
        # a failed callback must not roll back an already-submitted service.
        for removed_control in removed_controls:
            self.__index.pop(removed_control._i, None)
        for added_control in added_controls:
            self.__index[added_control._i] = added_control

        added_ids = {added_control._i for added_control in added_controls}
        for removed_control in removed_controls:
            if removed_control._i not in added_ids:
                removed_control.will_unmount()

        removed_ids = {removed_control._i for removed_control in removed_controls}
        for added_control in added_controls:
            if added_control._i not in removed_ids:
                added_control.did_mount()

    def apply_patch(self, control_id: int, patch: dict[str, Any]):
        """
        Applies a partial property patch received from the client to a control in the
        session index.

        A client can send anything, so only the fields listed in `client_writable` of
        the control's `@control` decorator are applied, and only if a real client could
        change them in the control's current state. The rest of `patch` is ignored, and
        the client gets back the value of a listed field it wasn't allowed to change.

        Args:
            control_id: Target control ID.
            patch: Property/value mapping to apply.
        """
        if control := self.__index.get(control_id):
            self.__apply_client_patch(control, patch, control._client_writable)

    def apply_page_patch(self, patch: dict[str, Any]):
        """
        Applies the page state a client sends when it registers: the fields listed in
        `client_writable` of `Page`, and `window`.

        The fields describing the client's environment, such as `web` and `platform`,
        are applied only the first time a client registers with this session. The rest
        of `patch` is ignored.

        Args:
            patch: Property/value mapping to apply to the page.
        """
        writable = self.__page._client_writable | _PAGE_REGISTRATION_FIELDS
        if not self.__page_registered:
            self.__page_registered = True
            writable |= _PAGE_ENVIRONMENT_FIELDS
        self.__apply_client_patch(self.__page, patch, writable, warn=False)

    def __apply_client_patch(
        self,
        control: BaseControl,
        patch: Any,
        writable: frozenset[str],
        warn: bool = True,
    ) -> None:
        """
        Applies the part of a client's patch that the client is allowed to change.

        A field holding a control is patched by that control's own rules, in place. A
        value can't replace the control. A dialog only accepts being closed.

        Args:
            control: The control to patch.
            patch: Property/value mapping sent by the client.
            writable: Names of the fields the client may change.
            warn: Whether to report a field of the control that isn't in `writable`.
        """
        if not isinstance(patch, dict):
            return

        allowed = {}
        rejected = []
        for name, value in patch.items():
            if name not in writable:
                if warn:
                    _warn_ignored_field(control, name)
            elif _rendering_blocks_input(control, name, _PATCHABLE_WHEN_HIDDEN) or (
                name == "open"
                and value is not False
                and isinstance(control, DialogControl)
            ):
                logger.debug("Ignored a client's value of %s.%s", control, name)
                rejected.append(name)
            elif isinstance(nested := getattr(control, name, None), BaseControl):
                self.__apply_client_patch(
                    nested, value, nested._client_writable, warn=False
                )
            else:
                allowed[name] = value
        patch_dataclass(control, allowed)

        if rejected:
            self.__schedule_field_values(control, rejected)

    def __schedule_field_values(self, control: BaseControl, names: list[str]) -> None:
        """
        Schedules sending the current values of a control's fields to the client.

        Values rejected in quick succession are sent once, at most once per
        `_REJECTED_VALUES_INTERVAL`.

        Args:
            control: The control the fields belong to.
            names: Names of the fields to send.
        """
        self.__rejected_fields.setdefault(control._i, set()).update(names)
        if self.__rejected_fields_timer is not None:
            return
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            self.__send_rejected_fields()
        else:
            self.__rejected_fields_timer = loop.call_later(
                _REJECTED_VALUES_INTERVAL, self.__send_rejected_fields
            )

    def __send_rejected_fields(self) -> None:
        """
        Sends the current values of the scheduled fields to the client.

        The client applies a value before sending it, so the widget shows a rejected
        value until it gets this one, and a later write of the same value in Python
        wouldn't produce a patch.
        """
        self.__rejected_fields_timer = None
        rejected, self.__rejected_fields = self.__rejected_fields, {}
        for control_id, names in rejected.items():
            if control := self.__index.get(control_id):
                self.__send_field_values(control, names)

    def __send_field_values(self, control: BaseControl, names: set[str]) -> None:
        """
        Sends the current values of a control's fields to the client.

        The diff snapshots of list and dict fields take the values too, so that the next
        update doesn't apply a pending change to them a second time.

        Args:
            control: The control the fields belong to.
            names: Names of the fields to send.
        """
        operations = []
        for name in names:
            value = getattr(control, name)
            operations.append([Operation.Replace, 0, name, value])
            for snapshots in (
                getattr(control, "__prev_lists", {}),
                getattr(control, "__prev_dicts", {}),
            ):
                if name in snapshots:
                    snapshots[name] = copy.copy(value)
        self.__send_message(
            Message(
                MessageAction.PATCH_CONTROL,
                PatchControlBody(control._i, [[0], *operations]),
            )
        )

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

    def __is_mounted_control(self, control: BaseControl) -> bool:
        try:
            return control.page is self.__page
        except RuntimeError:
            return False

    def __find_live_control(
        self,
        value: Any,
        control_id: int,
        parent: Optional[BaseControl] = None,
        visited: Optional[set[int]] = None,
    ) -> Optional[BaseControl]:
        if value is None:
            return None

        if visited is None:
            visited = set()

        value_id = id(value)
        if value_id in visited:
            return None

        current_parent = parent
        if isinstance(value, BaseControl):
            visited.add(value_id)
            if parent is not None and parent is not value:
                value._parent = weakref.ref(parent)
            if value._i == control_id:
                return value
            current_parent = value
        elif dataclasses.is_dataclass(value) or isinstance(value, (list, tuple, dict)):
            visited.add(value_id)

        if dataclasses.is_dataclass(value):
            for field in dataclasses.fields(value):
                if field.metadata.get("skip", False) or field.name == "_parent":
                    continue
                found = self.__find_live_control(
                    getattr(value, field.name, None),
                    control_id,
                    current_parent,
                    visited,
                )
                if found is not None:
                    return found
        elif isinstance(value, dict):
            for item in value.values():
                found = self.__find_live_control(
                    item, control_id, current_parent, visited
                )
                if found is not None:
                    return found
        elif isinstance(value, (list, tuple)):
            for item in value:
                found = self.__find_live_control(
                    item, control_id, current_parent, visited
                )
                if found is not None:
                    return found

        return None

    def __resolve_event_control(self, control_id: int) -> Optional[BaseControl]:
        control = self.__index.get(control_id)
        if control is not None and self.__is_mounted_control(control):
            return control

        live_control = self.__find_live_control(self.__page, control_id)
        if live_control is not None:
            if control is not None and control is not live_control:
                logger.debug(
                    "Recovered stale control %s -> %s for event dispatch",
                    control,
                    live_control,
                )
            self.__index[control_id] = live_control
            return live_control

        if control is not None:
            # The control was removed from the page after the client queued
            # the event (e.g. a size_change from a widget that was just torn
            # down). There is no page to run the handler against, so drop it
            # rather than failing with "Control must be added to the page
            # first".
            logger.debug(
                "Dropping event for detached control %s (%s)", control, control_id
            )
        return None

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
        Dispatches an event received from the client to a control by ID.

        A client can send anything, so an event only Python code triggers is ignored,
        and so is an event a real client can't send in the control's current state.

        Args:
            control_id: Target control ID.
            event_name: Event name without the `on_` prefix.
            event_data: Raw event payload.
        """
        # Bind the page context to THIS session for the duration of the event.
        # Event dispatch runs in a fresh task whose context var may otherwise
        # carry another session's page (e.g. when a host app embeds a FletApp),
        # which would make context-derived state such as auto-update mode
        # resolve against the wrong session.
        _context_page.set(self.__page)

        control = self.__resolve_event_control(control_id)
        if not control:
            logger.debug("Control with ID %s not found.", control_id)
            return

        if (
            not isinstance(event_name, str)
            or event_name in control._server_events
            or _rendering_blocks_input(control, event_name, _HIDDEN_CONTROL_EVENTS)
        ):
            logger.debug("Ignored client event %s of %s", event_name, control)
            return

        await self.__trigger_event(control, event_name, event_data)

    async def __dispatch_page_event(self, event_name: str):
        """
        Dispatches a page-level event that this session originates.

        Args:
            event_name: Event name without the `on_` prefix.
        """
        _context_page.set(self.__page)
        await self.__trigger_event(self.__page, event_name, None)

    async def __trigger_event(
        self, control: BaseControl, event_name: str, event_data: Any
    ):
        """
        Runs a control's event handler and reports an error it raises to the client.

        Args:
            control: Target control.
            event_name: Event name without the `on_` prefix.
            event_data: Raw event payload.
        """
        try:
            await control._trigger_event(event_name, event_data)
        except Exception as e:
            logger.error(
                "Unhandled error in 'on_%s' handler", event_name, exc_info=True
            )
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
            Message(
                MessageAction.INVOKE_METHOD,
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

        The result goes to the waiting call (matched by `call_id`) even if
        the control has been removed from the page in the meantime - e.g. an
        embedded app replaced while its `wait_idle()` was pending. It's a
        legitimate answer to a legitimate call; raising here instead killed
        the connection's receive loop and froze the whole app. A result
        nobody is waiting for is dropped.
        """
        evt = self.__method_calls.pop(call_id, None)
        if evt is None:
            logger.debug(
                "Dropping invoke method result for call %s (control %s): "
                "nobody is waiting for it.",
                call_id,
                control_id,
            )
            return
        if control_id not in self.__index:
            logger.debug(
                "Invoke method result for call %s arrived after control %s "
                "was removed; delivering it anyway.",
                call_id,
                control_id,
            )
        self.__method_call_results[evt] = (result, error)
        evt.set()

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
        if context.auto_update_enabled() and not context.was_update_called():
            await self.__auto_update(control)
        context.reset_update_called()

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
            Message(MessageAction.SESSION_CRASHED, SessionCrashedBody(message))
        )

    def __send_message(self, message: Message):
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

    def schedule_effect(self, hook: "EffectHook", is_cleanup: bool):
        """
        Queues an effect hook setup/cleanup operation for scheduler execution.

        Args:
            hook: Effect hook to process.
            is_cleanup: `True` to run cleanup, `False` to run setup.
        """
        logger.debug("Schedule_effect(%s, %s)", hook, is_cleanup)
        if self.__conn is None and self.__expires_at is not None:
            return
        # Hold a strong reference to the hook until it runs.  A weakref would
        # get cleared when the owning component unmounts and clears
        # `_state.hooks` — dropping queued cleanup effects on the floor.
        self.__pending_effects.append((hook, None if is_cleanup else hook.setup))
        self.__updates_ready.set()

    def start_updates_scheduler(self):
        """
        Starts the deferred updates/effects scheduler task if not already running.
        """
        logger.debug("Starting updates scheduler: %s", self.id)
        if self.__updates_task and not self.__updates_task.done():
            return
        self.__updates_task = asyncio.create_task(self.__updates_scheduler())

    async def __updates_scheduler(self):
        """
        Background loop that drains queued updates and effect operations.

        The scheduler waits for work signals, updates pending controls, then executes
        pending effect hook setup/cleanup callbacks. Errors inside effect processing
        are reported to the client via :meth:`error`.
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

                for hook, setup in pending_effects:
                    if hook:
                        self.__run_effect(hook, setup)
        except asyncio.CancelledError:
            pass

    def __run_effect(
        self, hook: "EffectHook", setup: Callable[[], Any | Awaitable[Any]] | None
    ):
        """
        Runs an effect's `setup`, the setup function it was scheduled with, or its
        cleanups when `setup` is `None`. Queues it while the effect's previous
        cleanups are still finishing.

        Cleanups run only if a setup ran since the last ones, and always before the
        next setup, even when that setup was scheduled without them. A setup that
        runs after its component unmounted is cleaned up right away. A
        `CancelledError` the effect raises itself means it was cancelled, which
        isn't an error: running an effect never awaits, so it can't come from the
        scheduler being cancelled. Other errors are reported.
        """
        try:
            if hook.running_cleanup():
                hook._queued.append(setup)
                return
            hook.cancel_setup()
            if hook._active and (setup is None or hook.has_cleanup()):
                hook._active = False
                self.__run_effect_cleanups(hook, hook.take_cleanups())
                if hook.running_cleanup() and setup is not None:
                    hook._queued.append(setup)
                    return
            if setup is not None:
                hook._active = True
                if inspect.iscoroutinefunction(setup):
                    hook._setup_task = asyncio.create_task(setup())
                else:
                    res = setup()
                    hook._returned_cleanup = res if callable(res) else None
                if not hook.is_live():
                    hook.cancel_setup()
                    hook._active = False
                    self.__run_effect_cleanups(hook, hook.take_cleanups())
        except asyncio.CancelledError:
            pass
        except Exception as ex:
            self.__report_effect_error(ex)

    def __run_effect_cleanups(
        self,
        hook: "EffectHook",
        cleanups: list[Callable[[], Any | Awaitable[Any]]],
    ):
        """
        Runs an effect's cleanups in order.

        Non-`async` cleanups run right away, up to the first `async` one. That one
        and the rest are finished in a task. Until it finishes, the effect's next
        setups and cleanups wait. Then they run right away, before anything
        scheduled later, unless the session has closed or disconnected.
        """
        started = None
        for i, cleanup in enumerate(cleanups):
            if inspect.iscoroutinefunction(cleanup):
                break
            started = self.__call_effect_cleanup(cleanup)
            if started is not None:
                i += 1
                break
        else:
            return
        task = asyncio.create_task(self.__finish_effect_cleanups(cleanups[i:], started))
        hook._cleanup_task = task
        self.__effect_cleanup_tasks.add(task)

        def done(task: asyncio.Task):
            self.__effect_cleanup_tasks.discard(task)
            hook._cleanup_task = None
            queued = hook.take_queued()
            if self.__closed or (self.__conn is None and self.__expires_at is not None):
                return
            for setup in queued:
                self.__run_effect(hook, setup)

        task.add_done_callback(done)

    def __call_effect_cleanup(
        self, cleanup: Callable[[], Any | Awaitable[Any]]
    ) -> Awaitable[Any] | None:
        """
        Calls a cleanup and returns what it returned if that is awaitable.

        A cleanup that raises is reported; one that raises `CancelledError` was
        cancelled, which isn't an error.
        """
        try:
            res = cleanup()
            return res if inspect.isawaitable(res) else None
        except asyncio.CancelledError:
            return None
        except Exception as ex:
            self.__report_effect_error(ex)
            return None

    async def __finish_effect_cleanups(
        self,
        cleanups: list[Callable[[], Any | Awaitable[Any]]],
        started: Awaitable[Any] | None,
    ):
        """
        Finishes an effect's cleanups in order: awaits `started`, then calls and
        awaits each of `cleanups`.

        One that raises is reported, and one that raises or is cancelled doesn't
        keep the others from running. If this task itself is cancelled, the
        cleanups not reached are skipped. Telling that apart from a cleanup
        cancelled on its own needs `Task.cancelling()`, so on Python 3.10 they
        still run.
        """
        pending = [started] if started is not None else []
        for item in pending + cleanups:
            try:
                res = item if inspect.isawaitable(item) else item()
                if inspect.isawaitable(res):
                    await res
            except asyncio.CancelledError:
                task = asyncio.current_task()
                if task is not None and getattr(task, "cancelling", lambda: 0)():
                    raise
            except Exception as ex:
                self.__report_effect_error(ex)

    def __report_effect_error(self, ex: Exception):
        """Reports an exception raised by an effect setup or cleanup."""
        tb = "".join(traceback.format_exception(type(ex), ex, ex.__traceback__))
        self.error(f"Exception in effect: {ex}\n{tb}")
