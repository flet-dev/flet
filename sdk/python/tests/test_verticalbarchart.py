import flet
from flet import VerticalBarChart
from flet.protocol import Command
from flet.verticalbarchart import Point


def test_verticalbarchart_add():
    vbc = VerticalBarChart(
        legend=True,
        tooltips=False,
        bar_width=56,
        colors="green yellow",
        y_min=0,
        y_max=1000,
        y_ticks=200,
        y_format="format{y}",
        x_type="number",
        points=[
            Point(
                x="1",
                y=100,
                legend="legend",
                color="green",
                x_tooltip="x tooltip",
                y_tooltip="y tooltip",
            ),
            Point(x="80", y=200),
            Point(x="100", y=300),
        ],
    )
    assert isinstance(vbc, flet.Control)
    assert isinstance(vbc, flet.VerticalBarChart)
    assert vbc.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["verticalbarchart"],
            attrs={
                "barwidth": "56",
                "colors": "green yellow",
                "legend": "true",
                "tooltips": "false",
                "xtype": "number",
                "yformat": "format{y}",
                "ymax": "1000",
                "ymin": "0",
                "yticks": "200",
            },
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
