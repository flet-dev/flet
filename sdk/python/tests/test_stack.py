import flet
from flet import ElevatedButton, Stack, TextField
from flet.protocol import Command


def test_stack_add():
    s = Stack(
        horizontal=True,
        vertical_fill=True,
        horizontal_align="center",
        vertical_align="baseline",
        gap="large",
        wrap=True,
        scroll_x=True,
        scroll_y=True,
        controls=[TextField(id="firstName"), TextField(id="lastName")],
    )
    assert isinstance(s, flet.Control)
    assert isinstance(s, flet.Stack)
    # raise Exception(s.get_cmd_str())
    assert s.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["stack"],
            attrs={
                "gap": "large",
                "horizontal": "true",
                "horizontalalign": "center",
                "scrollx": "true",
                "scrolly": "true",
                "verticalalign": "baseline",
                "verticalfill": "true",
                "wrap": "true",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["textbox"],
            attrs={"id": ("firstName", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["textbox"],
            attrs={"id": ("lastName", True)},
            lines=[],
            commands=[],
        ),
    ], "Test failed"


def test_nested_stacks_add():
    s = Stack(
        controls=[
            TextField(id="firstName"),
            TextField(id="lastName"),
            Stack(
                horizontal=True,
                controls=[
                    ElevatedButton(id="ok", text="OK", primary=True),
                    ElevatedButton(id="cancel", text="Cancel"),
                ],
            ),
        ]
    )
    assert isinstance(s, flet.Control)
    assert isinstance(s, flet.Stack)
    # raise Exception(s.get_cmd_str())
    assert s.get_cmd_str() == [
        Command(indent=0, name=None, values=["stack"], attrs={}, lines=[], commands=[]),
        Command(
            indent=2,
            name=None,
            values=["textbox"],
            attrs={"id": ("firstName", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["textbox"],
            attrs={"id": ("lastName", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["stack"],
            attrs={"horizontal": "true"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["button"],
            attrs={"primary": "true", "text": "OK", "id": ("ok", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["button"],
            attrs={"text": "Cancel", "id": ("cancel", True)},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
