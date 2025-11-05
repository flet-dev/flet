import flet as ft
import flet_charts as fch

NORMAL_RADIUS = 100
HOVER_RADIUS = 110
NORMAL_TITLE_STYLE = ft.TextStyle(
    size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
)
HOVER_TITLE_STYLE = ft.TextStyle(
    size=16,
    color=ft.Colors.WHITE,
    weight=ft.FontWeight.BOLD,
    shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK_54),
)
NORMAL_BADGE_SIZE = 40
HOVER_BADGE_SIZE = 50


class SectionBadge(ft.Container):
    def __init__(self, icon: ft.IconData, size: int = NORMAL_BADGE_SIZE):
        super().__init__(
            content=ft.Icon(icon),
            width=size,
            height=size,
            border=ft.Border.all(1, ft.Colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.Colors.WHITE,
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
        sections_space=0,
        center_space_radius=0,
        on_event=on_chart_event,
        expand=True,
        sections=[
            fch.PieChartSection(
                value=40,
                title="40%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.BLUE,
                radius=NORMAL_RADIUS,
                badge=SectionBadge(ft.Icons.AC_UNIT),
                badge_position=0.98,
            ),
            fch.PieChartSection(
                value=30,
                title="30%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.YELLOW,
                radius=NORMAL_RADIUS,
                badge=SectionBadge(ft.Icons.ACCESS_ALARM),
                badge_position=0.98,
            ),
            fch.PieChartSection(
                value=15,
                title="15%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.PURPLE,
                radius=NORMAL_RADIUS,
                badge=SectionBadge(ft.Icons.APPLE),
                badge_position=0.98,
            ),
            fch.PieChartSection(
                value=15,
                title="15%",
                title_style=NORMAL_TITLE_STYLE,
                color=ft.Colors.GREEN,
                radius=NORMAL_RADIUS,
                badge=SectionBadge(ft.Icons.PEDAL_BIKE),
                badge_position=0.98,
            ),
        ],
    )

    page.add(chart)


ft.run(main)
