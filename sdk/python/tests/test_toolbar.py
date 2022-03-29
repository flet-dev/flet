import flet
from flet import Toolbar, toolbar
from flet.protocol import Command


def test_toolbar_add():
    t = Toolbar(
        inverted=True,
        items=[
            toolbar.Item(
                text="text1",
                secondary_text="text2",
                url="url",
                new_window=True,
                icon="icon",
                icon_color="green",
                icon_only=False,
                split=True,
                divider=True,
            )
        ],
        overflow=[
            toolbar.Item(
                text="text12",
                secondary_text="text22",
                url="url2",
                new_window=True,
                icon="icon",
                icon_color="green",
                icon_only=False,
                split=True,
                divider=True,
            ),
            toolbar.Item(text="overflow"),
        ],
        far=[toolbar.Item(text="far")],
    )

    assert isinstance(t, flet.Control)
    assert isinstance(t, flet.Toolbar)
    assert t.get_cmd_str() == [
        Command(indent=0, name=None, values=["toolbar"], attrs={"inverted": "true"}, lines=[], commands=[]),
        Command(
            indent=2,
            name=None,
            values=["item"],
            attrs={
                "divider": "true",
                "icon": "icon",
                "iconcolor": "green",
                "icononly": "false",
                "newwindow": "true",
                "secondarytext": "text2",
                "split": "true",
                "text": "text1",
                "url": "url",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["overflow"], attrs={}, lines=[], commands=[]),
        Command(
            indent=4,
            name=None,
            values=["item"],
            attrs={
                "divider": "true",
                "icon": "icon",
                "iconcolor": "green",
                "icononly": "false",
                "newwindow": "true",
                "secondarytext": "text22",
                "split": "true",
                "text": "text12",
                "url": "url2",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=4, name=None, values=["item"], attrs={"text": "overflow"}, lines=[], commands=[]),
        Command(indent=2, name=None, values=["far"], attrs={}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["item"], attrs={"text": "far"}, lines=[], commands=[]),
    ], "Test failed"
