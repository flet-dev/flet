import random

import flet as ft
import flet_charts as ftc


class MySpot(ftc.ScatterChartSpot):
    def __init__(
        self,
        x: float,
        y: float,
        radius: float = 8.0,
        color: ft.Colors = None,
        show_tooltip: bool = False,
    ):
        super().__init__(
            x=x,
            y=y,
            radius=radius,
            color=color,
            show_tooltip=show_tooltip,
            selected=y == 43,
        )


flutter_logo_spots = [
    MySpot(20, 14.5),
    MySpot(20, 14.5),
    MySpot(22, 16.5),
    MySpot(24, 18.5),
    MySpot(22, 12.5),
    MySpot(24, 14.5),
    MySpot(26, 16.5),
    MySpot(24, 10.5),
    MySpot(26, 12.5),
    MySpot(28, 14.5),
    MySpot(26, 8.5),
    MySpot(28, 10.5),
    MySpot(30, 12.5),
    MySpot(28, 6.5),
    MySpot(30, 8.5),
    MySpot(32, 10.5),
    MySpot(30, 4.5),
    MySpot(32, 6.5),
    MySpot(34, 8.5),
    MySpot(34, 4.5),
    MySpot(36, 6.5),
    MySpot(38, 4.5),
    #  section 2
    MySpot(20, 14.5),
    MySpot(22, 12.5),
    MySpot(24, 10.5),
    MySpot(22, 16.5),
    MySpot(24, 14.5),
    MySpot(26, 12.5),
    MySpot(24, 18.5),
    MySpot(26, 16.5),
    MySpot(28, 14.5),
    MySpot(26, 20.5),
    MySpot(28, 18.5),
    MySpot(30, 16.5),
    MySpot(28, 22.5),
    MySpot(30, 20.5),
    MySpot(32, 18.5),
    MySpot(30, 24.5),
    MySpot(32, 22.5),
    MySpot(34, 20.5),
    MySpot(34, 24.5),
    MySpot(36, 22.5),
    MySpot(38, 24.5),
    # section 3
    MySpot(10, 25),
    MySpot(12, 23),
    MySpot(14, 21),
    MySpot(12, 27),
    MySpot(14, 25),
    MySpot(16, 23),
    MySpot(14, 29),
    MySpot(16, 27),
    MySpot(18, 25),
    MySpot(16, 31),
    MySpot(18, 29),
    MySpot(20, 27),
    MySpot(18, 33),
    MySpot(20, 31),
    MySpot(22, 29),
    MySpot(20, 35),
    MySpot(22, 33),
    MySpot(24, 31),
    MySpot(22, 37),
    MySpot(24, 35),
    MySpot(26, 33),
    MySpot(24, 39),
    MySpot(26, 37),
    MySpot(28, 35),
    MySpot(26, 41),
    MySpot(28, 39),
    MySpot(30, 37),
    MySpot(28, 43),
    MySpot(30, 41),
    MySpot(32, 39),
    MySpot(30, 45),
    MySpot(32, 43),
    MySpot(34, 41),
    MySpot(34, 45),
    MySpot(36, 43),
    MySpot(38, 45),
]


def get_random_spots():
    """Generates random spots for the scatter chart."""
    return [
        MySpot(
            x=random.uniform(4, 50),
            y=random.uniform(4, 50),
            radius=random.uniform(4, 20),
        )
        for _ in range(len(flutter_logo_spots))
    ]


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_event(e: ftc.ScatterChartEvent):
        if e.type == ftc.ChartEventType.TAP_DOWN:
            e.control.spots = (
                flutter_logo_spots
                if (e.control.spots != flutter_logo_spots)
                else get_random_spots()
            )

    page.add(
        ft.Text(
            "Tap on the chart to toggle between random spots and Flutter logo spots."
        ),
        ftc.ScatterChart(
            expand=True,
            aspect_ratio=1.0,
            min_x=0.0,
            max_x=50.0,
            min_y=0.0,
            max_y=50.0,
            left_axis=ftc.ChartAxis(show_labels=False),
            right_axis=ftc.ChartAxis(show_labels=False),
            top_axis=ftc.ChartAxis(show_labels=False),
            bottom_axis=ftc.ChartAxis(show_labels=False),
            show_tooltips_for_selected_spots_only=False,
            on_event=handle_event,
            animation=ft.Animation(
                duration=ft.Duration(milliseconds=600),
                curve=ft.AnimationCurve.FAST_OUT_SLOWIN,
            ),
            spots=flutter_logo_spots,
        ),
    )


ft.run(main)
