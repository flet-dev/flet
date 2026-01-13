from gallery.charts.barchart import BarChart
from gallery.charts.candlestickchart import CandlestickChart
from gallery.charts.linechart import LineChart
from gallery.charts.piechart import PieChart
from gallery.charts.radarchart import RadarChart
from gallery.charts.scatterchart import ScatterChart

import flet as ft

charts_map = {
    "BarChart": BarChart,
    "LineChart": LineChart,
    "PieChart": PieChart,
    "CandlestickChart": CandlestickChart,
    "RadarChart": RadarChart,
    "ScatterChart": ScatterChart,
}


@ft.component
def ChartView(chart_type: str, on_click_back: ft.EventHandler) -> ft.Control:
    return ft.Column(
        [
            ft.TextButton(
                "All charts", icon=ft.Icons.ARROW_BACK, on_click=on_click_back
            ),
            charts_map.get(chart_type, lambda: ft.Text("Something went wrong..."))(),
        ]
    )


@ft.component
def App():
    selected_chart, set_selected_chart = ft.use_state(None)

    def on_click_back(e):
        set_selected_chart(None)

    return (
        ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.STACKED_LINE_CHART),
                    title=ft.Text("LineChart"),
                    on_click=lambda e: set_selected_chart("LineChart"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BAR_CHART),
                    title=ft.Text("BarChart"),
                    on_click=lambda e: set_selected_chart("BarChart"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PIE_CHART),
                    title=ft.Text("PieChart"),
                    on_click=lambda e: set_selected_chart("PieChart"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SCATTER_PLOT),
                    title=ft.Text("ScatterChart"),
                    on_click=lambda e: set_selected_chart("ScatterChart"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CANDLESTICK_CHART),
                    title=ft.Text("CandlestickChart"),
                    on_click=lambda e: set_selected_chart("CandlestickChart"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.RADAR),
                    title=ft.Text("RadarChart"),
                    on_click=lambda e: set_selected_chart("RadarChart"),
                ),
            ],
        )
        if selected_chart is None
        else ChartView(selected_chart, on_click_back)
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
