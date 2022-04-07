import flet
from flet import PieChart
from flet.piechart import Point
from flet.protocol import Command


def test_piechart_add():
    pc = PieChart(
        legend=True,
        tooltips=True,
        inner_value=40,
        inner_radius=42,
        width="100%",
        points=[
            Point(value=20, color="yellow", legend="Yellow color", tooltip="20%"),
            Point(value=30, color="green", legend="Green color", tooltip="30%"),
        ],
    )

    assert isinstance(pc, flet.Control)
    assert isinstance(pc, flet.PieChart)
    assert pc.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["piechart"],
            attrs={"innerradius": "42", "innervalue": "40", "legend": "true", "tooltips": "true", "width": "100%"},
            lines=[],
            commands=[],
        ),
        Command(indent=2, name=None, values=["data"], attrs={}, lines=[], commands=[]),
        Command(
            indent=4,
            name=None,
            values=["p"],
            attrs={"color": "yellow", "legend": "Yellow color", "tooltip": "20%", "value": "20"},
            lines=[],
            commands=[],
        ),
        Command(
            indent=4,
            name=None,
            values=["p"],
            attrs={"color": "green", "legend": "Green color", "tooltip": "30%", "value": "30"},
            lines=[],
            commands=[],
        ),
    ], "Test failed"
