import flet
from flet import Link, Text
from flet.protocol import Command

"""
def test_button_primary_must_be_bool():
    with pytest.raises(Exception):
        Button(id="button1", text="My button", primary="1")

"""


def test_link_add():
    l = Link(value="search", url="http://google.com", align="left", new_window=True)
    assert isinstance(l, flet.Control)
    assert isinstance(l, flet.Link)
    assert l.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["link"],
            attrs={"align": "left", "newwindow": "true", "url": "http://google.com", "value": "search"},
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_link_with_controls():
    l = Link(
        value="Visit google",
        url="https://google.com",
        pre=True,
        align="right",
        width="100",
        size="large1",
        title="Link title",
        controls=[Text(value="LinkText1"), Text(value="LinkText2")],
    )
    assert isinstance(l, flet.Control)
    assert isinstance(l, flet.Link)
    assert l.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["link"],
            attrs={
                "align": "right",
                "pre": "true",
                "size": "large1",
                "title": "Link title",
                "url": "https://google.com",
                "value": "Visit google",
                "width": "100",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["text"], attrs={"value": "LinkText1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["text"], attrs={"value": "LinkText2"}, lines=[], commands=[]),
    ], "Test failed"
