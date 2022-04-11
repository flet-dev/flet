import flet
from flet import ElevatedButton, Stack, Text
from flet.protocol import Command


def test_text_add():
    c = Text(
        value="Hello,\nworld!",
        markdown=True,
        align="left",
        vertical_align="top",
        size="tiny",
        bold=True,
        italic=False,
        pre=False,
        nowrap=True,
        block=False,
        color="#9FE2BF",
        bgcolor="#FF7F50",
        border_style="dotted",
        border_width="1",
        border_color="yellow",
        border_radius="4px",
    )
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.Text)
    # raise Exception(s.get_cmd_str())
    # assert c.get_cmd_str() == ('text align="left" block="false" bold='true italic="false" nowrap="true" pre="false" size="tiny" value="Hello,\\nworld!" verticalAlign="left"'), "Test failed"
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["text"],
            attrs={
                "align": "left",
                "bgcolor": "#FF7F50",
                "block": "false",
                "bold": "true",
                "bordercolor": "yellow",
                "borderradius": "4px",
                "borderstyle": "dotted",
                "borderwidth": "1",
                "color": "#9FE2BF",
                "italic": "false",
                "markdown": "true",
                "nowrap": "true",
                "pre": "false",
                "size": "tiny",
                "value": "Hello,\nworld!",
                "verticalalign": "top",
            },
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_text_double_quotes():
    c = Text(value='Hello, "world!"')
    # raise Exception(c.get_cmd_str())
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["text"],
            attrs={"value": 'Hello, "world!"'},
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_add_text_inside_stack():
    text = Text(id="txt1", value='Hello, "world!"')
    button = ElevatedButton(text="Super button")
    stack = Stack(id="header", controls=[text, button])

    assert stack.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["stack"],
            attrs={"id": ("header", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["text"],
            attrs={"value": 'Hello, "world!"', "id": ("txt1", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["button"],
            attrs={"text": "Super button"},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
