import flet
from flet import SplitStack, Stack
from flet.protocol import Command


def test_splitstack_add():
    s = SplitStack(
        horizontal=True,
        gutter_size=10,
        gutter_color="yellow",
        gutter_hover_color="orange",
        gutter_drag_color="blue",
        controls=[Stack(id="left"), Stack(id="center")],
    )
    assert isinstance(s, flet.Control)
    assert isinstance(s, flet.SplitStack)

    assert s.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["splitstack"],
            attrs={
                "guttercolor": "yellow",
                "gutterdragcolor": "blue",
                "gutterhovercolor": "orange",
                "guttersize": "10",
                "horizontal": "true",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["stack"],
            attrs={"id": ("left", True)},
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["stack"],
            attrs={"id": ("center", True)},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
