import flet as ft
import flet_charts as fch


class State:
    toggled = True


state = State()


def main(page: ft.Page):
    data_1 = [
        fch.LineChartData(
            stroke_width=5,
            color=ft.Colors.CYAN,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(0, 3),
                fch.LineChartDataPoint(2.6, 2),
                fch.LineChartDataPoint(4.9, 5),
                fch.LineChartDataPoint(6.8, 3.1),
                fch.LineChartDataPoint(8, 4),
                fch.LineChartDataPoint(9.5, 3),
                fch.LineChartDataPoint(11, 4),
            ],
        )
    ]

    data_2 = [
        fch.LineChartData(
            stroke_width=5,
            color=ft.Colors.CYAN,
            curved=True,
            rounded_stroke_cap=True,
            points=[
                fch.LineChartDataPoint(0, 3.44),
                fch.LineChartDataPoint(2.6, 3.44),
                fch.LineChartDataPoint(4.9, 3.44),
                fch.LineChartDataPoint(6.8, 3.44),
                fch.LineChartDataPoint(8, 3.44),
                fch.LineChartDataPoint(9.5, 3.44),
                fch.LineChartDataPoint(11, 3.44),
            ],
        )
    ]

    chart = fch.LineChart(
        expand=True,
        data_series=data_1,
        min_y=0,
        max_y=6,
        min_x=0,
        max_x=11,
        border=ft.Border.all(3, ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE)),
        horizontal_grid_lines=fch.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        vertical_grid_lines=fch.ChartGridLines(
            interval=1, color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE), width=1
        ),
        tooltip=fch.LineChartTooltip(
            bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.BLUE_GREY)
        ),
        left_axis=fch.ChartAxis(
            label_size=40,
            labels=[
                fch.ChartAxisLabel(
                    value=1,
                    label=ft.Text("10K", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=3,
                    label=ft.Text("30K", size=14, weight=ft.FontWeight.BOLD),
                ),
                fch.ChartAxisLabel(
                    value=5,
                    label=ft.Text("50K", size=14, weight=ft.FontWeight.BOLD),
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
                            value="MAR",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=5,
                    label=ft.Container(
                        margin=ft.Margin(top=10),
                        content=ft.Text(
                            value="JUN",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.with_opacity(0.5, ft.Colors.ON_SURFACE),
                        ),
                    ),
                ),
                fch.ChartAxisLabel(
                    value=8,
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
            ],
        ),
    )

    def toggle_data(e: ft.Event[ft.ElevatedButton]):
        if state.toggled:
            chart.data_series = data_2
            chart.interactive = False
        else:
            chart.data_series = data_1
            chart.interactive = True
        state.toggled = not state.toggled
        chart.update()

    page.add(ft.Button("avg", on_click=toggle_data), chart)


if __name__ == "__main__":
    ft.run(main)
