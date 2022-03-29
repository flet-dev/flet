import flet
from flet import BarChart
from flet.barchart import Point
from flet.protocol import Command


def test_barchart_add():
    bc = BarChart(
        data_mode="default",
        tooltips=False,
        points=[
            Point(
                x=1,
                y=100,
                legend="legend",
                color="green",
                x_tooltip="x tooltip",
                y_tooltip="y tooltip",
            ),
            Point(x=80, y=200),
            Point(x=100, y=300),
        ],
    )
    assert isinstance(bc, flet.Control)
    assert isinstance(bc, flet.BarChart)
    assert bc.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["barchart"],
            attrs={"datamode": "default", "tooltips": "false"},
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["data"], attrs={}, lines=[], commands=[]),
        Command(
            indent=4,
            name=None,
            values=["p"],
            attrs={
                "color": "green",
                "legend": "legend",
                "x": "1",
                "xtooltip": "x tooltip",
                "y": "100",
                "ytooltip": "y tooltip",
            },
            lines=[],
            commands=[],
        ),
        Command(indent=4, name=None, values=["p"], attrs={"x": "80", "y": "200"}, lines=[], commands=[]),
        Command(indent=4, name=None, values=["p"], attrs={"x": "100", "y": "300"}, lines=[], commands=[]),
    ], "Test failed"
