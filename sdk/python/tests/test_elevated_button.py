import flet
from flet import elevated_button
import pytest
from flet import ElevatedButton
from flet.protocol import Command


def test_button_primary_must_be_bool():
    with pytest.raises(Exception):
        ElevatedButton(id="button1", text="My button", primary="1")


def test_button_add():
    b = ElevatedButton(
        id="button1", text="My button", primary=True, data="this is data"
    )
    assert isinstance(b, flet.Control)
    assert isinstance(b, flet.Button)
    assert b.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["button"],
            attrs={
                "data": "this is data",
                "primary": "true",
                "text": "My button",
                "id": ("button1", True),
            },
            lines=[],
            commands=[],
        )
    ], "Test failed"


def test_button_with_all_properties():
    b = ElevatedButton(
        primary=False,
        compound=False,
        action=False,
        toolbar=True,
        split=False,
        text="This is text",
        secondary_text="This is secondary text",
        url="https://google.com",
        new_window=True,
        title="This is title",
        icon="Mail",
        icon_color="red",
        data="data",
        menu_items=[
            elevated_button.MenuItem(
                text="Item1 text",
                secondary_text="Item1 secondary text",
                url="https://google.com",
                new_window=False,
                icon="Mail",
                icon_color="blue",
                icon_only=True,
                split=False,
                divider=False,
                sub_menu_items=[
                    elevated_button.MenuItem("Item1Item1"),
                    elevated_button.MenuItem("Item1Item2"),
                ],
            ),
            elevated_button.MenuItem(text="Item2 text"),
        ],
    )

    assert isinstance(b, flet.Control)
    assert isinstance(b, flet.Button)
    assert b.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["button"],
            attrs={
                "action": "false",
                "compound": "false",
                "data": "data",
                "icon": "Mail",
                "iconcolor": "red",
                "newwindow": "true",
                "primary": "false",
                "secondarytext": "This is secondary text",
                "split": "false",
                "text": "This is text",
                "title": "This is title",
                "toolbar": "true",
                "url": "https://google.com",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["item"],
            attrs={
                "divider": "false",
                "icon": "Mail",
                "iconcolor": "blue",
                "icononly": "true",
                "newwindow": "false",
                "secondarytext": "Item1 secondary text",
                "split": "false",
                "text": "Item1 text",
                "url": "https://google.com",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["item"],
            attrs={"text": "Item1Item1"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["item"],
            attrs={"text": "Item1Item2"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["item"],
            attrs={"text": "Item2 text"},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
