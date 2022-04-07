import flet
from flet.dropdown import Option
from flet.protocol import Command


def test_option():
    opt = Option("key1")
    assert isinstance(opt, flet.Control)
    assert isinstance(opt, Option)


def test_dropdown():
    dd = flet.Dropdown(
        id="list1",
        label="Your favorite color:",
        options=[Option(key="key1", text="value1"), Option(key="key2", text="value2")],
    )

    assert isinstance(dd, flet.Control)
    assert isinstance(dd, flet.Dropdown)
    assert dd.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["dropdown"],
            attrs={"label": "Your favorite color:", "id": ("list1", True)},
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["option"], attrs={"key": "key1", "text": "value1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["option"], attrs={"key": "key2", "text": "value2"}, lines=[], commands=[]),
    ], "Test failed"

    do = Option("key1")
    assert isinstance(do, Option)


def test_dropdown_with_just_keys():
    dd = flet.Dropdown(
        id="list1",
        label="Your favorite color:",
        options=[Option(key="key1"), Option(key="key2")],
    )
    assert dd.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["dropdown"],
            attrs={"label": "Your favorite color:", "id": ("list1", True)},
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["option"], attrs={"key": "key1"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["option"], attrs={"key": "key2"}, lines=[], commands=[]),
    ], "Test failed"

    do = Option("key1")
    assert isinstance(do, Option)
