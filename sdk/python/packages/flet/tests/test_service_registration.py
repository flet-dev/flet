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
    """Records messages encoded at send time, the way every real transport does."""

    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.messages: list[tuple[MessageAction, Any]] = []

        self.fail_next_send: Optional[BaseException] = None

    def send_message(self, message):
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
    return session.connection.messages


def _snapshots(session: Session, control: BaseControl) -> list[dict]:
    """Serialized forms of `control`, in the order the client received them."""
    found = []

    def walk(obj):
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
    return [id(s) for s in services]


@ft.control("LateFieldsService")
class LateFieldsService(ft.Service):
    """Sets fields after `super().init()`, like `RawImage` does for its handler."""

    src: str = ""
    model: Optional[str] = None
    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def init(self):
        super().init()
        if self.on_data_channel_open is None:
            self.on_data_channel_open = self._capture_channel
        self.src = self.src.upper()
        self.model = "computed"
        self._init_done = True

    def did_mount(self):
        super().did_mount()
        self.init_done_at_mount = getattr(self, "_init_done", False)

    def _capture_channel(self, e):
        pass


@ft.control("NoSuperInitService")
class NoSuperInitService(ft.Service):
    """An `init()` override that never calls `super().init()`."""

    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def init(self):
        self.on_data_channel_open = self._capture_channel

    def _capture_channel(self, e):
        pass


@ft.control("PostInitOverrideService")
class PostInitOverrideService(ft.Service):
    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None

    def __post_init__(self, ref):
        super().__post_init__(ref)
        self.on_data_channel_open = self._capture_channel

    def _capture_channel(self, e):
        pass


@ft.control("LateConnectivity")
class LateConnectivity(ft.Connectivity):
    def init(self):
        super().init()
        self.on_change = self._changed

    def _changed(self, e):
        pass


def test_fields_set_after_super_init_are_in_the_registration_message(session):
    svc = LateFieldsService(src="yolo.tflite")

    assert len(_sent(session)) == 1
    [first] = _snapshots(session, svc)
    assert first["on_data_channel_open"] is True
    assert first["src"] == "YOLO.TFLITE"
    assert first["model"] == "computed"


def test_service_is_registered_before_its_constructor_returns(session):
    """
    So `await svc.some_method()` right after construction targets a service the
    client has already been told about.
    """
    svc = LateFieldsService()

    assert _registered(session) == _ids(svc)
    assert svc.page is session.page
    assert _snapshots(session, svc)


def test_late_fields_are_not_sent_twice(session):
    svc = LateFieldsService(src="yolo.tflite")

    svc.update()
    session.page.update()

    assert len(_sent(session)) == 1


def test_later_changes_are_still_sent(session):
    svc = LateFieldsService(src="yolo.tflite")

    svc.model = "other"
    svc.update()

    assert len(_sent(session)) == 2
    action, body = _sent(session)[1]
    assert action == MessageAction.PATCH_CONTROL
    assert body == {"id": svc._i, "patch": [[0], [0, 0, "model", "other"]]}


def test_did_mount_runs_after_init_has_finished(session):
    svc = LateFieldsService()

    assert svc.init_done_at_mount is True


def test_init_without_super_init_is_registered(session):
    svc = NoSuperInitService()

    assert _registered(session) == _ids(svc)
    [first] = _snapshots(session, svc)
    assert first["on_data_channel_open"] is True


def test_subclass_of_built_in_service_sends_late_handler(session):
    svc = LateConnectivity()

    [first] = _snapshots(session, svc)
    assert first["_c"] == "LateConnectivity"
    assert first["on_change"] is True


def test_services_registered_in_a_row_each_carry_their_late_fields(session):
    first_svc = LateFieldsService(src="a")
    second_svc = LateFieldsService(src="b")

    assert _registered(session) == _ids(first_svc, second_svc)
    assert [_snapshots(session, s)[0]["src"] for s in (first_svc, second_svc)] == [
        "A",
        "B",
    ]


def test_fields_set_after_super_post_init_are_sent_with_the_next_update(session):
    """
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
    """A plain thread does not inherit the app's context variables."""
    created = {}

    def worker():
        created["svc"] = LateFieldsService()

    t = threading.Thread(target=worker)
    t.start()
    t.join()

    assert isinstance(created["svc"], LateFieldsService)
    assert _registered(session) == []
    assert _sent(session) == []


def test_service_registry_does_not_register_itself_with_the_current_page(session):
    """
    An embedded `FletApp` builds its own Page (and registry) while the host page
    is still the current context.
    """
    embedded = Session(_WireConnection())

    assert _registered(session) == []
    assert _sent(session) == []
    assert _registered(embedded) == []


@ft.control("CallableFieldService")
class CallableFieldService(ft.Service):
    """Keeps Python-only state in a public field, which can't be serialized."""

    callback: Optional[Any] = None

    def init(self):
        self.callback = lambda: None


@ft.control("ParentService")
class ParentService(ft.Service):
    label: Optional[str] = None

    def init(self):
        self._child = LateFieldsService(src="child")
        self.label = "parent"


def _registry_add_ops(session: Session) -> list[list]:
    """Patch ops of every message that changed the service registry."""
    registry_id = session.page._services._i
    return [
        body["patch"][1:]
        for action, body in _sent(session)
        if action == MessageAction.PATCH_CONTROL and body["id"] == registry_id
    ]


def test_registration_failure_is_raised_and_rolled_back(session):
    with pytest.raises(RuntimeError, match="Cannot serialize method"):
        CallableFieldService()

    assert _registered(session) == []

    svc = LateFieldsService(src="next")

    assert _registered(session) == _ids(svc)
    # Sent as the registry's first service - not relative to the failed one.
    [ops] = _registry_add_ops(session)
    assert ops[0][:4] == [0, 0, "_services", [_snapshots(session, svc)[0]]]


def test_service_constructed_before_page_is_sent_goes_out_with_the_page():
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
    parent = ParentService()

    assert _registered(session) == _ids(parent._child, parent)
    assert _snapshots(session, parent)[0]["label"] == "parent"
    assert _snapshots(session, parent._child)[0]["src"] == "CHILD"


def _core_services() -> list[type[Service]]:
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


@pytest.mark.parametrize("service_cls", _core_services(), ids=lambda cls: cls.__name__)
def test_every_core_service_registers_once(session, service_cls):
    # Sensors only allow themselves on mobile and web.
    session.page.platform = ft.PagePlatform.ANDROID

    svc = service_cls()

    assert _registered(session) == _ids(svc)
    assert len(_snapshots(session, svc)) == 1


def test_failed_send_removes_the_failed_instance_not_an_equal_one(session):
    first = ft.Clipboard()
    session.connection.fail_next_send = RuntimeError("connection lost")

    with pytest.raises(RuntimeError, match="connection lost"):
        ft.Clipboard()

    assert _registered(session) == _ids(first)

    third = ft.Clipboard()

    assert _registered(session) == _ids(first, third)
    # The client got `first`, then `third` added after it - nothing removed.
    [_, ops] = _registry_add_ops(session)
    assert [op[0] for op in ops] == [Operation.Add.value]
    assert ops[0][2:] == [1, _snapshots(session, third)[0]]


def test_interrupted_send_is_rolled_back(session):
    session.connection.fail_next_send = KeyboardInterrupt()

    with pytest.raises(KeyboardInterrupt):
        LateFieldsService()

    assert _registered(session) == []
    svc = LateFieldsService()
    assert _registered(session) == _ids(svc)


@ft.control("DidMountRaisesService")
class DidMountRaisesService(ft.Service):
    def did_mount(self):
        super().did_mount()
        raise ValueError("did_mount failed")


def test_service_whose_did_mount_raises_stays_registered(session):
    """The client already received it, so Python must keep it too."""
    with pytest.raises(ValueError, match="did_mount failed"):
        DidMountRaisesService()

    [svc] = session.page._services._services
    assert _snapshots(session, svc)


def test_unsupported_service_does_not_break_later_registrations(session):
    session.page.platform = ft.PagePlatform.MACOS

    with pytest.raises(ft.FletUnsupportedPlatformException):
        ft.Accelerometer()

    clipboard = ft.Clipboard()

    assert _registered(session) == _ids(clipboard)
    assert _snapshots(session, clipboard)


@ft.control("PageInInitService")
class PageInInitService(ft.Service):
    platform: Optional[str] = None

    def init(self):
        super().init()
        self.platform = ft.context.page.platform.value
        try:
            self.page_in_init = self.page is not None
        except RuntimeError:
            self.page_in_init = False


def test_page_is_not_attached_in_init_but_context_page_is_available(session):
    session.page.platform = ft.PagePlatform.ANDROID

    svc = PageInInitService()

    assert svc.page_in_init is False
    assert _snapshots(session, svc)[0]["platform"] == "android"
    assert svc.page is session.page


@ft.control("OptedOutService")
class OptedOutService(ft.Service):
    _auto_register = False


def test_auto_register_false_opts_out(session):
    OptedOutService()

    assert _registered(session) == []
    assert _sent(session) == []


def test_registration_does_not_mark_update_called(session):
    """Registration is internal bookkeeping, not a user `update()` call."""
    context.reset_update_called()

    LateFieldsService()

    assert _sent(session)
    assert context.was_update_called() is False
