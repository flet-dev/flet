import flet_charts as fch

import flet as ft

NORMAL_RADIUS = 50
HOVER_RADIUS = 60
NORMAL_TITLE_STYLE = ft.TextStyle(
    size=16, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
)
HOVER_TITLE_STYLE = ft.TextStyle(
    size=22,
    color=ft.Colors.WHITE,
    weight=ft.FontWeight.BOLD,
    shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK54),
)


def main(page: ft.Page):
    def on_chart_event(e: fch.PieChartEvent):
        for idx, section in enumerate(chart.sections):
            if idx == e.section_index:
                section.radius = HOVER_RADIUS
                section.title_style = HOVER_TITLE_STYLE
            else:
                section.radius = NORMAL_RADIUS
                section.title_style = NORMAL_TITLE_STYLE
        chart.update()

    chart = fch.PieChart(
        expand=True,
        sections_space=0,
        center_space_radius=40,
        on_event=on_chart_event,
        sections=[
            fch.PieChartSection(
                value=40,
                title="40%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.BLUE,
                radius=NORMAL_RADIUS,
            ),
            fch.PieChartSection(
                value=30,
                title="30%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.YELLOW,
                radius=NORMAL_RADIUS,
            ),
            fch.PieChartSection(
                value=15,
                title="15%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.PURPLE,
                radius=NORMAL_RADIUS,
            ),
            fch.PieChartSection(
                value=15,
                title="15%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.GREEN,
                radius=NORMAL_RADIUS,
            ),
        ],
    )

    page.add(chart)


ft.run(main)
