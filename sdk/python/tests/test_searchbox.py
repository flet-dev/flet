import flet
from flet import SearchBox
from flet.protocol import Command


def test_searchbox_add():
    sb = SearchBox(
        value="",
        placeholder="search for something",
        underlined=True,
        icon="icon1",
        icon_color="color1",
        data="data1",
    )
    assert isinstance(sb, flet.Control)
    assert isinstance(sb, flet.SearchBox)
    assert sb.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["searchbox"],
            attrs={
                "data": "data1",
                "icon": "icon1",
                "iconcolor": "color1",
                "onchange": "false",
                "placeholder": "search for something",
                "underlined": "true",
                "value": "",
            },
            lines=[],
            commands=[],
        )
    ], "Test failed"
