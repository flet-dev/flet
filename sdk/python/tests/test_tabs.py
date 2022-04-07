import flet
import pytest
from flet import Button, Tab, Tabs, Textbox
from flet.protocol import Command


def test_tabs_add():
    t = Tabs(tabs=[Tab(text="Tab1"), Tab("Tab2"), Tab("Tab3")])

    assert isinstance(t, flet.Control)
    assert isinstance(t, flet.Tabs)
    assert t.get_cmd_str() == [
        Command(indent=0, name=None, values=["tabs"], attrs={"value": "Tab1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["tab"], attrs={"text": "Tab1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["tab"], attrs={"text": "Tab2"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["tab"], attrs={"text": "Tab3"}, lines=[], commands=[]),
    ], "Test failed"


def test_tabs_with_controls_add():
    t = Tabs(
        tabs=[
            Tab(text="Tab1", controls=[Button(text="OK"), Button(text="Cancel")]),
            Tab(
                "Tab2",
                controls=[Textbox(label="Textbox 1"), Textbox(label="Textbox 2")],
            ),
        ]
    )
    assert isinstance(t, flet.Control)
    assert isinstance(t, flet.Tabs)
    assert t.get_cmd_str() == [
        Command(indent=0, name=None, values=["tabs"], attrs={"value": "Tab1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["tab"], attrs={"text": "Tab1"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["button"], attrs={"text": "OK"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["button"], attrs={"text": "Cancel"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["tab"], attrs={"text": "Tab2"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["textbox"], attrs={"label": "Textbox 1"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["textbox"], attrs={"label": "Textbox 2"}, lines=[], commands=[]),
    ], "Test failed"


def test_value__initialized_as_empty():
    t = Tabs()

    assert t.value == ""


def test_value__has_an_initial_value():
    t = Tabs(tabs=[Tab(text="Tab1", controls=[Button(text="OK")])])

    assert t.value == "Tab1"


def test_value__key_is_preferred():
    t = Tabs(tabs=[Tab(text="Tab1", key="first_tab_key", controls=[Button(text="OK")])])

    assert t.value == "first_tab_key"


def test_value__can_be_set_on_initialization():
    t = Tabs(
        value="Tab2",
        tabs=[
            Tab("Tab1", controls=[Button(text="OK")]),
            Tab("Tab2", controls=[Button(text="Not OK")]),
        ],
    )
    assert t.value == "Tab2"


def test_value__emptying_tabs_after_initialization_clears_value_as_well():
    t = Tabs(tabs=[Tab(text="Tab1", controls=[Button(text="OK")])])
    t.tabs = None

    assert t.tabs == []
    assert t.value == ""


def test_value__setting_value_to_empty_only_allowed_when_no_tabs():
    t = Tabs(tabs=[Tab(text="Tab1", controls=[Button(text="OK")])])
    with pytest.raises(AssertionError):
        t.value = ""

    t = Tabs()
    t.value = ""

    assert t.value == ""


def test_value__can_be_set_to_valid_tab_key_only_when_tabs():
    t = Tabs(tabs=[Tab(text="Tab1", key="first_tab_key", controls=[Button(text="OK")])])

    t.value = "Tab1"
    t.value = "first_tab_key"
    with pytest.raises(AssertionError):
        t.value = "Unknown value"
