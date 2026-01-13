from dataclasses import dataclass, field
from typing import Optional

import flet as ft
import flet_charts as fch

name = "PieChart 3"


normal_radius = 100
hover_radius = 110

normal_title_style = ft.TextStyle(
    size=12, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD
)
hover_title_style = ft.TextStyle(
    size=16,
    color=ft.Colors.WHITE,
    weight=ft.FontWeight.BOLD,
    shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK_54),
)
normal_badge_size = 40
hover_badge_size = 50


@dataclass
@ft.observable
class SectionData:
    value: int
    radius: int
    color: ft.ColorValue
    badge_icon: Optional[ft.IconData] = None
    badge_size: int = normal_badge_size
    badge_position: float = 0.98
    hovered: bool = False


@dataclass
class ChartData:
    sections: list[SectionData] = field(default_factory=list)


@ft.component
def PieChartSection(section: SectionData) -> fch.PieChartSection:
    badge = None
    if section.badge_icon:
        s = section.badge_size if not section.hovered else hover_badge_size
        badge = ft.Container(
            ft.Icon(section.badge_icon),
            width=s,
            height=s,
            border=ft.Border.all(1, ft.Colors.BROWN),
            border_radius=s / 2,
            bgcolor=ft.Colors.WHITE,
        )

    return fch.PieChartSection(
        section.value,
        title=f"{section.value}%",
        title_style=hover_title_style if section.hovered else normal_title_style,
        color=section.color,
        radius=section.radius + 10 if section.hovered else section.radius,
        badge=badge,
        badge_position=section.badge_position,
    )


@ft.component
def PieChart():
    chart_data, _ = ft.use_state(
        ChartData(
            sections=[
                SectionData(
                    value=40,
                    radius=normal_radius,
                    color=ft.Colors.BLUE,
                    badge_icon=ft.Icons.AC_UNIT,
                ),
                SectionData(
                    value=30,
                    radius=normal_radius,
                    color=ft.Colors.YELLOW,
                    badge_icon=ft.Icons.ACCESS_ALARM,
                ),
                SectionData(
                    value=15,
                    radius=normal_radius,
                    color=ft.Colors.PURPLE,
                    badge_icon=ft.Icons.APPLE,
                ),
                SectionData(
                    value=15,
                    radius=normal_radius,
                    color=ft.Colors.GREEN,
                    badge_icon=ft.Icons.PEDAL_BIKE,
                ),
            ]
        )
    )

    def on_chart_event(e):
        for idx, section in enumerate(chart_data.sections):
            section.hovered = idx == e.section_index

    chart = fch.PieChart(
        sections=[PieChartSection(section=section) for section in chart_data.sections],
        sections_space=0,
        center_space_radius=0,
        on_event=on_chart_event,
        expand=True,
    )

    return chart
