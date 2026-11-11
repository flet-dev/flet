import math

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from sales import load_monthly_sales

import flet as ft
import flet_charts as fch

INK = "#172B4D"
MUTED = "#718096"
ACCENT = "#168C83"
AVERAGE = "#E18B45"
PAGE_BG = "#F4F7FA"
CARD_BG = "#FFFFFF"
BORDER = "#E5EAF0"


def money(value: float) -> str:
    return f"${value:,.0f}"


def metric_card(label: str, value: str, detail: str, icon: ft.IconData):
    return ft.Container(
        col={"xs": 6, "md": 3},
        padding=14,
        bgcolor=CARD_BG,
        border=ft.Border.all(1, BORDER),
        border_radius=14,
        content=ft.Column(
            spacing=7,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    spacing=4,
                    controls=[
                        ft.Text(label, size=10, color=MUTED),
                        ft.Icon(icon, size=16, color=ACCENT),
                    ],
                ),
                ft.Text(value, size=22, weight=ft.FontWeight.W_700, color=INK),
                ft.Text(detail, size=10, color=MUTED, max_lines=2),
            ],
        ),
    )


def legend_item(color: str, label: str):
    return ft.Row(
        spacing=5,
        controls=[
            ft.Container(width=12, height=3, bgcolor=color),
            ft.Text(label, size=9, color=MUTED),
        ],
    )


def revenue_figure(sales):
    # MatplotlibChart needs a pyplot figure: a bare Figure() has no canvas manager.
    figure, axis = plt.subplots(figsize=(10, 3.6), dpi=110, facecolor=CARD_BG)
    dates = sales["month"].to_numpy()
    revenue = sales["revenue"].to_numpy()
    moving_average = sales["revenue"].rolling(window=3).mean()

    axis.plot(
        dates,
        revenue,
        color=ACCENT,
        linewidth=2.8,
        marker="o",
        markersize=5,
        markerfacecolor=CARD_BG,
        markeredgewidth=2,
    )
    axis.plot(dates, moving_average, color=AVERAGE, linewidth=2, linestyle="--")
    axis.fill_between(dates, revenue, min(revenue) * 0.92, color=ACCENT, alpha=0.10)
    axis.set_ylim(bottom=min(revenue) * 0.92)
    axis.yaxis.set_major_formatter(lambda value, _: f"${value / 1000:.0f}k")
    axis.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    axis.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    axis.grid(axis="y", color=BORDER, linewidth=0.8, linestyle="--")
    axis.set_axisbelow(True)
    axis.tick_params(axis="both", colors=MUTED, labelsize=9, length=0, pad=9)
    for side in ("top", "right", "left", "bottom"):
        axis.spines[side].set_visible(False)
    figure.subplots_adjust(left=0.20, right=0.98, top=0.96, bottom=0.20)
    return figure


def main(page: ft.Page):
    page.title = "Sales Dashboard"
    page.bgcolor = PAGE_BG
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO

    sales = load_monthly_sales()
    first, latest = sales.iloc[0], sales.iloc[-1]
    growth = latest["growth"]
    has_growth = not math.isnan(growth)

    chart_card = ft.Container(
        padding=20,
        bgcolor=CARD_BG,
        border=ft.Border.all(1, BORDER),
        border_radius=14,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Column(
                    spacing=3,
                    controls=[
                        ft.Text(
                            "Revenue over time",
                            size=17,
                            weight=ft.FontWeight.W_600,
                            color=INK,
                        ),
                        ft.Text("Monthly revenue performance", size=11, color=MUTED),
                    ],
                ),
                fch.MatplotlibChart(figure=revenue_figure(sales), height=250),
                ft.Row(
                    spacing=14,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        legend_item(ACCENT, "Monthly revenue"),
                        legend_item(AVERAGE, "3-month average"),
                    ],
                ),
            ],
        ),
    )

    date_range = ft.Container(
        padding=ft.Padding.symmetric(horizontal=10, vertical=7),
        bgcolor=CARD_BG,
        border=ft.Border.all(1, BORDER),
        border_radius=10,
        content=ft.Row(
            spacing=7,
            controls=[
                ft.Icon(ft.Icons.CALENDAR_MONTH, size=15, color=ACCENT),
                ft.Text(
                    f"{first['month']:%b %Y} – {latest['month']:%b %Y}",
                    size=11,
                    color=INK,
                ),
            ],
        ),
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Column(
                        spacing=6,
                        controls=[
                            ft.Text(
                                "Sales overview",
                                size=27,
                                weight=ft.FontWeight.W_700,
                                color=INK,
                            ),
                            ft.Text(
                                "A clear view of your monthly business performance",
                                size=14,
                                color=MUTED,
                                max_lines=2,
                            ),
                            date_range,
                        ],
                    ),
                    chart_card,
                    ft.ResponsiveRow(
                        spacing=12,
                        run_spacing=12,
                        controls=[
                            metric_card(
                                "TOTAL REVENUE",
                                money(sales["revenue"].sum()),
                                "Across all months",
                                ft.Icons.ANALYTICS,
                            ),
                            metric_card(
                                "LATEST MONTH",
                                money(latest["revenue"]),
                                f"{latest['month']:%B %Y}",
                                ft.Icons.CALENDAR_MONTH,
                            ),
                            metric_card(
                                "MONTH-OVER-MONTH",
                                f"{growth:+.1%}" if has_growth else "—",
                                "Compared with previous month"
                                if has_growth
                                else "No prior month available",
                                ft.Icons.TRENDING_UP,
                            ),
                            metric_card(
                                "MONTHLY AVERAGE",
                                money(sales["revenue"].mean()),
                                "Average per month",
                                ft.Icons.SHOW_CHART,
                            ),
                        ],
                    ),
                    ft.Text("Source: monthly_sales.csv", size=11, color=MUTED),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
