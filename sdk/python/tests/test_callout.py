import flet
from flet import Callout, Text
from flet.protocol import Command


def test_callout_add():
    c = Callout(
        target="button1",
        position="leftBottom",
        gap=100,
        beak=True,
        beak_width=10,
        page_padding=10,
        focus=False,
        cover=True,
        visible=True,
        controls=[Text(value="This is callout")],
    )

    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.Callout)
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["callout"],
            attrs={
                "beak": "true",
                "beakwidth": "10",
                "cover": "true",
                "focus": "false",
                "gap": "100",
                "pagepadding": "10",
                "position": "leftBottom",
                "target": "button1",
                "visible": "true",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["text"], attrs={"value": "This is callout"}, lines=[], commands=[]),
    ], "Test failed"
