from flet.core.container import Container, ContainerTapEvent
from flet.core.control_event import ControlEvent
from flet.core.elevated_button import ElevatedButton
from flet.core.event import get_event_field_type


def test_get_event_field_type():
    btn = ElevatedButton()
    on_click_type = get_event_field_type(btn, "on_click")
    assert on_click_type == ControlEvent

    c = Container()
    on_tap_down_type = get_event_field_type(c, "on_tap_down")
    assert on_tap_down_type == ContainerTapEvent
