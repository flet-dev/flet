import flet
from flet import LineChart
from flet.linechart import Data, Point
from flet.protocol import Command


def test_verticalbarchart_add():
    lc = LineChart(
        legend=True,
        tooltips=True,
        stroke_width=4,
        y_min=0,
        y_max=100,
        y_ticks=2,
        y_format="{y}%",
        x_type="number",
        lines=[
            Data(
                color="yellow",
                legend="yellow color",
                points=[Point(x=1, y=100), Point(x=5, y=50)],
            ),
            Data(
                color="green",
                legend="green color",
                points=[Point(x=10, y=20), Point(x=20, y=10)],
            ),
        ],
    )
    assert isinstance(lc, flet.Control)
    assert isinstance(lc, flet.LineChart)
    assert lc.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["linechart"],
            attrs={
                "legend": "true",
                "strokewidth": "4",
                "tooltips": "true",
                "xtype": "number",
                "yformat": "{y}%",
                "ymax": "100",
                "ymin": "0",
                "yticks": "2",
            },
            lines=[],
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["data"],
            attrs={"color": "yellow", "legend": "yellow color"},
            lines=[],
            commands=[],
        ),
        Command(indent=4, name=None, values=["p"], attrs={"x": "1", "y": "100"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["p"], attrs={"x": "5", "y": "50"}, lines=[], commands=[]),
        Command(
            indent=2,
            name=None,
            values=["data"],
            attrs={"color": "green", "legend": "green color"},
            lines=[],
            commands=[],
        ),
        Command(indent=4, name=None, values=["p"], attrs={"x": "10", "y": "20"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["p"], attrs={"x": "20", "y": "10"}, lines=[], commands=[]),
    ], "Test failed"
