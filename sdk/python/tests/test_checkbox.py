import flet
from flet import Checkbox
from flet.protocol import Command


def test_checkbox_add():
    c = Checkbox(label="Do you agree?", value=True, visible=True, box_side="start", data="data1")
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.Checkbox)
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["checkbox"],
            attrs={"boxside": "start", "data": "data1", "label": "Do you agree?", "value": "true", "visible": "true"},
            lines=[],
            commands=[],
        )
    ], "Test failed"
