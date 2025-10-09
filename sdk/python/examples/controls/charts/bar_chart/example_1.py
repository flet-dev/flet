import flet_charts as fch

import flet as ft


def main(page: ft.Page):
    page.add(
        fch.BarChart(
            expand=True,
            interactive=True,
            max_y=110,
            border=ft.Border.all(1, ft.Colors.GREY_400),
            horizontal_grid_lines=fch.ChartGridLines(
                color=ft.Colors.GREY_300, width=1, dash_pattern=[3, 3]
            ),
            tooltip=fch.BarChartTooltip(
                bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
                border_radius=ft.BorderRadius.all(20),
            ),
            left_axis=fch.ChartAxis(
                label_size=40, title=ft.Text("Fruit supply"), title_size=40
            ),
            right_axis=fch.ChartAxis(show_labels=False),
            bottom_axis=fch.ChartAxis(
                label_size=40,
                labels=[
                    fch.ChartAxisLabel(
                        value=0, label=ft.Container(ft.Text("Apple"), padding=10)
                    ),
                    fch.ChartAxisLabel(
                        value=1, label=ft.Container(ft.Text("Blueberry"), padding=10)
                    ),
                    fch.ChartAxisLabel(
                        value=2, label=ft.Container(ft.Text("Cherry"), padding=10)
                    ),
                    fch.ChartAxisLabel(
                        value=3, label=ft.Container(ft.Text("Orange"), padding=10)
                    ),
                ],
            ),
            groups=[
                fch.BarChartGroup(
                    x=0,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=40,
                            width=40,
                            color=ft.Colors.GREEN,
                            border_radius=0,
                        ),
                    ],
                ),
                fch.BarChartGroup(
                    x=1,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=100,
                            width=40,
                            color=ft.Colors.BLUE,
                            tooltip=fch.BarChartRodTooltip("Blueberry"),
                            border_radius=0,
                        ),
                    ],
                ),
                fch.BarChartGroup(
                    x=2,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=30,
                            width=40,
                            color=ft.Colors.RED,
                            border_radius=0,
                        ),
                    ],
                ),
                fch.BarChartGroup(
                    x=3,
                    rods=[
                        fch.BarChartRod(
                            from_y=0,
                            to_y=60,
                            width=40,
                            color=ft.Colors.ORANGE,
                            tooltip=fch.BarChartRodTooltip("Orange"),
                            border_radius=0,
                        ),
                    ],
                ),
            ],
        )
    )


ft.run(main)
