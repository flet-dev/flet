import flet as ft

name = "BarChart 2"


def example():
    class SampleRod(ft.BarChartRod):
        def __init__(self, y: float, hovered: bool = False):
            super().__init__()
            self.hovered = hovered
            self.y = y
            # self.tooltip = f"{self.y}"
            self.width = 22
            self.color = ft.Colors.WHITE
            self.bg_to_y = 20
            self.bg_color = ft.Colors.GREEN_300

        def before_update(self):
            self.to_y = self.y + 0.5 if self.hovered else self.y
            self.color = ft.Colors.YELLOW if self.hovered else ft.Colors.WHITE
            self.border_side = (
                ft.BorderSide(width=1, color=ft.Colors.GREEN_400)
                if self.hovered
                else ft.BorderSide(width=0, color=ft.Colors.WHITE)
            )
            super().before_update()

    def on_chart_event(e: ft.BarChartEvent):
        for group_index, group in enumerate(chart.bar_groups):
            for rod_index, rod in enumerate(group.bar_rods):
                rod.hovered = e.group_index == group_index and e.rod_index == rod_index
        # chart.update()

    chart = ft.BarChart(
        bar_groups=[
            ft.BarChartGroup(
                x=0,
                bar_rods=[SampleRod(5)],
            ),
            ft.BarChartGroup(
                x=1,
                bar_rods=[SampleRod(6.5)],
            ),
            ft.BarChartGroup(
                x=2,
                bar_rods=[SampleRod(15)],
            ),
            ft.BarChartGroup(
                x=3,
                bar_rods=[SampleRod(7.5)],
            ),
            ft.BarChartGroup(
                x=4,
                bar_rods=[SampleRod(9)],
            ),
            ft.BarChartGroup(
                x=5,
                bar_rods=[SampleRod(11.5)],
            ),
            ft.BarChartGroup(
                x=6,
                bar_rods=[SampleRod(6)],
            ),
        ],
        bottom_axis=ft.ChartAxis(
            labels=[
                ft.ChartAxisLabel(value=0, label=ft.Text("M")),
                ft.ChartAxisLabel(value=1, label=ft.Text("T")),
                ft.ChartAxisLabel(value=2, label=ft.Text("W")),
                ft.ChartAxisLabel(value=3, label=ft.Text("T")),
                ft.ChartAxisLabel(value=4, label=ft.Text("F")),
                ft.ChartAxisLabel(value=5, label=ft.Text("S")),
                ft.ChartAxisLabel(value=6, label=ft.Text("S")),
            ],
        ),
        on_chart_event=on_chart_event,
        interactive=True,
    )

    return ft.Container(
        chart,
        bgcolor=ft.Colors.GREEN_200,
        padding=10,
        border_radius=5,
        # expand=True
        width=700,
        height=400,
    )

    # return ft.Container(
    #         chart, bgcolor=ft.Colors.GREEN_200, padding=10, border_radius=5, expand=True
    #     )
