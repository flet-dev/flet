import flet_charts as fch

import flet as ft


class CustomRod(fch.BarChartRod):
    def __init__(self, y: float, hovered: bool = False):
        super().__init__()
        self.hovered = hovered
        self.y = y
        self.width = 22
        self.color = ft.Colors.WHITE
        self.bg_to_y = 20
        self.bg_color = ft.Colors.GREEN_300

    def before_update(self):
        super().before_update()
        self.to_y = self.y + 0.5 if self.hovered else self.y
        self.color = ft.Colors.YELLOW if self.hovered else ft.Colors.WHITE
        self.border_side = (
            ft.BorderSide(width=1, color=ft.Colors.RED)
            if self.hovered
            else ft.BorderSide(width=1, color=ft.Colors.BLUE)
        )


def main(page: ft.Page):
    def on_chart_event(e: fch.BarChartEvent):
        if e.type == fch.ChartEventType.POINTER_HOVER:
            for group_index, group in enumerate(chart.groups):
                for rod_index, rod in enumerate(group.rods):
                    rod.hovered = (
                        e.group_index == group_index and e.rod_index == rod_index
                    )
            chart.update()

    chart = fch.BarChart(
        on_event=on_chart_event,
        interactive=True,
        groups=[
            fch.BarChartGroup(x=0, rods=[CustomRod(5)]),
            fch.BarChartGroup(x=1, rods=[CustomRod(6.5)]),
            fch.BarChartGroup(x=2, rods=[CustomRod(15)]),
            fch.BarChartGroup(x=3, rods=[CustomRod(7.5)]),
            fch.BarChartGroup(x=4, rods=[CustomRod(9)]),
            fch.BarChartGroup(x=5, rods=[CustomRod(11.5)]),
            fch.BarChartGroup(x=6, rods=[CustomRod(6)]),
        ],
        bottom_axis=fch.ChartAxis(
            labels=[
                fch.ChartAxisLabel(value=0, label=ft.Text("M", color=ft.Colors.BLUE)),
                fch.ChartAxisLabel(value=1, label=ft.Text("T", color=ft.Colors.YELLOW)),
                fch.ChartAxisLabel(value=2, label=ft.Text("W", color=ft.Colors.BLUE)),
                fch.ChartAxisLabel(value=3, label=ft.Text("T", color=ft.Colors.YELLOW)),
                fch.ChartAxisLabel(value=4, label=ft.Text("F", color=ft.Colors.BLUE)),
                fch.ChartAxisLabel(value=5, label=ft.Text("S", color=ft.Colors.YELLOW)),
                fch.ChartAxisLabel(value=6, label=ft.Text("S", color=ft.Colors.BLUE)),
            ],
        ),
    )

    page.add(
        ft.Container(
            content=chart,
            bgcolor=ft.Colors.GREEN_200,
            padding=10,
            border_radius=5,
            expand=True,
        )
    )


ft.run(main)
