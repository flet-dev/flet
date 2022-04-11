import flet
from flet import ProgressBar
from flet.protocol import Command


def test_progress_add():
    c = ProgressBar(label="Doing something...", value=10)
    assert isinstance(c, flet.Control)
    assert isinstance(c, flet.Progress)
    # raise Exception(s.get_cmd_str())
    assert c.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["progress"],
            attrs={"label": "Doing something...", "value": "10"},
            lines=[],
            commands=[],
        )
    ], "Test failed"
