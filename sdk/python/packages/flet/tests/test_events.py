from typing import ForwardRef, get_args, get_origin

from flet.controls.control_event import ControlEvent, Event
from flet.controls.core.column import Column
from flet.controls.events import TapEvent
from flet.controls.material.container import Container
from flet.controls.material.elevated_button import ElevatedButton
from flet.controls.material.reorderable_list_view import (
    OnReorderEvent,
    ReorderableListView,
)
from flet.controls.page import Page
from flet.controls.page_view import PageResizeEvent
from flet.controls.scrollable_control import OnScrollEvent
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub
from flet.utils.from_dict import from_dict


def test_get_event_field_type():
    btn = ElevatedButton()
    on_click_type = ControlEvent.get_event_field_type(btn, "on_click")
    assert get_origin(on_click_type) is Event
    assert get_args(on_click_type)[0] == ForwardRef("ElevatedButton")

    c = Container()
    on_tap_down_type = ControlEvent.get_event_field_type(c, "on_tap_down")
    assert on_tap_down_type == TapEvent
    assert on_tap_down_type != ControlEvent

    col = Column()
    on_scroll_type = ControlEvent.get_event_field_type(col, "on_scroll")
    assert on_scroll_type == OnScrollEvent
    assert on_scroll_type != ControlEvent


def test_create_event_typed_data():
    c = Container()
    on_tap_down_type = ControlEvent.get_event_field_type(c, "on_tap_down")
    assert on_tap_down_type == TapEvent

    evt = from_dict(
        on_tap_down_type,
        {
            "control": c,
            "name": "some_event",
            "data": None,
            "lx": 1,
            "ly": 2,
            "gx": 4,
            "gy": 5,
        },
    )

    assert isinstance(evt, TapEvent)
    assert evt.local_x == 1
    assert evt.global_y == 5
    assert evt.control == c
    assert evt.name == "some_event"


def test_create_reorder_event():
    c = ReorderableListView()
    on_reorder_type = ControlEvent.get_event_field_type(c, "on_reorder")
    assert on_reorder_type == OnReorderEvent

    evt = from_dict(
        on_reorder_type,
        {
            "control": c,
            "name": "some_event",
            "data": None,
            "old_index": 0,
            "new_index": 1,
        },
    )

    assert isinstance(evt, OnReorderEvent)
    assert evt.old_index == 0
    assert evt.new_index == 1
    assert evt.control == c
    assert evt.name == "some_event"


def test_page_events():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    p = Page(sess=Session(conn))
    on_resized_type = ControlEvent.get_event_field_type(p, "on_resized")
    assert on_resized_type == PageResizeEvent
    evt = from_dict(
        on_resized_type,
        {
            "control": p,
            "name": "on_resized",
            "data": None,
            "width": 1,
            "height": 2,
        },
    )

    assert isinstance(evt, PageResizeEvent)
