import flet
from flet import Slider
from flet.protocol import Command


def test_slider_add():
    s = Slider(
        value=1,
        label="To what extend you agree",
        min=0,
        max=10,
        step=1,
        show_value=True,
        value_format="current_value is {value}",
        vertical=True,
        height=200,
    )
    assert isinstance(s, flet.Control)
    assert isinstance(s, flet.Slider)
    assert s.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["slider"],
            attrs={
                "height": "200",
                "label": "To what extend you agree",
                "max": "10",
                "min": "0",
                "showvalue": "true",
                "step": "1",
                "value": "1",
                "valueformat": "current_value is {value}",
                "vertical": "true",
            },
            lines=[],
            commands=[],
        )
    ], "Test failed"
