import flet
from flet import Button, Panel, Text
from flet.protocol import Command


def test_panel_add():
    p = Panel(
        open=True,
        title="Hello",
        type="small",
        auto_dismiss=True,
        light_dismiss=False,
        width=100,
        blocking=False,
        data="data1",
        controls=[Text(value="Are you sure?")],
        footer=[Button(text="OK"), Button(text="Cancel")],
    )

    assert isinstance(p, flet.Control)
    assert isinstance(p, flet.Panel)
    assert p.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["panel"],
            attrs={
                "autodismiss": "true",
                "blocking": "false",
                "data": "data1",
                "lightdismiss": "false",
                "open": "true",
                "title": "Hello",
                "type": "small",
                "width": "100",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["text"], attrs={"value": "Are you sure?"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["footer"], attrs={}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["button"], attrs={"text": "OK"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["button"], attrs={"text": "Cancel"}, lines=[], commands=[]),
    ], "Test failed"
