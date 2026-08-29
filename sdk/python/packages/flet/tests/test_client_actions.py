import weakref

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.messaging.protocol import configure_encode_object_for_msgpack


class FakeSession:
    def __init__(self):
        self.index: dict[int, object] = {}

    def patch_control(self, control, **kwargs):
        pass

    def schedule_update(self, control):
        pass

    async def after_event(self, control):
        pass


@pytest.fixture
def page():
    # Page holds its session weakly, so the local reference has to outlive the
    # test or `page.session` raises "An attempt to fetch destroyed session".
    session = FakeSession()
    page = ft.Page(sess=session)
    page._dialogs._parent = weakref.ref(page)
    token = _context_page.set(page)
    yield page
    _context_page.reset(token)
    del session


def pack(obj):
    return msgpack.unpackb(
        msgpack.packb(obj, default=configure_encode_object_for_msgpack(BaseControl)),
        strict_map_key=False,
    )


def test_page_is_serializable_after_creating_an_action(page):
    """
    The services an action targets must not be cached anywhere that reaches the
    wire. Stashing them in `page._internals` - which *is* serialized - made the
    whole page unpackable with "type object 'Clipboard' has no attribute '_i'".
    """
    page.add(ft.Button("Copy", action=ft.CopyToClipboard("hello")))
    pack(page)


def test_action_serializes_as_a_service_call(page):
    action = ft.CopyToClipboard("hello")
    assert pack(action) == {
        "service_id": action._service._i,
        "method": "set",
        "args": {"data": "hello"},
    }


def test_actions_of_one_kind_share_a_single_service(page):
    first = ft.CopyToClipboard("a")
    second = ft.CopyToClipboard("b")
    assert first.service_id == second.service_id


def test_actions_of_different_kinds_target_different_services(page):
    assert (
        ft.CopyToClipboard("a").service_id != ft.OpenUrl("https://flet.dev").service_id
    )


def test_open_url_passes_target_through(page):
    action = ft.OpenUrl("https://flet.dev", target=ft.UrlTarget.BLANK)
    assert action.args["url"].target is ft.UrlTarget.BLANK
    # "_blank" is the reserved keyword; "blank" would be read as a window name.
    assert pack(action)["args"]["url"]["target"] == "_blank"


def test_pick_files_targets_the_users_file_picker(page):
    picker = ft.FilePicker()
    action = ft.PickFiles(picker, allow_multiple=True)
    assert action.service_id == picker._i
    assert action.method == "pick_files"
    assert action.args["allow_multiple"] is True


def test_action_is_carried_by_every_control_that_declares_one(page):
    for control in [
        ft.Button("x"),
        ft.IconButton(icon=ft.Icons.ADD),
        ft.Container(),
        ft.ListTile(),
        ft.FloatingActionButton(icon=ft.Icons.ADD),
        ft.OutlinedButton("x"),
        ft.TextButton("x"),
        ft.CupertinoButton(content="x"),
        ft.CupertinoListTile(title=ft.Text("x")),
        ft.TextSpan("x"),
    ]:
        assert isinstance(control, ft.ActionControl)
        control.action = ft.CopyToClipboard("hello")
        assert pack(control)["action"]["method"] == "set"


def test_action_is_omitted_when_unset(page):
    assert "action" not in pack(ft.Button("x"))
