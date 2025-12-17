import flet_charts as fch

import flet as ft


class State:
    toggled = True


state = State()


def main(page: ft.Page):
    data_1 = [
        fch.LineChartData(
            stroke_width=8,
            color=ft.Colors.LIGHT_GREEN,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 1.5),
                fch.LineChartDataPoint(5, 1.4),
                fch.LineChartDataPoint(7, 3.4),
                fch.LineChartDataPoint(10, 2),
                fch.LineChartDataPoint(12, 2.2),
                fch.LineChartDataPoint(13, 1.8),
            ],
        ),
        fch.LineChartData(
            color=ft.Colors.PINK,
            below_line_bgcolor=ft.Colors.with_opacity(0, ft.Colors.PINK),
            stroke_width=8,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 2.8),
                fch.LineChartDataPoint(7, 1.2),
                fch.LineChartDataPoint(10, 2.8),
                fch.LineChartDataPoint(12, 2.6),
                fch.LineChartDataPoint(13, 3.9),
            ],
        ),
        fch.LineChartData(
            color=ft.Colors.CYAN,
            stroke_width=8,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 2.8),
                fch.LineChartDataPoint(3, 1.9),
                fch.LineChartDataPoint(6, 3),
                fch.LineChartDataPoint(10, 1.3),
                fch.LineChartDataPoint(13, 2.5),
            ],
        ),
    ]

    data_2 = [
        fch.LineChartData(
            stroke_width=4,
            color=ft.Colors.with_opacity(0.5, ft.Colors.LIGHT_GREEN),
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 4),
                fch.LineChartDataPoint(5, 1.8),
                fch.LineChartDataPoint(7, 5),
                fch.LineChartDataPoint(10, 2),
                fch.LineChartDataPoint(12, 2.2),
                fch.LineChartDataPoint(13, 1.8),
            ],
        ),
        fch.LineChartData(
            color=ft.Colors.with_opacity(0.5, ft.Colors.PINK),
            below_line_bgcolor=ft.Colors.with_opacity(0.2, ft.Colors.PINK),
            stroke_width=4,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 1),
                fch.LineChartDataPoint(3, 2.8),
                fch.LineChartDataPoint(7, 1.2),
                fch.LineChartDataPoint(10, 2.8),
                fch.LineChartDataPoint(12, 2.6),
                fch.LineChartDataPoint(13, 3.9),
            ],
        ),
        fch.LineChartData(
            color=ft.Colors.with_opacity(0.5, ft.Colors.CYAN),
            stroke_width=4,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(1, 3.8),
                fch.LineChartDataPoint(3, 1.9),
                fch.LineChartDataPoint(6, 5),
                fch.LineChartDataPoint(10, 3.3),
                fch.LineChartDataPoint(13, 4.5),
            ],
        ),
    ]

    chart = fch.LineChart(
        data_series=data_1,
        border=ft.Border(
            bottom=ft.BorderSide(4, ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE))
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY)
        ),
        min_y=0,
        max_y=4,
        min_x=0,
        max_x=14,
        expand=True,
        right_axis=fch.ChartAxis(show_labels=False),
        left_axis=fch.ChartAxis(
            label_size=40,
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
        ),
        bottom_axis=fch.ChartAxis(
            label_size=32,
            labels=[
                fch.ChartAxisLabel(
                    value=2,
                    label=ft.Container(
                        margin=ft.Margin(top=10),
                        content=ft.Text(
                            value="SEP",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=7,
                    label=ft.Container(
                        margin=ft.Margin(top=10),
                        content=ft.Text(
                            value="OCT",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=12,
                    label=ft.Container(
                        margin=ft.Margin(top=10),
                        content=ft.Text(
                            value="DEC",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                    ),
                ),
            ],
        ),
    )

    def toggle_data(e: ft.Event[ft.IconButton]):
        if state.toggled:
            chart.data_series = data_2
            chart.data_series[2].point = True
            chart.max_y = 6
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.max_y = 4
            chart.interactive = True
        state.toggled = not state.toggled
        chart.update()

    page.add(ft.IconButton(ft.Icons.REFRESH, on_click=toggle_data), chart)


if __name__ == "__main__":
    ft.run(main)
