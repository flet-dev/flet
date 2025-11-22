import flet as ft

name = "PieChart 2"


def example():
    normal_radius = 50
    hover_radius = 60
    normal_title_style = ft.TextStyle(
        size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=22,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
    )

    def on_chart_event(e: ft.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = hover_radius
                section.title_style = hover_title_style
            else:
                section.radius = normal_radius
                section.title_style = normal_title_style
        chart.update()

    chart = ft.PieChart(
        sections=[
            ft.PieChartSection(
                40,
                title="40%",
                title_style=normal_title_style,
                color=ft.Colors.BLUE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                30,
                title="30%",
                title_style=normal_title_style,
                color=ft.Colors.YELLOW,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.Colors.PURPLE,
                radius=normal_radius,
            ),
            ft.PieChartSection(
                15,
                title="15%",
                title_style=normal_title_style,
                color=ft.Colors.GREEN,
                radius=normal_radius,
            ),
        ],
        sections_space=0,
        center_space_radius=40,
        on_chart_event=on_chart_event,
        expand=True,
    )

    return chart
