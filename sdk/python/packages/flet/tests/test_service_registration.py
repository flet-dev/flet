"""Tests for when a `Service` registers itself with the page.

The client creates a service's Dart `FletService` and calls its `init()` as soon
as the message that adds the service arrives, using only the properties in that
message. Dart gates `control.triggerEvent()` on `on_<event> == true`, so an event
handler missing from that first message makes events fired from the Dart
`init()` (such as `data_channel_open`) disappear.
"""

import importlib
import pkgutil
import threading
from typing import Any, Optional

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page, context
from flet.controls.object_patch import Operation
from flet.controls.services.service import Service
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    MessageAction,
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


def _wire(obj: Any) -> Any:
    """Round-trip `obj` through the msgpack encoding every real transport uses.

    Encoding is not side-effect free: it records the snapshots later in-place
    diffs compare against.
    """
    packed = msgpack.packb(
        obj, default=configure_encode_object_for_msgpack(BaseControl)
    )
    return msgpack.unpackb(
        packed, ext_hook=decode_ext_from_msgpack, strict_map_key=False
    )


class _WireConnection(Connection):
    """Records messages encoded at send time, the way every real transport does.

    Set `fail_next_send` to make the next send raise that exception instead, as a
    transport that loses its connection mid-send would.
    """

    def __init__(self):
        """Start with no recorded messages and no pending send failure."""
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.messages: list[tuple[MessageAction, Any]] = []

        self.fail_next_send: Optional[BaseException] = None

    def send_message(self, message):
        """Encode `message` and record it, or raise the pending send failure."""
        if self.fail_next_send is not None:
            error, self.fail_next_send = self.fail_next_send, None
            raise error
        action, body = _wire([message.action, message.body])
        self.messages.append((MessageAction(action), body))


@pytest.fixture
def session():
    """A session whose client has registered and received the page."""
    s = Session(_WireConnection())
    _wire(s.get_page_patch())
    token = _context_page.set(s.page)
    yield s
    _context_page.reset(token)


def _sent(session: Session) -> list[tuple[MessageAction, Any]]:
    """Messages sent to the client after it received the page, in order."""
    return session.connection.messages


def _snapshots(session: Session, control: BaseControl) -> list[dict]:
    """Serialized forms of `control`, in the order the client received them."""
    found = []

    def walk(obj):
        """Collect every serialized dict of `control` nested in `obj`."""
        if isinstance(obj, dict):
            if obj.get("_i") == control._i and "_c" in obj:
                found.append(obj)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    for _, body in _sent(session):
        walk(body)
    return found


def _registered(session: Session) -> list[int]:
    """Ids of the registered service instances.

    Compared by identity: services are dataclasses, so two instances with the same
    field values - two `ft.Clipboard()`s, for example - are equal.
    """
    return [id(s) for s in session.page._services._services]


def _ids(*services: BaseControl) -> list[int]:
    """Ids of `services`, to compare against `_registered()`."""
    return [id(s) for s in services]


def _registry_add_ops(session: Session) -> list[list]:
    """Patch ops of every message that changed the service registry."""
    registry_id = session.page._services._i
    return [
        body["patch"][1:]
        for action, body in _sent(session)
        if action == MessageAction.PATCH_CONTROL and body["id"] == registry_id
    ]


def _core_services() -> list[type[Service]]:
    """Every service class defined in `flet.controls.services`, sorted by name."""
    import flet.controls.services as services_pkg

    for module in pkgutil.iter_modules(services_pkg.__path__):
        importlib.import_module(f"{services_pkg.__name__}.{module.name}")

    found: list[type[Service]] = []
    pending = [Service]
    while pending:
        for cls in pending.pop().__subclasses__():
            if cls not in found:
                found.append(cls)
                pending.append(cls)
    return sorted(
        (
            cls
            for cls in found
            if cls.__module__.startswith(f"{services_pkg.__name__}.")
        ),
        key=lambda cls: cls.__name__,
    )


@ft.control("LateFieldsService")
class LateFieldsService(ft.Service):
    """Sets fields after `super().init()`, like `RawImage` does for its handler."""

    src: str = ""
    model: Optional[str] = None
    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def init(self):
        """Set a handler and two fields after `super().init()`."""
        super().init()
        if self.on_data_channel_open is None:
            self.on_data_channel_open = self._capture_channel
        self.src = self.src.upper()
        self.model = "computed"
        self._init_done = True

    def did_mount(self):
        """Record whether `init()` had finished by the time the service mounted."""
        super().did_mount()
        self.init_done_at_mount = getattr(self, "_init_done", False)

    def _capture_channel(self, e):
        """Default `on_data_channel_open` handler; its presence is what matters."""


@ft.control("NoSuperInitService")
class NoSuperInitService(ft.Service):
    """An `init()` override that never calls `super().init()`."""

    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def init(self):
        """Set a handler without calling `super().init()`."""
        self.on_data_channel_open = self._capture_channel

    def _capture_channel(self, e):
        """Default `on_data_channel_open` handler; its presence is what matters."""


@ft.control("PostInitOverrideService")
class PostInitOverrideService(ft.Service):
    """Sets its handler after `super().__post_init__()`, where it has registered."""

    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def __post_init__(self, ref):
        """Set the handler once `Service.__post_init__()` has registered."""
        super().__post_init__(ref)
        self.on_data_channel_open = self._capture_channel

    def _capture_channel(self, e):
        """Default `on_data_channel_open` handler; its presence is what matters."""


@ft.control("LateConnectivity")
class LateConnectivity(ft.Connectivity):
    """A subclass of a built-in service that sets its handler in `init()`."""

    def init(self):
        """Subscribe to connectivity changes after `super().init()`."""
        super().init()
        self.on_change = self._changed

    def _changed(self, e):
        """`on_change` handler; its presence is what matters."""


@ft.control("CallableFieldService")
class CallableFieldService(ft.Service):
    """Keeps Python-only state in a declared field, which can't be serialized."""

    callback: Optional[Any] = None

    def init(self):
        """Store a callable in the declared `callback` field."""
        self.callback = lambda: None


@ft.control("ParentService")
class ParentService(ft.Service):
    """Creates a child service in its own `init()`."""

    label: Optional[str] = None

    def init(self):
        """Create the child service, then set a field of its own."""
        self._child = LateFieldsService(src="child")
        self.label = "parent"


@ft.control("DidMountRaisesService")
class DidMountRaisesService(ft.Service):
    """Fails in `did_mount()`, which runs after the client received the service."""

    def did_mount(self):
        """Raise after the service has been sent and mounted."""
        super().did_mount()
        raise ValueError("did_mount failed")


@ft.control("FailingMountControl")
class FailingMountControl(ft.Control):
    """Fails in `did_mount()`, which runs after the client received the control."""

    def did_mount(self):
        """Raise after the control has been sent and mounted."""
        super().did_mount()
        raise ValueError("child did_mount failed")


@ft.control("HolderService")
class HolderService(ft.Service):
    """Holds a control, so a change to it rides along with the next registration."""

    content: Optional[ft.Control] = None


@ft.control("PageInInitService")
class PageInInitService(ft.Service):
    """Reads the page in `init()`, through `ft.context.page` and `self.page`."""

    platform: Optional[str] = None

    def init(self):
        """Store the platform from `ft.context.page` and whether `self.page` worked."""
        super().init()
        self.platform = ft.context.page.platform.value
        try:
            self.page_in_init = self.page is not None
        except RuntimeError:
            self.page_in_init = False


@ft.control("OptedOutService")
class OptedOutService(ft.Service):
    """Opts out of registering itself when constructed."""

    _auto_register = False


def test_fields_set_after_super_init_are_in_the_registration_message(session):
    """Everything `init()` sets after `super().init()` is in the one add message."""
    svc = LateFieldsService(src="yolo.tflite")

    assert len(_sent(session)) == 1
    [first] = _snapshots(session, svc)
    assert first["on_data_channel_open"] is True
    assert first["src"] == "YOLO.TFLITE"
    assert first["model"] == "computed"


def test_service_is_registered_before_its_constructor_returns(session):
    """The service is registered and sent by the time its constructor returns.

    So `await svc.some_method()` right after construction targets a service the
    client has already been told about.
    """
    svc = LateFieldsService()

    assert _registered(session) == _ids(svc)
    assert svc.page is session.page
    assert _snapshots(session, svc)


def test_late_fields_are_not_sent_twice(session):
    """Fields that went out with registration aren't re-sent by later updates."""
    svc = LateFieldsService(src="yolo.tflite")

    svc.update()
    session.page.update()

    assert len(_sent(session)) == 1


def test_later_changes_are_still_sent(session):
    """A change made after construction is sent by the next `update()`."""
    svc = LateFieldsService(src="yolo.tflite")

    svc.model = "other"
    svc.update()

    assert len(_sent(session)) == 2
    action, body = _sent(session)[1]
    assert action == MessageAction.PATCH_CONTROL
    assert body == {"id": svc._i, "patch": [[0], [0, 0, "model", "other"]]}


def test_did_mount_runs_after_init_has_finished(session):
    """`did_mount()` sees the state `init()` finished setting up."""
    svc = LateFieldsService()

    assert svc.init_done_at_mount is True


def test_init_without_super_init_is_registered(session):
    """An `init()` that skips `super().init()` is still registered and sent."""
    svc = NoSuperInitService()

    assert _registered(session) == _ids(svc)
    [first] = _snapshots(session, svc)
    assert first["on_data_channel_open"] is True


def test_subclass_of_built_in_service_sends_late_handler(session):
    """A built-in service's subclass sends the handler it sets in `init()`."""
    svc = LateConnectivity()

    [first] = _snapshots(session, svc)
    assert first["_c"] == "LateConnectivity"
    assert first["on_change"] is True


def test_services_registered_in_a_row_each_carry_their_late_fields(session):
    """Consecutive registrations each send their own late fields."""
    first_svc = LateFieldsService(src="a")
    second_svc = LateFieldsService(src="b")

    assert _registered(session) == _ids(first_svc, second_svc)
    assert [_snapshots(session, s)[0]["src"] for s in (first_svc, second_svc)] == [
        "A",
        "B",
    ]


def test_fields_set_after_super_post_init_are_sent_with_the_next_update(session):
    """Fields set after `super().__post_init__()` arrive with the next update.

    `Service.__post_init__()` registers, so an override that sets fields after
    calling it is too late for the first message. The fields stay dirty and reach
    the client with the next update instead of being lost.
    """
    svc = PostInitOverrideService()

    [first] = _snapshots(session, svc)
    assert "on_data_channel_open" not in first

    svc.update()

    assert _sent(session)[-1][1] == {
        "id": svc._i,
        "patch": [[0], [0, 0, "on_data_channel_open", True]],
    }


def test_service_without_page_context_is_not_registered(session):
    """A service constructed without a current page is not registered.

    A plain thread does not inherit the app's context variables.
    """
    created = {}

    def worker():
        """Construct a service outside the app's context."""
        created["svc"] = LateFieldsService()

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    assert isinstance(created["svc"], LateFieldsService)
    assert _registered(session) == []
    assert _sent(session) == []


def test_service_registry_does_not_register_itself_with_the_current_page(session):
    """A new page's registry doesn't register into the current page's registry.

    An embedded `FletApp` builds its own Page (and registry) while the host page
    is still the current context.
    """
    embedded = Session(_WireConnection())

    assert _registered(session) == []
    assert _sent(session) == []
    assert _registered(embedded) == []


def test_registration_failure_is_raised_and_rolled_back(session):
    """A service that can't be serialized raises and isn't left registered.

    The next registration is sent as the registry's first service, not relative
    to a list containing the failed one.
    """
    with pytest.raises(RuntimeError, match="Cannot serialize method"):
        CallableFieldService()

    assert _registered(session) == []

    svc = LateFieldsService(src="next")

    assert _registered(session) == _ids(svc)
    [ops] = _registry_add_ops(session)
    assert ops[0][:4] == [0, 0, "_services", [_snapshots(session, svc)[0]]]


def test_service_constructed_before_page_is_sent_goes_out_with_the_page():
    """A service registered before the client has the page is sent with the page."""
    s = Session(_WireConnection())
    token = _context_page.set(s.page)
    try:
        svc = LateFieldsService(src="early")

        assert _registered(s) == _ids(svc)
        assert _sent(s) == []

        page_patch = _wire(s.get_page_patch())
        [snapshot] = page_patch["_services"]["_services"]
        assert snapshot["_i"] == svc._i
        assert snapshot["src"] == "EARLY"
        assert snapshot["on_data_channel_open"] is True
    finally:
        _context_page.reset(token)


def test_child_service_created_in_init_registers_before_its_parent(session):
    """A service created in another service's `init()` registers first."""
    parent = ParentService()

    assert _registered(session) == _ids(parent._child, parent)
    assert _snapshots(session, parent)[0]["label"] == "parent"
    assert _snapshots(session, parent._child)[0]["src"] == "CHILD"


@pytest.mark.parametrize("service_cls", _core_services(), ids=lambda cls: cls.__name__)
def test_every_core_service_registers_once(session, service_cls):
    """Every core service registers and is sent exactly once when constructed."""
    # Sensors only allow themselves on mobile and web.
    session.page.platform = ft.PagePlatform.ANDROID

    svc = service_cls()

    assert _registered(session) == _ids(svc)
    assert len(_snapshots(session, svc)) == 1


def test_failed_send_removes_the_failed_instance_not_an_equal_one(session):
    """Rolling back a failed send removes that instance, not an equal earlier one.

    The next registration is then sent as an add after the service the client
    already has, with nothing removed.
    """
    first = ft.Clipboard()
    session.connection.fail_next_send = RuntimeError("connection lost")

    with pytest.raises(RuntimeError, match="connection lost"):
        ft.Clipboard()

    assert _registered(session) == _ids(first)

    third = ft.Clipboard()

    assert _registered(session) == _ids(first, third)
    [_, ops] = _registry_add_ops(session)
    assert [op[0] for op in ops] == [Operation.Add.value]
    assert ops[0][2:] == [1, _snapshots(session, third)[0]]


def test_interrupted_send_is_rolled_back(session):
    """A send interrupted by a `BaseException` is rolled back too."""
    session.connection.fail_next_send = KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        LateFieldsService()

    assert _registered(session) == []
    svc = LateFieldsService()
    assert _registered(session) == _ids(svc)


def test_service_whose_did_mount_raises_stays_registered(session):
    """A failure after the client received the service keeps it registered.

    The client already has it, so Python must keep it too.
    """
    with pytest.raises(ValueError, match="did_mount failed"):
        DidMountRaisesService()

    [svc] = session.page._services._services
    assert _snapshots(session, svc)


def test_service_sent_alongside_a_failing_control_stays_registered(session):
    """A service stays registered when another control in its patch fails to mount.

    The holder's pending child goes out in the same patch as the new service, and
    its `did_mount()` raises before the new service mounts. The client already has
    both, so the next registration must be added after the new service.
    """
    holder = HolderService()
    holder.content = FailingMountControl()

    with pytest.raises(ValueError, match="child did_mount failed"):
        ft.Clipboard()

    [_, clipboard] = session.page._services._services
    assert isinstance(clipboard, ft.Clipboard)
    assert _snapshots(session, clipboard)

    launcher = ft.UrlLauncher()

    assert _registered(session) == _ids(holder, clipboard, launcher)
    ops = _registry_add_ops(session)[-1]
    assert [op[0] for op in ops] == [Operation.Add.value]
    assert ops[0][2:] == [2, _snapshots(session, launcher)[0]]


def test_unsupported_service_does_not_break_later_registrations(session):
    """A service rejected on this platform doesn't break later registrations."""
    session.page.platform = ft.PagePlatform.MACOS

    with pytest.raises(ft.FletUnsupportedPlatformException):
        ft.Accelerometer()

    clipboard = ft.Clipboard()

    assert _registered(session) == _ids(clipboard)
    assert _snapshots(session, clipboard)


def test_page_is_not_attached_in_init_but_context_page_is_available(session):
    """In `init()`, `self.page` isn't attached yet but `ft.context.page` works."""
    session.page.platform = ft.PagePlatform.ANDROID

    svc = PageInInitService()

    assert svc.page_in_init is False
    assert _snapshots(session, svc)[0]["platform"] == "android"
    assert svc.page is session.page


def test_auto_register_false_opts_out(session):
    """A service class with `_auto_register = False` doesn't register itself."""
    OptedOutService()

    assert _registered(session) == []
    assert _sent(session) == []


def test_registration_does_not_mark_update_called(session):
    """Registration is internal bookkeeping, not a user `update()` call."""
    context.reset_update_called()

    LateFieldsService()

    assert _sent(session)
    assert context.was_update_called() is False


@pytest.mark.parametrize("failure", ["serialization", "send"])
def test_failed_registration_preserves_pending_subtree_changes(session, failure):
    """Retry all pending changes when a registration patch cannot be sent."""
    old = ft.Text("old")
    label = ft.Text("before")
    column = ft.Column([label])
    holder = HolderService(content=ft.Row([old, column]))
    replacement = ft.Text("replacement")
    appended = ft.Text("appended")
    holder.content.controls[0] = replacement
    column.controls.append(appended)
    label.value = "after"
    unmounted = []
    old.will_unmount = lambda: unmounted.append(old._i)

    if failure == "send":
        session.connection.fail_next_send = RuntimeError("connection lost")
    with pytest.raises(RuntimeError):
        if failure == "serialization":
            CallableFieldService()
        else:
            ft.Clipboard()

    assert session.index[old._i] is old
    assert unmounted == []
    assert replacement.parent is None
    assert appended.parent is None

    # Capture the retry itself: it must contain all changes from the failed patch.
    session.connection.messages.clear()
    holder.update()
    assert _snapshots(session, replacement)
    assert _snapshots(session, appended)
    assert any(
        op[-2:] == ["value", "after"]
        for _, body in _sent(session)
        for op in body["patch"][1:]
    )
    assert session.index[replacement._i] is replacement
    assert session.index[appended._i] is appended
    assert old._i not in session.index
    assert unmounted == [old._i]


@pytest.mark.parametrize("failure", ["serialization", "send"])
def test_failed_registration_preserves_child_replacement(session, failure):
    """A single-child snapshot must still point to the client-side child."""
    old = ft.Text("old")
    holder = HolderService(content=old)
    replacement = ft.Text("new")
    holder.content = replacement
    if failure == "send":
        session.connection.fail_next_send = RuntimeError("connection lost")
    with pytest.raises(RuntimeError):
        if failure == "serialization":
            CallableFieldService()
        else:
            ft.Clipboard()

    assert session.index[old._i] is old
    session.connection.messages.clear()
    clipboard = ft.Clipboard()
    assert _snapshots(session, replacement)
    assert session.index[replacement._i] is replacement
    assert old._i not in session.index
    assert _registered(session) == _ids(holder, clipboard)


def test_service_sent_alongside_failing_unmount_stays_registered(session):
    """An unmount callback failure happens after committing the entire patch."""
    old = ft.Text("old")
    holder = HolderService(content=old)
    replacement = ft.Text("new")
    holder.content = replacement

    def fail_unmount():
        raise ValueError("unmount failed")

    old.will_unmount = fail_unmount
    with pytest.raises(ValueError, match="unmount failed"):
        ft.Clipboard()

    assert old._i not in session.index
    assert session.index[replacement._i] is replacement
    clipboard = session.page._services._services[-1]
    assert isinstance(clipboard, ft.Clipboard)
    assert session.index[clipboard._i] is clipboard
    launcher = ft.UrlLauncher()
    assert _registered(session) == _ids(holder, clipboard, launcher)
    ops = _registry_add_ops(session)[-1]
    assert [op[0] for op in ops] == [Operation.Add.value]
    assert ops[0][2:] == [2, _snapshots(session, launcher)[0]]


@pytest.mark.parametrize("was_called", [False, True])
def test_failed_registration_preserves_update_called_flag(session, was_called):
    """Failed internal updates must not suppress the handler's auto-update."""
    context.reset_update_called()
    if was_called:
        context.mark_update_called()
    with pytest.raises(RuntimeError, match="Cannot serialize method"):
        CallableFieldService()
    assert context.was_update_called() is was_called
