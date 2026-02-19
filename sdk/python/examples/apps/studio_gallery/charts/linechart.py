import flet as ft
import flet_charts as fch


@ft.component
def LineChart():
    toggle, set_toggle = ft.use_state(True)

    data_1 = [
        fch.LineChartData(
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 1.5),
                fch.LineChartDataPoint(5, 1.4),
                fch.LineChartDataPoint(7, 3.4),
                fch.LineChartDataPoint(10, 2),
                fch.LineChartDataPoint(12, 2.2),
                fch.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=8,
            color=ft.Colors.LIGHT_GREEN,
            curved=True,
            rounded_stroke_cap=True,
        ),
        fch.LineChartData(
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 2.8),
                fch.LineChartDataPoint(7, 1.2),
                fch.LineChartDataPoint(10, 2.8),
                fch.LineChartDataPoint(12, 2.6),
                fch.LineChartDataPoint(13, 3.9),
            ],
            color=ft.Colors.PINK,
            below_line_bgcolor=ft.Colors.with_opacity(0, ft.Colors.PINK),
            stroke_width=8,
            curved=True,
            rounded_stroke_cap=True,
        ),
        fch.LineChartData(
            points=[
                fch.LineChartDataPoint(1, 2.8),
                fch.LineChartDataPoint(3, 1.9),
                fch.LineChartDataPoint(6, 3),
                fch.LineChartDataPoint(10, 1.3),
                fch.LineChartDataPoint(13, 2.5),
            ],
            color=ft.Colors.CYAN,
            stroke_width=8,
            curved=True,
            rounded_stroke_cap=True,
        ),
    ]

    data_2 = [
        fch.LineChartData(
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 4),
                fch.LineChartDataPoint(5, 1.8),
                fch.LineChartDataPoint(7, 5),
                fch.LineChartDataPoint(10, 2),
                fch.LineChartDataPoint(12, 2.2),
                fch.LineChartDataPoint(13, 1.8),
            ],
            stroke_width=4,
            color=ft.Colors.with_opacity(0.5, ft.Colors.LIGHT_GREEN),
            rounded_stroke_cap=True,
        ),
        fch.LineChartData(
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 2.8),
                fch.LineChartDataPoint(7, 1.2),
                fch.LineChartDataPoint(10, 2.8),
                fch.LineChartDataPoint(12, 2.6),
                fch.LineChartDataPoint(13, 3.9),
            ],
            color=ft.Colors.with_opacity(0.5, ft.Colors.PINK),
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.PINK),
            stroke_width=4,
            curved=True,
            rounded_stroke_cap=True,
        ),
        fch.LineChartData(
            point=True if not toggle else None,
            points=[
                fch.LineChartDataPoint(1, 3.8),
                fch.LineChartDataPoint(3, 1.9),
                fch.LineChartDataPoint(6, 5),
                fch.LineChartDataPoint(10, 3.3),
                fch.LineChartDataPoint(13, 4.5),
            ],
            color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN),
            stroke_width=4,
            rounded_stroke_cap=True,
        ),
    ]

    chart = fch.LineChart(
        data_series=data_1 if toggle else data_2,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY))
        ),
        left_axis=fch.ChartAxis(
            labels=[
                fch.ChartAxisLabel(
                    value=1,
                    label=ft.Text("1m", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=2,
                    label=ft.Text("2m", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=3,
                    label=ft.Text("3m", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=4,
                    label=ft.Text("4m", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=5,
                    label=ft.Text("5m", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=6,
                    label=ft.Text("6m", size=14, weight=ft.FontWeight.BOLD),
                ),
            ],
            label_size=40,
        ),
        bottom_axis=fch.ChartAxis(
            labels=[
                fch.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        ft.Text(
                            "SEP",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY),
                        ),
                        margin=ft.Margin.only(top=10),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=7,
                    label=ft.Container(
                        ft.Text(
                            "OCT",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY),
                        ),
                        margin=ft.Margin.only(top=10),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=12,
                    label=ft.Container(
                        ft.Text(
                            "DEC",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.PRIMARY),
                        ),
                        margin=ft.Margin.only(top=10),
                    ),
                ),
            ],
            label_size=32,
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY)
        ),
        min_y=0,
        max_y=4 if toggle else 6,
        min_x=0,
        max_x=14,
        interactive=toggle,
        width=700,
        height=500,
    )

    return ft.Column(
        controls=[
            ft.IconButton(ft.Icons.REFRESH, on_click=lambda e: set_toggle(not toggle)),
            chart,
        ]
    )
