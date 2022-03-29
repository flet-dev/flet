import flet
from flet.protocol import Command


def test_textbox_add():
    tb = flet.Textbox(id="txt1", label="Your name:")
    assert isinstance(tb, flet.Control)
    assert isinstance(tb, flet.Textbox)
    assert [
        Command(
            indent="  ",
            name=None,
            values=["textbox"],
            attrs={"label": "Your name:", "id": ("txt1", True)},
            lines=[],
            commands=[],
        )
    ], "Test failed"
