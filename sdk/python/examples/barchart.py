import flet
from flet import Text, BarChart
from flet.barchart import Point


def main(page):

    # Fractions BarChart
    chart1 = BarChart(
        data_mode="fraction",
        width="50%",
        tooltips=True,
        points=[
            Point(
                legend="C:", x=20, y=250, x_tooltip="20%", y_tooltip="20 of 250 GB used"
            ),
            Point(legend="D:", x=50, y=250, x_tooltip="50%"),
            Point(legend="E:", x=30, y=250, x_tooltip="30%"),
        ],
    )

    # Percentage BarChart
    chart2 = BarChart(
        data_mode="percentage",
        width="30%",
        tooltips=True,
        points=[
            Point(legend="/disk1", x=20, y=100, color="green"),
            Point(legend="/disk2", x=50, y=100, color="yellow"),
            Point(legend="/disk3", x=90, y=100, color="red"),
        ],
    )

    page.add(
        Text("Fractions BarChart", size="xLarge"),
        chart1,
        Text("Percentage BarChart", size="xLarge"),
        chart2,
    )


flet.app("python-barchart", target=main)
