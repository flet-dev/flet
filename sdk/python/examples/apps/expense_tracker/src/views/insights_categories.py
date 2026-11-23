"""Category spending pie chart and readable, currency-aware legend."""

import theme
from components.category_style import category_color
from expenses import money
from state import StateContext

import flet as ft
import flet_charts as fc


@ft.component
def CategorySpending(totals: dict[str, int]):
    state = ft.use_context(StateContext)
    total = sum(totals.values())
    chart = (
        fc.PieChart(
            height=theme.CHART_HEIGHT,
            center_space_radius=0,
            sections_space=theme.Space.XS,
            sections=[
                fc.PieChartSection(
                    value=totals.get(category.id, 0),
                    color=category_color(category),
                    radius=theme.PIE_RADIUS,
                )
                for category in state.categories
                if totals.get(category.id, 0) > 0
            ],
        )
        if total
        else ft.Container(
            height=theme.CHART_HEIGHT,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                tight=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=theme.Space.M,
                controls=[
                    ft.Icon(
                        ft.Icons.PIE_CHART_OUTLINE,
                        size=theme.CHART_AXIS_WIDTH,
                        color=ft.Colors.OUTLINE,
                    ),
                    ft.Text("No spending this month", theme_style=theme.Text.TITLE),
                    ft.Text(
                        "Add an expense to see your category breakdown.",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ],
            ),
        )
    )
    return ft.Container(
        padding=theme.Space.L,
        border_radius=theme.Radius.L,
        border=ft.Border.all(theme.LINE_WIDTH, ft.Colors.OUTLINE),
        content=ft.Column(
            tight=True,
            spacing=theme.Space.L,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Spending by category", theme_style=theme.Text.TITLE),
                ft.Text(
                    money(total, state.currency),
                    theme_style=theme.Text.DISPLAY,
                    weight=ft.FontWeight.BOLD,
                ),
                chart,
                *[
                    CategoryLegendRow(
                        category.id, totals.get(category.id, 0), total, key=category.id
                    )
                    for category in state.categories
                ],
            ],
        ),
    )


@ft.component
def CategoryLegendRow(category_id: str, cents: int, total: int):
    state = ft.use_context(StateContext)
    category = state.category(category_id)
    return ft.Row(
        spacing=theme.Space.M,
        controls=[
            ft.Container(
                width=theme.LEGEND_DOT_SIZE,
                height=theme.LEGEND_DOT_SIZE,
                border_radius=theme.Radius.S,
                bgcolor=category_color(category),
            ),
            ft.Text(category.name, expand=True),
            ft.Text(
                f"{cents / total:.0%}" if total else "0%",
                color=ft.Colors.ON_SURFACE_VARIANT,
            ),
            ft.Text(money(cents, state.currency), weight=ft.FontWeight.W_600),
        ],
    )
