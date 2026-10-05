import asyncio

import pytest

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    MessageAction,
    configure_encode_object_for_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

encode = configure_encode_object_for_msgpack(BaseControl)


# --- min/max size constraints on every LayoutControl ------------------------


def test_size_constraints_are_encoded_for_the_client():
    encoded = encode(
        ft.Container(min_width=200, max_width=760, min_height=40, max_height=600)
    )
    assert encoded["min_width"] == 200
    assert encoded["max_width"] == 760
    assert encoded["min_height"] == 40
    assert encoded["max_height"] == 600


def test_size_constraints_are_available_on_any_layout_control():
    for control in (ft.Column(), ft.Text("x"), ft.Row(), ft.Button("b")):
        control.max_width = 300
        assert encode(control)["max_width"] == 300


def test_unset_constraints_are_not_sent():
    encoded = encode(ft.Container())
    for name in ("min_width", "max_width", "min_height", "max_height"):
        assert name not in encoded


def test_controls_with_their_own_min_size_skip_the_generic_constraint():
    # ListTile.min_height / NavigationRail.min_width are applied by the
    # controls themselves; the client must not wrap them in a second
    # ConstrainedBox for the same property.
    tile = ft.ListTile(min_height=72)
    assert tile._internals["skip_properties"] == ["min_height"]
    rail = ft.NavigationRail(destinations=[], min_width=80)
    assert rail._internals["skip_properties"] == ["min_width"]


# --- tap target size --------------------------------------------------------


def test_material_tap_target_size_is_exported_with_flutter_names():
    assert ft.MaterialTapTargetSize.PADDED.value == "padded"
    assert ft.MaterialTapTargetSize.SHRINK_WRAP.value == "shrinkWrap"


def test_switch_tap_target_size_is_encoded():
    encoded = encode(
        ft.Switch(material_tap_target_size=ft.MaterialTapTargetSize.SHRINK_WRAP)
    )
    assert encoded["material_tap_target_size"] == ft.MaterialTapTargetSize.SHRINK_WRAP


def test_theme_tap_target_size_field():
    theme = ft.Theme(material_tap_target_size=ft.MaterialTapTargetSize.SHRINK_WRAP)
    assert theme.material_tap_target_size == ft.MaterialTapTargetSize.SHRINK_WRAP


def test_popup_menu_button_border_radius_is_encoded():
    encoded = encode(ft.PopupMenuButton(content=ft.Text("x"), border_radius=8))
    assert encoded["border_radius"] == 8


# --- events for detached controls -------------------------------------------


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


@pytest.mark.asyncio
async def test_event_for_a_removed_control_is_dropped_not_crashed():
    # A client can queue an event (e.g. size_change) for a widget whose control
    # has just been taken off the page while the session still has it indexed.
    # Dispatching it used to crash the session with "Control must be added to
    # the page first".
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    session = Session(conn)
    token = _context_page.set(session.page)
    calls = []
    try:
        box = ft.Container(on_size_change=lambda e: calls.append(e))
        session.page.add(box)
        session.get_page_patch()
        control_id = box._i

        # Detached but still indexed: off the page tree, parent link gone.
        session.page.controls.remove(box)
        box._parent = None

        await session.dispatch_event(control_id, "size_change", {"w": 1, "h": 1})
        await asyncio.sleep(0)

        crashes = [
            m for m in conn.messages if m.action == MessageAction.SESSION_CRASHED
        ]
        assert crashes == []
        assert calls == []
    finally:
        session.close()
        _context_page.reset(token)


# --- FletApp.platform_brightness ---------------------------------------------


def test_flet_app_platform_brightness_is_encoded():
    encoded = encode(ft.FletApp(platform_brightness=ft.Brightness.DARK))
    assert encoded["platform_brightness"] == ft.Brightness.DARK


def test_flet_app_platform_brightness_unset_is_not_sent():
    assert "platform_brightness" not in encode(ft.FletApp())


# --- invoke-method results for removed controls ----------------------------


@pytest.mark.asyncio
async def test_invoke_result_for_a_removed_control_is_delivered_not_raised():
    # An embedded app replaced while its wait_idle() was pending answers for a
    # control the session no longer knows. Raising there killed the
    # connection's receive loop and froze the whole app.
    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    conn.loop = asyncio.get_running_loop()
    session = Session(conn)
    try:
        missing_id = 987654
        call = asyncio.create_task(
            session.invoke_method(missing_id, "wait_idle", {}, timeout=5)
        )
        await asyncio.sleep(0)
        call_id = conn.messages[-1].body.call_id

        session.handle_invoke_method_results(missing_id, call_id, "idle", None)
        assert await call == "idle"

        # A result nobody waits for is dropped quietly.
        session.handle_invoke_method_results(missing_id, "nobody", "x", None)
    finally:
        session.close()
