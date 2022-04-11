import flet
from flet import AlertDialog, ElevatedButton, Text
from flet.protocol import Command


def test_dialog_add():
    d = AlertDialog(
        open=True,
        title="Hello",
        sub_text="sub_text1",
        type="close",
        auto_dismiss=True,
        width=100,
        max_width=200,
        height=100,
        fixed_top=True,
        blocking=False,
        data="data1",
        controls=[Text(value="Are you sure?")],
        footer=[ElevatedButton(text="OK"), ElevatedButton(text="Cancel")],
    )

    assert isinstance(d, flet.Control)
    assert isinstance(d, flet.AlertDialog)
    assert d.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["dialog"],
            attrs={
                "autodismiss": "true",
                "blocking": "false",
                "data": "data1",
                "fixedtop": "true",
                "height": "100",
                "maxwidth": "200",
                "open": "true",
                "subtext": "sub_text1",
                "title": "Hello",
                "type": "close",
                "width": "100",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["text"],
            attrs={"value": "Are you sure?"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2, name=None, values=["footer"], attrs={}, lines=[], commands=[]
        ),
        Command(
            indent=4,
            name=None,
            values=["button"],
            attrs={"text": "OK"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["button"],
            attrs={"text": "Cancel"},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
