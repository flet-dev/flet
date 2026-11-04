"""Tests that frames from a client change only what a real client can change."""

import asyncio
import datetime
import logging
import weakref
from typing import ClassVar, Optional

import msgpack
import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.controls.object_patch import ObjectPatch
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    MessageAction,
    configure_encode_object_for_msgpack,
)
from flet.messaging.session import (
    _REJECTED_VALUES_INTERVAL,
    Session,
    _warned_client_fields,
)
from flet.pubsub.pubsub_hub import PubSubHub

SHARED_STYLE = ft.TextStyle(size=10)


def _encode(value) -> bytes:
    """Encodes `value` like a transport does, which records the diff snapshots."""
    return msgpack.packb(
        value, default=configure_encode_object_for_msgpack(BaseControl)
    )


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.messages = []

    def send_message(self, message):
        _encode([message.action, message.body])
        self.messages.append(message)


@pytest.fixture
def session():
    """A session whose page was sent to its client, so controls are indexed."""
    session = Session(_RecordingConnection())
    token = _context_page.set(session.page)
    yield session
    _context_page.reset(token)


def _mount(session: Session, *controls):
    """Adds `controls` to the page and sends the page to the client."""
    session.page.controls.extend(controls)
    _encode(session.get_page_patch())


def _patch_ops(session: Session) -> list:
    """Returns the patch messages an update of the page sends to the client."""
    conn = session.connection
    conn.messages.clear()
    session.patch_control(session.page)
    return [m for m in conn.messages if m.action == MessageAction.PATCH_CONTROL]


class TestPrivateState:
    @pytest.mark.parametrize(
        "name",
        [
            "_app_flag",
            "_Page__authorization",
            "_Page__session",
            "_i",
            "_c",
            "_values",
            "_dirty",
            "_internals",
            "_parent",
            "_frozen",
            "_isolated",
            "__dict__",
            "__class__",
        ],
    )
    def test_page_private_attribute_is_ignored(self, session, name):
        """A client can't write any private attribute of the page."""
        page = session.page
        before = dict(vars(page))
        session.apply_patch(page._i, {name: {"forged": True}})
        assert vars(page).keys() == before.keys()
        for key, value in before.items():
            assert vars(page)[key] is value
        assert page.auth is None
        assert page.session is session

    @pytest.mark.parametrize("name", ["_i", "_c", "_frozen", "_values", "__dict__"])
    def test_control_private_attribute_is_ignored(self, session, name):
        """A client can't write any private attribute of a control."""
        text = ft.Text("kept")
        _mount(session, text)
        control_id, control_type = text._i, text._c
        session.apply_patch(control_id, {name: {"forged": True}})
        assert text.value == "kept"
        assert text._i == control_id
        assert text._c == control_type
        assert not hasattr(text, "_frozen")

    def test_registration_ignores_private_attributes(self, session):
        """The page state of a registration can't write private attributes."""
        session.apply_page_patch(
            {
                "route": "/",
                "_app_flag": True,
                "_Page__authorization": "forged",
                "window": {"_i": 99, "_app_flag": True, "width": 5.0},
            }
        )
        assert not hasattr(session.page, "_app_flag")
        assert session.page.auth is None
        assert session.page.window._i == 2
        assert not hasattr(session.page.window, "_app_flag")
        assert session.page.window.width == 5.0


class TestDeclaredFields:
    def test_server_owned_page_fields_are_ignored(self, session):
        """A client can't change the page fields only the server sets."""
        page = session.page
        page.client_ip = "1.2.3.4"
        page.client_user_agent = "real"
        session.apply_patch(
            page._i,
            {
                "client_ip": "10.0.0.1",
                "client_user_agent": "forged",
                "title": "forged",
                "views": [],
                "web": True,
                "platform": "ios",
            },
        )
        assert page.client_ip == "1.2.3.4"
        assert page.client_user_agent == "real"
        assert page.title != "forged"
        assert len(page.views) == 1
        assert page.web is False
        assert page.platform is None

    def test_control_fields_a_client_never_sends_are_ignored(self, session):
        """A client can't change a field the control's Dart code never sends."""

        def handler(e):
            pass

        button = ft.Button("Pay", data={"role": "viewer"}, on_click=handler, key="pay")
        text = ft.Text("immutable", data="server")
        _mount(session, button, text)

        session.apply_patch(
            button._i,
            {
                "data": {"role": "admin"},
                "on_click": None,
                "key": "forged",
                "disabled": True,
                "visible": False,
            },
        )
        session.apply_patch(text._i, {"value": "forged", "data": "forged"})

        assert button.data == {"role": "viewer"}
        assert button.on_click is handler
        assert button.key == "pay"
        assert button.disabled is False
        assert button.visible is True
        assert text.value == "immutable"
        assert text.data == "server"

    def test_child_controls_cannot_be_replaced(self, session):
        """A client can't replace or reach through a control's children."""
        inner = ft.Text("kept")
        container = ft.Container(content=inner)
        column = ft.Column(controls=[ft.Text("first")])
        _mount(session, container, column)

        session.apply_patch(container._i, {"content": {"value": "forged"}})
        session.apply_patch(column._i, {"controls": []})

        assert container.content is inner
        assert inner.value == "kept"
        assert len(column.controls) == 1

    def test_malformed_patch_is_ignored(self, session):
        """A patch that isn't a mapping changes nothing and doesn't raise."""
        route = session.page.route
        session.apply_patch(session.page._i, "not-a-mapping")
        session.apply_page_patch("not-a-mapping")
        assert session.page.route == route


class TestNestedValues:
    def test_shared_value_object_is_not_changed(self, session):
        """A patch of a nested value doesn't reach an object other sessions share."""
        field = ft.TextField(
            selection=ft.TextSelection(base_offset=0, extent_offset=0),
        )
        shared = field.selection
        _mount(session, field)

        session.apply_patch(
            field._i, {"selection": {"base_offset": 3, "extent_offset": 4}}
        )

        assert shared.base_offset == 0
        assert field.selection.base_offset == 3
        assert field.selection.extent_offset == 4

    def test_replaced_value_is_not_sent_back_to_the_client(self, session):
        """A value that came from the client isn't echoed to it by the next update."""
        field = ft.TextField(
            selection=ft.TextSelection(base_offset=0, extent_offset=0),
        )
        _mount(session, field)

        session.apply_patch(
            field._i, {"selection": {"base_offset": 3, "extent_offset": 4}}
        )
        session.apply_page_patch(
            {"media": {"padding": {"top": 7.0}, "device_pixel_ratio": 2.0}}
        )

        assert _patch_ops(session) == []

    def test_python_change_of_a_replaced_value_is_sent(self, session):
        """A Python change after a client patch of a value reaches the client."""
        field = ft.TextField(
            selection=ft.TextSelection(base_offset=0, extent_offset=0),
        )
        _mount(session, field)
        session.apply_patch(
            field._i, {"selection": {"base_offset": 3, "extent_offset": 4}}
        )

        field.selection.base_offset = 1

        assert len(_patch_ops(session)) == 1

    def test_text_style_is_not_client_writable(self, session):
        """A style shared by many controls can't be changed by a client."""
        text = ft.Text("x", style=SHARED_STYLE)
        _mount(session, text)
        session.apply_patch(text._i, {"style": {"size": 99, "_app_flag": True}})
        assert text.style is SHARED_STYLE
        assert SHARED_STYLE.size == 10
        assert not hasattr(SHARED_STYLE, "_app_flag")

    def test_private_keys_of_a_nested_value_are_ignored(self, session):
        """A nested patch can't write private attributes of the value object."""
        session.apply_page_patch(
            {
                "media": {
                    "device_pixel_ratio": 2.0,
                    "_app_flag": True,
                    "__changes": {"x": 1},
                    "padding": {"top": 1.0, "_values": {"left": 9}},
                }
            }
        )
        media = session.page.media
        assert media.device_pixel_ratio == 2.0
        assert not hasattr(media, "_app_flag")
        assert media.padding.top == 1.0
        assert media.padding.left == 0

    def test_wrong_type_for_a_value_field_is_ignored(self, session):
        """A scalar can't replace a value object, and `None` only an optional one."""
        media = session.page.media
        session.apply_page_patch({"media": "forged"})
        assert session.page.media is media
        session.apply_page_patch({"media": None})
        assert session.page.media is media

    def test_optional_value_field_can_be_cleared(self, session):
        """An optional value field can be cleared by the client."""
        field = ft.TextField(
            selection=ft.TextSelection(base_offset=0, extent_offset=0),
        )
        _mount(session, field)
        session.apply_patch(field._i, {"selection": None})
        assert field.selection is None

    def test_invalid_enum_value_does_not_abort_the_patch(self, session):
        """One bad value is ignored, and the other values of the patch are applied."""
        session.apply_page_patch(
            {"platform": "fuchsia", "platform_brightness": "dark", "route": "/x"}
        )
        assert session.page.platform is None
        assert session.page.platform_brightness == ft.Brightness.DARK
        assert session.page.route == "/x"


class TestLegitimateClientUpdates:
    @pytest.mark.parametrize(
        "make, patch",
        [
            (lambda: ft.TextField(), {"value": "typed"}),
            (lambda: ft.CupertinoTextField(), {"value": "typed"}),
            (lambda: ft.Checkbox(), {"value": True}),
            (lambda: ft.Switch(), {"value": True}),
            (lambda: ft.Slider(), {"value": 0.5}),
            (lambda: ft.RangeSlider(0.0, 1.0), {"start_value": 0.5, "end_value": 0.6}),
            (lambda: ft.Dropdown(), {"value": "a", "text": "A"}),
            (lambda: ft.RadioGroup(ft.Column()), {"value": "a"}),
            (lambda: ft.SearchBar(), {"value": "typed"}),
            (lambda: ft.AutoComplete(), {"value": "typed", "_selected_index": 2}),
            (lambda: ft.Tabs(ft.Column(), length=1), {"selected_index": 0}),
            (lambda: ft.PageView(controls=[]), {"selected_index": 1}),
            (
                lambda: ft.NavigationBar(
                    destinations=[
                        ft.NavigationBarDestination("a"),
                        ft.NavigationBarDestination("b"),
                    ]
                ),
                {"selected_index": 1},
            ),
            (lambda: ft.ExpansionTile(ft.Text("t")), {"expanded": True}),
            (lambda: ft.Chip(ft.Text("c")), {"selected": True}),
            (
                lambda: ft.SegmentedButton(
                    segments=[ft.Segment("a", label="a"), ft.Segment("b", label="b")],
                    selected=["b"],
                ),
                {"selected": ["a"]},
            ),
            (lambda: ft.AlertDialog(title="t", open=True), {"open": False}),
            (lambda: ft.SnackBar(ft.Text("s"), open=True), {"open": False}),
            (lambda: ft.DatePicker(), {"open": False, "entry_mode": "input"}),
        ],
    )
    def test_field_sent_by_the_dart_client_is_applied(self, session, make, patch):
        """Every field a control's Dart code sends reaches the Python control."""
        control = make()
        _mount(session, control)
        session.apply_patch(control._i, patch)
        for name, value in patch.items():
            actual = getattr(control, name)
            assert getattr(actual, "value", actual) == value

    def test_auto_complete_selected_index(self, session):
        """`AutoComplete.selected_index` follows what the client selects."""
        control = ft.AutoComplete()
        _mount(session, control)
        assert control.selected_index is None
        session.apply_patch(control._i, {"_selected_index": 2})
        assert control.selected_index == 2

    def test_undeclared_dart_only_keys_are_ignored_without_warning(
        self, session, caplog
    ):
        """A key the Dart code sends but Python has no field for isn't logged."""
        bar = ft.SnackBar(ft.Text("s"), open=True)
        _mount(session, bar)
        with caplog.at_level(logging.WARNING, logger="flet"):
            session.apply_patch(bar._i, {"_dismissed": True, "open": False})
        assert bar.open is False
        assert not hasattr(bar, "_dismissed")
        assert caplog.records == []

    def test_frozen_control_accepts_a_client_value(self, session):
        """A client's value reaches a frozen control, as a declarative app builds."""
        field = ft.TextField()
        _mount(session, field)
        field._frozen = True
        session.apply_patch(field._i, {"value": "typed"})
        assert field.value == "typed"


class TestPageRegistration:
    def test_first_registration_sets_the_environment(self, session):
        """The first registration sets everything the Dart client reports."""
        session.apply_page_patch(
            {
                "route": "/start",
                "pwa": False,
                "web": True,
                "debug": True,
                "wasm": True,
                "test": False,
                "multi_view": False,
                "pyodide": False,
                "platform_brightness": "light",
                "width": 800.0,
                "height": 600.0,
                "platform": "macos",
                "embedded": False,
                "window": {"width": 800.0, "focused": True},
                "media": {
                    "padding": {"top": 1.0, "right": 2.0, "bottom": 3.0, "left": 4.0},
                    "view_padding": {"top": 0, "right": 0, "bottom": 0, "left": 0},
                    "view_insets": {"top": 0, "right": 0, "bottom": 0, "left": 0},
                    "device_pixel_ratio": 2.0,
                    "orientation": "landscape",
                    "always_use_24_hour_format": True,
                },
            }
        )
        page = session.page
        assert page.route == "/start"
        assert page.web is True
        assert page.debug is True
        assert page.wasm is True
        assert page.platform == ft.PagePlatform.MACOS
        assert page.platform_brightness == ft.Brightness.LIGHT
        assert page.width == 800.0
        assert page.window.width == 800.0
        assert page.window.focused is True
        assert page.media.padding.left == 4.0
        assert page.media.device_pixel_ratio == 2.0
        assert page.media.orientation == ft.Orientation.LANDSCAPE

    def test_later_registration_keeps_the_environment(self, session):
        """A client reconnecting to a session can't change what it first reported."""
        session.apply_page_patch({"route": "/", "web": True, "platform": "macos"})
        session.apply_page_patch(
            {
                "route": "/next",
                "web": False,
                "debug": True,
                "platform": "ios",
                "width": 5.0,
                "window": {"width": 6.0},
            }
        )
        page = session.page
        assert page.web is True
        assert page.debug is False
        assert page.platform == ft.PagePlatform.MACOS
        assert page.route == "/next"
        assert page.width == 5.0
        assert page.window.width == 6.0

    def test_environment_cannot_be_patched_after_registration(self, session):
        """An update message can't change the environment fields at any point."""
        session.apply_patch(session.page._i, {"web": True, "debug": True})
        assert session.page.web is False
        assert session.page.debug is False
        session.apply_page_patch({"web": True})
        session.apply_patch(session.page._i, {"web": False})
        assert session.page.web is True

    def test_reconnect_window_echo_keeps_the_window_handler(self, session):
        """The window state a client echoes on reconnect can't replace a handler."""

        def handler(e):
            pass

        window = session.page.window
        window.on_event = handler
        session.apply_page_patch(
            {"window": {"on_event": True, "bgcolor": "red", "width": 5.0}}
        )
        assert window.on_event is handler
        assert window.bgcolor != "red"
        assert window.width == 5.0

    def test_runtime_window_updates_are_applied(self, session):
        """The desktop client's window state reaches the `Window` control."""
        _mount(session)
        window = session.page.window
        session.apply_patch(
            window._i, {"width": 5.0, "maximized": True, "visible": False}
        )
        assert window.width == 5.0
        assert window.maximized is True
        assert window.visible is False


class TestInputGate:
    @pytest.mark.parametrize(
        "make",
        [
            lambda: ft.TextField(value="kept", read_only=True),
            lambda: ft.TextField(value="kept", disabled=True),
            lambda: ft.TextField(value="kept", visible=False),
        ],
    )
    def test_value_of_a_field_a_user_cannot_edit_is_ignored(self, session, make):
        """A client can't change a field a user can't edit."""
        field = make()
        _mount(session, field)
        session.apply_patch(field._i, {"value": "forged"})
        assert field.value == "kept"

    @pytest.mark.parametrize("ancestor", [{"disabled": True}, {"visible": False}])
    def test_value_under_a_blocking_ancestor_is_ignored(self, session, ancestor):
        """The disabled and hidden state of an ancestor protects a field."""
        field = ft.TextField(value="kept")
        _mount(session, ft.Column(controls=[field], **ancestor))
        session.apply_patch(field._i, {"value": "forged"})
        assert field.value == "kept"

    @pytest.mark.parametrize(
        "make, name, value",
        [
            (lambda **kw: ft.Slider(value=0.5, **kw), "value", 0.9),
            (lambda **kw: ft.Switch(value=False, **kw), "value", True),
            (lambda **kw: ft.Checkbox(value=False, **kw), "value", True),
            (
                lambda **kw: ft.Chip(ft.Text("c"), selected=False, **kw),
                "selected",
                True,
            ),
            (
                lambda **kw: ft.NavigationBar(
                    destinations=[
                        ft.NavigationBarDestination("a"),
                        ft.NavigationBarDestination("b"),
                    ],
                    selected_index=0,
                    **kw,
                ),
                "selected_index",
                1,
            ),
        ],
    )
    def test_field_of_a_control_gated_on_disabled_is_ignored(
        self, session, make, name, value
    ):
        """A field the widget holds back while disabled can't be changed then."""
        control = make(disabled=True)
        before = getattr(control, name)
        _mount(session, control)
        session.apply_patch(control._i, {name: value})
        assert getattr(control, name) == before

    @pytest.mark.parametrize(
        "make, patch",
        [
            (lambda: ft.SearchBar(), {"value": "typed"}),
            (lambda: ft.AutoComplete(), {"value": "typed", "_selected_index": 1}),
            (lambda: ft.CupertinoTimerPicker(), {"value": 60}),
            (lambda: ft.PageView(controls=[]), {"selected_index": 1}),
        ],
    )
    def test_value_of_a_widget_that_ignores_disabled_is_applied(
        self, session, make, patch
    ):
        """A widget that keeps working while disabled reaches Python."""
        control = make()
        _mount(session, ft.Column(controls=[control], disabled=True))
        session.apply_patch(control._i, patch)
        for name, value in patch.items():
            assert getattr(control, name) == value

    def test_date_picker_under_a_disabled_page_is_applied(self, session):
        """A picker dialog keeps working under a disabled page."""
        picker = ft.DatePicker(open=True)
        session.page.disabled = True
        _mount(session, picker)
        when = datetime.datetime(2026, 5, 20, tzinfo=datetime.timezone.utc)
        session.apply_patch(picker._i, {"value": when, "open": False})
        assert picker.value == when
        assert picker.open is False

    def test_selection_of_a_read_only_field_is_applied(self, session):
        """A user can select text in a read-only field."""
        field = ft.TextField(value="text", read_only=True)
        _mount(session, field)
        session.apply_patch(
            field._i, {"selection": {"base_offset": 1, "extent_offset": 2}}
        )
        assert field.selection.base_offset == 1

    def test_hidden_page_does_not_block_its_controls(self, session):
        """`Page.visible` has no effect on the client, so its controls keep working."""
        field = ft.TextField(value="old")
        session.page.visible = False
        _mount(session, field)
        session.apply_patch(field._i, {"value": "typed"})
        assert field.value == "typed"

    def test_dismissal_of_a_dialog_under_a_disabled_page_is_applied(self, session):
        """A dialog closing while the page is disabled reaches Python."""
        dialog = ft.AlertDialog(title="t", open=True)
        session.page.disabled = True
        _mount(session, dialog)
        session.apply_patch(dialog._i, {"open": False})
        assert dialog.open is False

    def test_closing_a_hidden_dialog_is_applied(self, session):
        """A dialog hidden while it closes can report that it closed."""
        dialog = ft.AlertDialog(title="t", open=True, visible=False)
        _mount(session, dialog)
        session.apply_patch(dialog._i, {"open": False})
        assert dialog.open is False

    @pytest.mark.parametrize("value", [True, "yes", 1, None])
    def test_client_cannot_open_a_dialog(self, session, value):
        """A dialog only accepts being closed, as a client never opens one."""
        dialog = ft.AlertDialog(title="t", open=False)
        _mount(session, dialog)
        session.apply_patch(dialog._i, {"open": value})
        assert dialog.open is False

    def test_field_in_a_closed_dialog_is_ignored(self, session):
        """A field inside a closed dialog isn't rendered, so it can't change."""
        field = ft.TextField(value="kept")
        dialog = ft.AlertDialog(content=field, open=False)
        session.page.overlay.append(dialog)
        _mount(session)
        session.apply_patch(field._i, {"value": "forged"})
        assert field.value == "kept"

    def test_field_in_an_open_dialog_is_applied(self, session):
        """A field inside an open dialog works like any other."""
        field = ft.TextField(value="old")
        dialog = ft.AlertDialog(content=field, open=True)
        session.page.overlay.append(dialog)
        _mount(session)
        session.apply_patch(field._i, {"value": "typed"})
        assert field.value == "typed"

    def test_rejected_value_is_sent_back_to_the_client(self, session):
        """The client gets the server's value back, so the widget matches it."""
        field = ft.TextField(value="kept", disabled=True)
        _mount(session, field)
        session.connection.messages.clear()

        session.apply_patch(field._i, {"value": "forged"})

        patches = session.connection.messages
        assert len(patches) == 1
        assert patches[0].action == MessageAction.PATCH_CONTROL
        assert patches[0].body.id == field._i
        operation = patches[0].body.patch[1]
        assert operation[2:] == ["value", "kept"]

    @pytest.mark.asyncio
    async def test_rejected_values_in_a_burst_are_sent_once(self, session):
        """Small frames can't queue a copy of a large value each."""
        field = ft.TextField(value="x" * 1000, read_only=True)
        _mount(session, field)
        session.connection.messages.clear()

        for _ in range(100):
            session.apply_patch(field._i, {"value": "forged"})
        await asyncio.sleep(_REJECTED_VALUES_INTERVAL * 2)

        assert len(session.connection.messages) == 1

    @pytest.mark.asyncio
    async def test_rejected_value_is_read_when_it_is_sent(self, session):
        """The client gets the value the field holds at the time of sending."""
        field = ft.TextField(value="old", disabled=True)
        _mount(session, field)
        session.connection.messages.clear()

        session.apply_patch(field._i, {"value": "forged"})
        field.value = "new"
        await asyncio.sleep(_REJECTED_VALUES_INTERVAL * 2)

        assert session.connection.messages[0].body.patch[1][2:] == ["value", "new"]

    def test_pending_list_change_is_not_applied_twice(self, session):
        """A list sent back isn't changed again by the update that follows."""
        button = ft.SegmentedButton(
            segments=[ft.Segment("a", label="a"), ft.Segment("b", label="b")],
            selected=["a"],
            allow_multiple_selection=True,
            disabled=True,
        )
        _mount(session, button)
        button.selected.append("b")
        session.apply_patch(button._i, {"selected": ["forged"]})
        assert session.connection.messages[-1].body.patch[1][3] == ["a", "b"]
        assert _patch_ops(session) == []

    def test_rejected_value_of_a_removed_control_is_not_sent(self, session):
        """A control that left the page gets nothing, as the client has no widget."""
        field = ft.TextField(value="kept", disabled=True)
        _mount(session, field)
        session.connection.messages.clear()
        session._Session__index.pop(field._i)
        session._Session__rejected_fields[field._i] = {"value"}
        session._Session__send_rejected_fields()
        assert session.connection.messages == []

    def test_later_python_write_of_the_kept_value_stays_in_sync(self, session):
        """A rejected value leaves nothing for a later update of the field to fix."""
        field = ft.TextField(value="kept", disabled=True)
        _mount(session, field)
        session.apply_patch(field._i, {"value": "forged"})
        field.value = "kept"
        field.disabled = False
        ops = _patch_ops(session)
        assert len(ops) == 1
        assert "value" not in str(ops[0].body.patch)

    def test_unlisted_field_gets_no_answer(self, session):
        """A property a client may never change isn't answered, which limits traffic."""
        text = ft.Text("kept")
        _mount(session, text)
        session.connection.messages.clear()
        session.apply_patch(text._i, {"value": "forged", "made_up": 1})
        assert session.connection.messages == []


class TestValueTypes:
    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda: ft.TextField(value="kept"), "value"),
            (lambda: ft.Switch(value=True), "value"),
            (lambda: ft.Slider(value=0.5), "value"),
            (lambda: ft.Dropdown(value="a"), "value"),
            (lambda: ft.RadioGroup(ft.Column(), value="a"), "value"),
        ],
    )
    @pytest.mark.parametrize("forged", [{"$ne": ""}, ["a", "b"]], ids=["dict", "list"])
    def test_scalar_field_cannot_hold_a_container(self, session, make, name, forged):
        """A `dict` or `list` can't reach a field that holds a single value."""
        control = make()
        before = getattr(control, name)
        _mount(session, control)
        session.apply_patch(control._i, {name: forged})
        assert getattr(control, name) == before

    @pytest.mark.parametrize("forged", [{"route": "/x"}, ["/x"]], ids=["dict", "list"])
    def test_route_cannot_hold_a_container(self, session, forged):
        """The page route stays a string."""
        session.apply_page_patch({"route": "/"})
        session.apply_patch(session.page._i, {"route": forged})
        assert session.page.route == "/"

    @pytest.mark.parametrize(
        "forged", ["a", [{"deep": 1}], [["a"]]], ids=["string", "dict", "list"]
    )
    def test_list_field_items_must_be_scalars(self, session, forged):
        """A list of values stays a flat list."""
        control = ft.SegmentedButton(
            segments=[ft.Segment("a", label="a"), ft.Segment("b", label="b")],
            selected=["b"],
        )
        _mount(session, control)
        session.apply_patch(control._i, {"selected": forged})
        assert control.selected == ["b"]

    def test_value_object_built_from_a_patch_checks_its_fields(self, session):
        """A value object built by a patch can't hold a `dict` in a scalar field."""
        field = ft.TextField(value="text")
        _mount(session, field)
        session.apply_patch(
            field._i, {"selection": {"base_offset": {"$gt": ""}, "extent_offset": [1]}}
        )
        assert field.selection is None

    def test_union_with_a_dataclass_cannot_hold_a_dict(self, session):
        """A `dict` isn't accepted for a value that is never converted from one."""
        picker = ft.CupertinoTimerPicker()
        before = picker.value
        _mount(session, picker)
        session.apply_patch(picker._i, {"value": {"$gt": ""}})
        session.apply_patch(picker._i, {"value": ["x"]})
        assert picker.value == before
        session.apply_patch(picker._i, {"value": 60})
        assert picker.value == 60

    def test_bool_value_of_a_string_field_is_kept(self, session):
        """A scalar is written as sent, as apps can use other types than declared."""
        group = ft.RadioGroup(ft.Column(), value="a")
        _mount(session, group)
        session.apply_patch(group._i, {"value": 1})
        assert group.value == 1


class TestNestedDeclarations:
    def test_control_inside_a_value_keeps_its_own_rules(self, session):
        """A value can't be used to reach the fields of a control it holds."""

        @ft.value
        class Holder:
            label: Optional[ft.Text] = None
            size: int = 0

        @ft.control("HolderView", client_writable=("holder",))
        class HolderView(ft.LayoutControl):
            holder: Optional[Holder] = None

        inner = ft.Text("kept", data="server")
        view = HolderView(holder=Holder(label=inner))
        _mount(session, view)

        session.apply_patch(
            view._i,
            {"holder": {"size": 5, "label": {"value": "forged", "data": "forged"}}},
        )

        assert view.holder.size == 5
        assert inner.value == "kept"
        assert inner.data == "server"

    def test_control_cannot_be_built_from_client_data(self, session):
        """A client can't create a control through an empty field of a value."""

        @ft.value
        class Holder:
            label: Optional[ft.Text] = None

        @ft.control("HolderField", client_writable=("label",))
        class HolderField(ft.LayoutControl):
            label: Optional[ft.Text] = None

        control = HolderField()
        _mount(session, control)
        session.apply_patch(control._i, {"label": {"value": "forged"}})
        assert control.label is None

    def test_class_level_annotations_are_not_writable(self, session):
        """A nested patch only writes dataclass fields, not `ClassVar` names."""

        @ft.value
        class Holder:
            KIND: ClassVar[str] = "server"
            size: int = 0

        @ft.control("ClassVarView", client_writable=("holder",))
        class ClassVarView(ft.LayoutControl):
            holder: Optional[Holder] = None

        view = ClassVarView(holder=Holder())
        _mount(session, view)
        session.apply_patch(view._i, {"holder": {"KIND": "forged", "size": 3}})
        assert view.holder.size == 3
        assert view.holder.KIND == "server"

    def test_field_with_an_unresolved_annotation_is_applied(self, session):
        """A listed field is written even if its annotation is only a string."""

        @ft.control("LazyField", client_writable=("stars",))
        class LazyField(ft.LayoutControl):
            stars: "int" = 0

        control = LazyField()
        _mount(session, control)
        session.apply_patch(control._i, {"stars": 4})
        assert control.stars == 4


class TestClientEvents:
    @pytest.mark.parametrize(
        "name",
        ["connect", "disconnect", "close", "login", "logout", "views_pop_until"],
    )
    @pytest.mark.asyncio
    async def test_server_only_page_event_is_ignored(self, session, name):
        """A client can't trigger a page event only the server originates."""
        calls = []
        setattr(session.page, f"on_{name}", lambda e: calls.append(e))
        await session.dispatch_event(session.page._i, name, None)
        await session.dispatch_event(
            session.page._i, name, {"error": "", "error_description": ""}
        )
        assert calls == []

    @pytest.mark.parametrize(
        "name, data",
        [
            ("route_change", {"route": "/x"}),
            ("resize", {"width": 1.0, "height": 2.0}),
            ("error", "client error"),
            ("app_lifecycle_state_change", {"state": "resume"}),
            ("view_pop", {"route": "/"}),
        ],
    )
    @pytest.mark.asyncio
    async def test_page_event_from_the_client_is_dispatched(self, session, name, data):
        """Page events the Dart client sends reach their handlers."""
        calls = []
        setattr(session.page, f"on_{name}", lambda e: calls.append(e))
        await session.dispatch_event(session.page._i, name, data)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_session_lifecycle_events_fire(self, session):
        """The events a session originates reach the page's handlers."""
        calls = []
        page = session.page
        page.on_connect = lambda e: calls.append("connect")
        page.on_disconnect = lambda e: calls.append("disconnect")
        page.on_close = lambda e: calls.append("close")

        await session.dispatch_connect_event()
        await session.disconnect(60)
        session.close()
        await asyncio.sleep(0)

        assert calls == ["connect", "disconnect", "close"]

    @pytest.mark.asyncio
    async def test_login_event_triggered_by_python_fires(self, session):
        """A login Python code completes reaches `on_login`."""
        calls = []
        page = session.page
        page.on_login = lambda e: calls.append(e.error)
        await page._trigger_event(
            "login",
            None,
            ft.LoginEvent(
                error="denied",
                error_description="",
                control=page,
                name="login",
            ),
        )
        assert calls == ["denied"]

    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda **kw: ft.Button("b", **kw), "click"),
            (lambda **kw: ft.Button("b", **kw), "long_press"),
            (lambda **kw: ft.FilledButton("b", **kw), "click"),
            (lambda **kw: ft.TextButton("b", **kw), "click"),
            (lambda **kw: ft.TextButton("b", **kw), "long_press"),
            (lambda **kw: ft.OutlinedButton("b", **kw), "click"),
            (lambda **kw: ft.OutlinedButton("b", **kw), "long_press"),
            (lambda **kw: ft.IconButton(ft.Icons.ADD, **kw), "click"),
            (lambda **kw: ft.TextField(**kw), "submit"),
            (lambda **kw: ft.Chip(ft.Text("c"), **kw), "select"),
            (lambda **kw: ft.Chip(ft.Text("c"), **kw), "delete"),
        ],
    )
    @pytest.mark.parametrize(
        "state", [{"disabled": True}, {"visible": False}], ids=["disabled", "hidden"]
    )
    @pytest.mark.parametrize("on_ancestor", [False, True], ids=["self", "ancestor"])
    @pytest.mark.asyncio
    async def test_command_on_an_unreachable_control_is_ignored(
        self, session, make, name, state, on_ancestor
    ):
        """A command for a hidden or disabled control doesn't run its handler."""
        calls = []
        control = make(**({} if on_ancestor else state))
        setattr(control, f"on_{name}", lambda e: calls.append(e))
        _mount(
            session,
            ft.Column(controls=[control], **state) if on_ancestor else control,
        )
        await session.dispatch_event(control._i, name, None)
        assert calls == []

    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda: ft.Button("b"), "click"),
            (lambda: ft.Button("b"), "long_press"),
            (lambda: ft.TextField(), "submit"),
            (lambda: ft.Chip(ft.Text("c")), "select"),
            (lambda: ft.Chip(ft.Text("c")), "delete"),
        ],
    )
    @pytest.mark.asyncio
    async def test_command_on_a_reachable_control_is_dispatched(
        self, session, make, name
    ):
        """A command for a visible and enabled control runs its handler."""
        calls = []
        control = make()
        setattr(control, f"on_{name}", lambda e: calls.append(e))
        _mount(session, control)
        await session.dispatch_event(control._i, name, None)
        assert len(calls) == 1

    @pytest.mark.parametrize(
        "name",
        ["tap", "double_tap", "secondary_tap", "tap_down", "pan_end", "long_press"],
    )
    @pytest.mark.asyncio
    async def test_gesture_on_a_hidden_control_is_ignored(self, session, name):
        """A gesture for a hidden control doesn't run its handler."""
        calls = []
        detector = ft.GestureDetector(visible=False)
        setattr(detector, f"on_{name}", lambda e: calls.append(e))
        _mount(session, detector)
        await session.dispatch_event(detector._i, name, None)
        assert calls == []

    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda: ft.Slider(visible=False), "change_end"),
            (lambda: ft.Dismissible(ft.Text("d"), visible=False), "update"),
            (
                lambda: ft.DataTable(
                    columns=[ft.DataColumn(ft.Text("c"))], visible=False
                ),
                "select_all",
            ),
        ],
    )
    @pytest.mark.asyncio
    async def test_other_events_of_a_hidden_control_are_ignored(
        self, session, make, name
    ):
        """A hidden control emits no events, whatever they are called."""
        calls = []
        control = make()
        setattr(control, f"on_{name}", lambda e: calls.append(e))
        _mount(session, ft.Column(controls=[control]))
        await session.dispatch_event(control._i, name, None)
        assert calls == []

    @pytest.mark.parametrize(
        "name, data",
        [
            ("blur", None),
            ("size_change", {"w": 1, "h": 1}),
            ("animation_end", None),
        ],
    )
    @pytest.mark.asyncio
    async def test_ending_events_of_a_hidden_control_are_dispatched(
        self, session, name, data
    ):
        """An event that ends what a control was doing passes once it is hidden."""
        calls = []
        field = ft.TextField(visible=False)
        setattr(field, f"on_{name}", lambda e: calls.append(e))
        _mount(session, field)
        await session.dispatch_event(field._i, name, data)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_hover_ending_in_a_closed_dialog_is_dispatched(self, session):
        """A widget that stops being hovered as its dialog closes reports it."""
        calls = []
        box = ft.Container(on_hover=lambda e: calls.append(e.data))
        dialog = ft.AlertDialog(content=box, open=False)
        session.page.overlay.append(dialog)
        _mount(session)
        await session.dispatch_event(box._i, "hover", "false")
        assert calls == ["false"]

    @pytest.mark.asyncio
    async def test_dialog_dismiss_after_closing_is_dispatched(self, session):
        """A dialog reports its dismissal after it is closed."""
        calls = []
        dialog = ft.AlertDialog(
            title="t", open=False, on_dismiss=lambda e: calls.append(e)
        )
        session.page.overlay.append(dialog)
        _mount(session)
        await session.dispatch_event(dialog._i, "dismiss", None)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_button_in_a_closed_dialog_is_ignored(self, session):
        """A button inside a closed dialog isn't rendered, so it can't be clicked."""
        calls = []
        button = ft.Button("Join", on_click=lambda e: calls.append(e))
        dialog = ft.AlertDialog(title="t", actions=[button], open=False)
        session.page.overlay.append(dialog)
        _mount(session)
        await session.dispatch_event(button._i, "click", None)
        assert calls == []

    @pytest.mark.asyncio
    async def test_button_in_an_open_dialog_is_dispatched(self, session):
        """A button inside an open dialog works like any other."""
        calls = []
        button = ft.Button("Join", on_click=lambda e: calls.append(e))
        dialog = ft.AlertDialog(title="t", actions=[button], open=True)
        session.page.overlay.append(dialog)
        _mount(session)
        await session.dispatch_event(button._i, "click", None)
        assert len(calls) == 1

    @pytest.mark.parametrize("name", ["tap", "long_press", "double_tap"])
    @pytest.mark.asyncio
    async def test_gesture_of_a_disabled_detector_is_dispatched(self, session, name):
        """A `GestureDetector` ignores `disabled`, so its gestures reach Python."""
        calls = []
        detector = ft.GestureDetector(disabled=True)
        setattr(detector, f"on_{name}", lambda e: calls.append(e))
        _mount(session, detector)
        await session.dispatch_event(detector._i, name, {"l": {"x": 0, "y": 0}})
        assert len(calls) == 1

    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda: ft.SearchBar(), "submit"),
            (lambda: ft.AutoComplete(), "select"),
            (lambda: ft.DataCell(ft.Text("c")), "long_press"),
        ],
    )
    @pytest.mark.asyncio
    async def test_command_of_a_widget_that_ignores_disabled_is_dispatched(
        self, session, make, name
    ):
        """A widget that keeps working while disabled reaches its handler."""
        calls = []
        control = make()
        setattr(control, f"on_{name}", lambda e: calls.append(e))
        session.index[control._i] = control
        control._parent = weakref.ref(session.page)
        session.page.disabled = True
        await session.dispatch_event(control._i, name, None)
        assert len(calls) == 1

    @pytest.mark.parametrize(
        "make, name",
        [
            (lambda **kw: ft.Slider(**kw), "change_end"),
            (lambda **kw: ft.Switch(**kw), "change"),
            (lambda **kw: ft.TextField(**kw), "change"),
            (lambda **kw: ft.Container(**kw), "tap_down"),
        ],
    )
    @pytest.mark.asyncio
    async def test_event_of_a_widget_gated_on_disabled_is_ignored(
        self, session, make, name
    ):
        """An event the widget holds back while disabled doesn't run its handler."""
        calls = []
        control = make(disabled=True)
        setattr(control, f"on_{name}", lambda e: calls.append(e))
        _mount(session, control)
        await session.dispatch_event(control._i, name, None)
        assert calls == []

    @pytest.mark.asyncio
    async def test_change_of_a_read_only_field_is_ignored(self, session):
        """A read-only field can't report an edit."""
        calls = []
        field = ft.TextField(read_only=True, on_change=lambda e: calls.append(e))
        _mount(session, field)
        await session.dispatch_event(field._i, "change", "forged")
        assert calls == []

    @pytest.mark.parametrize(
        "name, data",
        [("blur", None), ("focus", None), ("size_change", {"w": 1, "h": 1})],
    )
    @pytest.mark.asyncio
    async def test_lifecycle_event_of_a_disabled_control_is_dispatched(
        self, session, name, data
    ):
        """Disabling a control doesn't stop its focus and layout events."""
        calls = []
        field = ft.TextField(disabled=True)
        setattr(field, f"on_{name}", lambda e: calls.append(e))
        _mount(session, field)
        await session.dispatch_event(field._i, name, data)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_window_events_ignore_its_visible_field(self, session):
        """`Window.visible` is the state of the OS window, not of a widget."""
        calls = []
        window = session.page.window
        window.visible = False
        window.on_event = lambda e: calls.append(e)
        _mount(session)
        await session.dispatch_event(window._i, "event", {"type": "show"})
        assert len(calls) == 1

    def test_controls_in_a_retained_list_follow_their_new_parent(self, session):
        """A list kept across a re-render takes its state from the new parent."""
        field = ft.TextField(value="kept")
        retained = [field]
        old_parent = ft.TabBarView(controls=retained, disabled=False)
        new_parent = ft.TabBarView(controls=retained, disabled=True)
        session.page.controls.append(old_parent)
        _mount(session)
        old_parent._frozen = True
        new_parent._frozen = True
        ObjectPatch.from_diff(
            old_parent, new_parent, control_cls=BaseControl, frozen=True
        )
        assert field.parent is new_parent
        session.apply_patch(field._i, {"value": "forged"})
        assert field.value == "kept"

    @pytest.mark.asyncio
    async def test_retained_child_follows_its_new_parent(self, session):
        """A child kept across a re-render takes its state from the new parent."""
        calls = []
        button = ft.Button("b", on_click=lambda e: calls.append(e))
        old_parent = ft.Container(content=button, visible=False)
        new_parent = ft.Container(content=button, visible=True)
        for parent in (old_parent, new_parent):
            parent._frozen = True
        button._frozen = True
        session.page.controls.append(old_parent)
        _encode(session.get_page_patch())
        patch, _, _ = ObjectPatch.from_diff(
            old_parent, new_parent, control_cls=BaseControl, frozen=True
        )
        assert patch is not None
        assert button.parent is new_parent

    @pytest.mark.asyncio
    async def test_component_visible_does_not_hide_its_body(self, session):
        """`Component.visible` has no effect on the client, so events aren't blocked."""
        calls = []
        button = ft.Button("b", on_click=lambda e: calls.append(e))
        component = ft.Component(fn=lambda: button, visible=False)
        _mount(session, component)
        await session.dispatch_event(button._i, "click", None)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_service_event_ignores_a_hidden_page(self, session):
        """A service renders nothing, so hiding the page doesn't stop its events."""

        @ft.control("Sensor")
        class Sensor(ft.Service):
            on_change: Optional[ft.ControlEventHandler["Sensor"]] = None

        calls = []
        sensor = Sensor(on_change=lambda e: calls.append(e))
        session.page.visible = False
        session.page._services.register_service(sensor)
        _mount(session)
        await session.dispatch_event(sensor._i, "change", None)
        assert len(calls) == 1

    @pytest.mark.asyncio
    async def test_event_of_a_visible_enabled_control_is_dispatched(self, session):
        """An ordinary click runs its handler."""
        calls = []
        button = ft.Button("b", on_click=lambda e: calls.append(e))
        _mount(session, button)
        await session.dispatch_event(button._i, "click", None)
        assert len(calls) == 1

    @pytest.mark.parametrize("name", [["click"], None, 5])
    @pytest.mark.asyncio
    async def test_non_string_event_name_is_ignored(self, session, name):
        """A malformed event name is dropped without raising."""
        button = ft.Button("b")
        _mount(session, button)
        await session.dispatch_event(button._i, name, None)

    @pytest.mark.asyncio
    async def test_event_data_cannot_replace_control_and_name(self, session):
        """The payload of an event can't change which control and event it reports."""
        calls = []
        page = session.page
        page.on_route_change = lambda e: calls.append((e.control, e.name, e.route))
        await session.dispatch_event(
            page._i,
            "route_change",
            {"route": "/x", "control": "forged", "name": "forged"},
        )
        assert calls == [(page, "route_change", "/x")]

    @pytest.mark.asyncio
    async def test_view_pop_payload_cannot_supply_the_view(self, session):
        """`ViewPopEvent.view` holds a view of the page, never one from the payload."""
        calls = []
        page = session.page
        page.on_view_pop = lambda e: calls.append(e.view)
        await session.dispatch_event(
            page._i, "view_pop", {"route": "/nowhere", "view": {"route": "/forged"}}
        )
        assert calls == [None]

    @pytest.mark.asyncio
    async def test_drag_source_must_be_a_draggable(self, session):
        """A drag event resolves `src` only to a `Draggable`, otherwise to `None`."""
        secret = ft.TextField(data={"api_key": "secret"})
        draggable = ft.Draggable(content=ft.Text("d"))
        calls = []
        target = ft.DragTarget(
            content=ft.Text("t"), on_accept=lambda e: calls.append(e)
        )
        _mount(session, secret, draggable, target)

        data = {"l": {"x": 0, "y": 0}, "g": {"x": 0, "y": 0}}
        await session.dispatch_event(
            target._i, "accept", {**data, "src_id": draggable._i}
        )
        await session.dispatch_event(target._i, "accept", {**data, "src_id": secret._i})
        await session.dispatch_event(target._i, "accept", {**data, "src_id": None})

        assert calls[0].src is draggable
        assert calls[1].src is None
        assert calls[2].src is None

    @pytest.mark.asyncio
    async def test_accepted_drop_must_come_from_the_same_group(self, session):
        """An accepted drop resolves `src` only within the target's group."""
        other = ft.Draggable(content=ft.Text("d"), group="admin")
        calls = []
        target = ft.DragTarget(
            content=ft.Text("t"), group="user", on_accept=lambda e: calls.append(e)
        )
        _mount(session, other, target)

        position = {"x": 0, "y": 0}
        await session.dispatch_event(
            target._i, "accept", {"src_id": other._i, "l": position, "g": position}
        )

        assert calls[0].src is None

    @pytest.mark.asyncio
    async def test_will_accept_reports_a_source_of_another_group(self, session):
        """The client reports a source of another group, which it can't accept."""
        other = ft.Draggable(content=ft.Text("d"), group="admin")
        calls = []
        target = ft.DragTarget(
            content=ft.Text("t"), group="user", on_will_accept=lambda e: calls.append(e)
        )
        _mount(session, other, target)

        await session.dispatch_event(
            target._i, "will_accept", {"src_id": other._i, "accept": False}
        )

        assert calls[0].src is other

    @pytest.mark.asyncio
    async def test_context_menu_item_must_belong_to_the_menu(self, session):
        """A context menu event resolves `item` only among the items of that menu."""
        secret = ft.TextField(data={"api_key": "secret"})
        item = ft.PopupMenuItem(content="item")
        foreign = ft.PopupMenuItem(content="foreign")
        calls = []
        menu = ft.ContextMenu(
            content=ft.Text("m"),
            items=[item],
            on_select=lambda e: calls.append(e.item),
        )
        other_menu = ft.ContextMenu(content=ft.Text("o"), items=[foreign])
        _mount(session, secret, menu, other_menu)

        position = {"x": 0, "y": 0}
        for item_id in (item._i, foreign._i, secret._i):
            await session.dispatch_event(
                menu._i, "select", {"id": item_id, "g": position, "l": position}
            )

        assert calls == [item, None, None]


class TestControlDeclarations:
    def test_custom_control_with_a_declaration_receives_values(self, session):
        """A control lists what its Dart code sends with `client_writable`."""

        @ft.control("Rating", client_writable=("stars",))
        class Rating(ft.LayoutControl):
            stars: int = 0
            secret: str = "kept"

        rating = Rating()
        _mount(session, rating)
        session.apply_patch(rating._i, {"stars": 4, "secret": "forged"})
        assert rating.stars == 4
        assert rating.secret == "kept"

    def test_undeclared_custom_control_warns_once(self, session, caplog):
        """A dropped value of an undeclared field tells the developer how to fix it."""

        @ft.control("Terminal")
        class Terminal(ft.LayoutControl):
            ctrl_active: bool = False

        terminal = Terminal()
        _mount(session, terminal)
        with caplog.at_level(logging.WARNING, logger="flet"):
            session.apply_patch(terminal._i, {"ctrl_active": True})
            session.apply_patch(terminal._i, {"ctrl_active": True})
        assert terminal.ctrl_active is False
        assert len(caplog.records) == 1
        assert "client_writable" in caplog.text
        assert "Terminal.ctrl_active" in caplog.text

    def test_unknown_names_are_never_logged(self, session, caplog):
        """A client can't make the server log names it made up, or grow its memory."""
        before = len(_warned_client_fields)
        text = ft.Text("x")
        _mount(session, text)
        with caplog.at_level(logging.WARNING, logger="flet"):
            session.apply_patch(text._i, {f"made_up_{i}": 1 for i in range(100)})
            session.apply_patch(text._i, {b"bytes-key": 1})
        assert caplog.records == []
        assert len(_warned_client_fields) == before

    def test_subclass_inherits_and_extends_the_declaration(self):
        """A subclass keeps the fields of its parent and can add its own."""

        @ft.control("CodeField", client_writable=("language",))
        class CodeField(ft.TextField):
            language: str = "python"

        @ft.control()
        class PlainSubclass(CodeField):
            label_extra: str = "x"

        assert CodeField._client_writable == {"language", "selection", "value"}
        assert PlainSubclass._client_writable == CodeField._client_writable

    def test_python_only_composite_control_has_no_writable_fields(self):
        """A field added by a Python-only control isn't writable by a client."""

        @ft.control()
        class AdminPanel(ft.Column):
            is_admin: bool = False

        assert AdminPanel._client_writable == frozenset()

    def test_unknown_client_writable_name_raises(self):
        """A typo in `client_writable` fails when the class is declared."""
        with pytest.raises(ValueError, match="client_writable"):

            @ft.control("Bad", client_writable=("missing",))
            class Bad(ft.LayoutControl):
                pass

    def test_unknown_enabled_only_name_raises(self):
        """A typo in `enabled_only` fails when the class is declared."""
        with pytest.raises(ValueError, match="enabled_only"):

            @ft.control("Bad", enabled_only=("missing",))
            class Bad(ft.LayoutControl):
                pass

    def test_enabled_only_of_a_custom_control_is_applied(self, session):
        """A control lists what its Dart code holds back while disabled."""
        calls = []

        @ft.control(
            "Rating",
            client_writable=("stars",),
            enabled_only=("stars", "rate"),
        )
        class Rating(ft.LayoutControl):
            stars: int = 0
            on_rate: Optional[ft.ControlEventHandler["Rating"]] = None

        rating = Rating(disabled=True, on_rate=lambda e: calls.append(e))
        _mount(session, rating)
        session.apply_patch(rating._i, {"stars": 4})
        assert rating.stars == 0

    def test_undeclared_control_is_not_gated_on_disabled(self, session):
        """A control that lists nothing keeps its values and events while disabled."""

        @ft.control("Meter", client_writable=("level",))
        class Meter(ft.LayoutControl):
            level: int = 0

        meter = Meter(disabled=True)
        _mount(session, meter)
        session.apply_patch(meter._i, {"level": 4})
        assert meter.level == 4

    def test_unknown_server_event_raises(self):
        """A typo in `server_events` fails when the class is declared."""
        with pytest.raises(ValueError, match="server_events"):

            @ft.control("Bad", server_events=("missing",))
            class Bad(ft.LayoutControl):
                pass
