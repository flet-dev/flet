import sys
from typing import ForwardRef, get_args, get_origin, get_type_hints

from flet.controls.base_page import PageResizeEvent
from flet.controls.control_event import ControlEvent, Event, get_event_field_type
from flet.controls.core.column import Column
from flet.controls.core.interactive_viewer import (
    InteractiveViewer,
    InteractiveViewerTransform,
)
from flet.controls.events import InteractiveViewerTransformEvent, TapEvent
from flet.controls.material.button import Button
from flet.controls.material.container import Container
from flet.controls.material.reorderable_list_view import (
    OnReorderEvent,
    ReorderableListView,
)
from flet.controls.page import Page
from flet.controls.scrollable_control import OnScrollEvent
from flet.controls.types import PointerDeviceType
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub
from flet.utils.from_dict import from_dict


def test_get_event_field_type():
    btn = Button()
    on_click_type = get_event_field_type(btn, "on_click")
    assert get_origin(on_click_type) is Event
    assert get_args(on_click_type)[0] == ForwardRef("Button")

    c = Container()
    on_tap_down_type = get_event_field_type(c, "on_tap_down")
    assert on_tap_down_type == TapEvent["Container"]
    assert on_tap_down_type != ControlEvent

    col = Column()
    on_scroll_type = get_event_field_type(col, "on_scroll")
    assert on_scroll_type == OnScrollEvent
    assert on_scroll_type != ControlEvent


def test_get_page_event_field_type():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))
    on_resize_type = get_event_field_type(page, "on_resize")
    assert on_resize_type == PageResizeEvent
    assert on_resize_type != ControlEvent


def test_create_event_typed_data():
    c = Container()
    on_tap_down_type = get_event_field_type(c, "on_tap_down")
    assert on_tap_down_type == TapEvent["Container"]

    evt = from_dict(
        on_tap_down_type,
        {
            "control": c,
            "name": "some_event",
            "data": None,
            "k": "mouse",
            "l": {"x": 1, "y": 2},
            "g": {"x": 4, "y": 5},
        },
    )

    assert isinstance(evt, TapEvent)
    assert evt.kind == PointerDeviceType.MOUSE
    assert evt.local_position.x == 1
    assert evt.global_position.y == 5
    assert evt.control == c
    assert evt.name == "some_event"


def test_create_reorder_event():
    c = ReorderableListView()
    on_reorder_type = get_event_field_type(c, "on_reorder")
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
    on_resized_type = get_event_field_type(p, "on_resize")
    assert on_resized_type == PageResizeEvent
    evt = from_dict(
        on_resized_type,
        {
            "control": p,
            "name": "on_resize",
            "data": None,
            "width": 1,
            "height": 2,
        },
    )

    assert isinstance(evt, PageResizeEvent)


def test_page_forward_ref_resolution_uses_base_module():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))

    page_module = sys.modules["flet.controls.page"]
    removed = page_module.__dict__.pop("PageResizeEvent", None)

    try:
        on_resize_type = get_event_field_type(page, "on_resize")
        assert on_resize_type == PageResizeEvent
    finally:
        if removed is not None:
            page_module.PageResizeEvent = removed


def test_interactive_viewer_transform_event():
    viewer = InteractiveViewer(content=Container())
    event_type = get_event_field_type(viewer, "on_transform_changed")
    assert event_type == InteractiveViewerTransformEvent["InteractiveViewer"]

    event = from_dict(
        event_type,
        {
            "control": viewer,
            "name": "transform_changed",
            "data": None,
            "s": 2,
            "tx": 3,
            "ty": 4,
            "tz": 0,
            "m": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 4, 0, 1],
        },
    )

    assert isinstance(event, InteractiveViewerTransformEvent)
    assert event.scale == 2
    assert event.translation_x == 3
    assert event.translation_y == 4
    assert event.matrix[12] == 3
    assert len(event.matrix) == 16


def test_interactive_viewer_transform_from_message():
    transform = InteractiveViewerTransform.from_message(
        {
            "s": 2,
            "tx": 3,
            "ty": 4,
            "tz": 0,
            "m": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 3, 4, 0, 1],
        }
    )

    assert transform.scale == 2.0
    assert isinstance(transform.scale, float)
    assert transform.translation_x == 3.0
    assert transform.matrix[13] == 4.0


def test_get_type_hints_control_event_forward_ref():
    def handler(event: ControlEvent) -> None:
        pass

    hints = get_type_hints(handler, include_extras=True)
    assert hints["event"] == ControlEvent
