import asyncio
import random
from dataclasses import dataclass, field

import flet as ft
import flet_charts as ft_charts

MAX_POINTS = 20


@dataclass
class DataPoint:
    x: float
    y: float


@dataclass
@ft.observable
class ChartData:
    x: float = 0.0
    min_y: float = 0.0
    max_y: float = 1.0
    points: list[DataPoint] = field(default_factory=list)

    def __post_init__(self):
        for _ in range(MAX_POINTS):
            self.add_point()

    def add_point(self):
        self.points.append(
            DataPoint(x=self.x, y=random.uniform(self.min_y, self.max_y))
        )
        self.x += 0.5
        if len(self.points) > MAX_POINTS:
            self.points.pop(0)


@ft.component
def Gauge(
    min_y: float = 0.0,
    max_y: float = 1.0,
    width: int = 200,
    height: int = 150,
    line_color=ft.Colors.BLUE,
    bgcolor=ft.Colors.BLUE_100,
):
    chart_data, _ = ft.use_state(lambda: ChartData(min_y=min_y, max_y=max_y))

    async def generate_chart_data():
        for _ in range(0, 100):
            chart_data.add_point()
            await asyncio.sleep(1.0)

    ft.on_mounted(generate_chart_data)

    return ft_charts.LineChart(
        data_series=[
            ft_charts.LineChartData(
                stroke_width=2,
                color=line_color,
                curved=True,
                points=[
                    ft_charts.LineChartDataPoint(
                        key=point.x,
                        x=point.x,
                        y=point.y,
                        selected_point=ft_charts.ChartCirclePoint(radius=4),
                        selected_below_line=False,
                        tooltip=f"{round(point.y, 2)}%",
                    )
                    for point in chart_data.points
                ],
                below_line_bgcolor=bgcolor,
            )
        ],
        border=ft.Border.all(1, ft.Colors.GREY_400),
        horizontal_grid_lines=ft_charts.ChartGridLines(
            color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3], interval=0.1
        ),
        tooltip=ft_charts.LineChartTooltip(
            bgcolor=ft.Colors.BLACK_12,
            border_radius=4,
            padding=ft.Padding(5),
        ),
        min_y=0,
        max_y=1,
        width=width,
        height=height,
        animation=ft.Animation(duration=0),
    )


@ft.component
def App():
    return ft.Row(
        controls=[
            ft.Column(
                [
                    ft.Text("CPU Usage"),
                    Gauge(
                        min_y=0.3,
                        max_y=1.0,
                        line_color=ft.Colors.BLUE,
                        bgcolor=ft.Colors.BLUE_100,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Text("Memory Usage"),
                    Gauge(
                        min_y=0.2,
                        max_y=0.5,
                        line_color=ft.Colors.GREEN,
                        bgcolor=ft.Colors.GREEN_100,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Column(
                [
                    ft.Text("Disk Usage"),
                    Gauge(
                        min_y=0.7,
                        max_y=0.9,
                        line_color=ft.Colors.ORANGE,
                        bgcolor=ft.Colors.ORANGE_100,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        ]
    )


ft.run(lambda page: page.render(App))
