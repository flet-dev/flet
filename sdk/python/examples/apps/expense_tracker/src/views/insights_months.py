"""Six-month spending bar chart with exact totals."""

from datetime import date
from math import ceil

import theme
from expenses import money
from insights import axis_money
from state import StateContext

import flet as ft
import flet_charts as fc


@ft.component
def MonthlySpending(totals: list[tuple[date, int]]):
    state = ft.use_context(StateContext)
    peak = max(cents for _, cents in totals) / 100
    ceiling = max(1, ceil(peak * 1.15))
    first, last = totals[0][0], totals[-1][0]
    return ft.Container(
        padding=theme.Space.L,
        border_radius=theme.Radius.L,
        border=ft.Border.all(theme.LINE_WIDTH, ft.Colors.OUTLINE),
        content=ft.Column(
            tight=True,
            spacing=theme.Space.L,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Last 6 months", theme_style=theme.Text.TITLE),
                ft.Text(
                    f"{first:%b %Y} – {last:%b %Y} · {state.currency}",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                    theme_style=theme.Text.LABEL,
                ),
                fc.BarChart(
                    height=theme.CHART_HEIGHT,
                    min_y=0,
                    max_y=ceiling,
                    groups=[
                        fc.BarChartGroup(
                            x=index,
                            rods=[
                                fc.BarChartRod(
                                    from_y=0,
                                    to_y=cents / 100,
                                    width=theme.CHART_BAR_WIDTH,
                                    color=ft.Colors.PRIMARY,
                                    border_radius=theme.Radius.S,
                                    tooltip=(
                                        f"{month:%B %Y}: {money(cents, state.currency)}"
                                    ),
                                )
                            ],
                        )
                        for index, (month, cents) in enumerate(totals)
                    ],
                    horizontal_grid_lines=fc.ChartGridLines(
                        interval=ceiling / 2,
                        width=theme.LINE_WIDTH,
                        color=ft.Colors.with_opacity(0.15, ft.Colors.OUTLINE),
                    ),
                    left_axis=fc.ChartAxis(
                        label_size=theme.CHART_AXIS_WIDTH,
                        labels=[
                            fc.ChartAxisLabel(
                                value=value,
                                label=ft.Text(
                                    axis_money(value, state.currency),
                                    theme_style=theme.Text.LABEL,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                            )
                            for value in (0, ceiling / 2, ceiling)
                        ],
                    ),
                    bottom_axis=fc.ChartAxis(
                        label_size=theme.CHART_LABEL_HEIGHT,
                        labels=[
                            fc.ChartAxisLabel(
                                value=index,
                                label=ft.Text(
                                    month.strftime("%b"),
                                    theme_style=theme.Text.LABEL,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                            )
                            for index, (month, _) in enumerate(totals)
                        ],
                    ),
                    top_axis=fc.ChartAxis(show_labels=False),
                    right_axis=fc.ChartAxis(show_labels=False),
                ),
                *[
                    ft.Row(
                        key=month.isoformat(),
                        controls=[
                            ft.Text(month.strftime("%B %Y"), expand=True),
                            ft.Text(
                                money(cents, state.currency), weight=ft.FontWeight.W_600
                            ),
                        ],
                    )
                    for month, cents in totals
                ],
                ft.Text(
                    "Includes the current month so far.",
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
        ),
    )
