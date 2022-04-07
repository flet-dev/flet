import flet
from flet import Icon
from flet.protocol import Command


def test_icon_add():
    c = Icon(name="Mail", color="#FF7F50", size="tiny")
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.Icon)
    # raise Exception(s.get_cmd_str())
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["icon"],
            attrs={"color": "#FF7F50", "name": "Mail", "size": "tiny"},
            lines=[],
            commands=[],
        )
    ], "Test failed"
