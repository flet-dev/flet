"""Monthly total and individual expense rows."""

from datetime import date

import theme
from components.category_style import category_color, category_icon
from expenses import date_label, money
from models import Expense
from state import StateContext

import flet as ft


@ft.component
def MonthSummary(total: int, count: int, month: date):
    state = ft.use_context(StateContext)
    return ft.Container(
        bgcolor=ft.Colors.PRIMARY,
        border_radius=theme.Radius.L,
        padding=theme.Space.XL,
        content=ft.Column(
            tight=True,
            spacing=theme.Space.S,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text(
                    month.strftime("%B %Y").upper(),
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_PRIMARY,
                ),
                ft.Text(
                    money(total, state.currency),
                    theme_style=theme.Text.DISPLAY,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.ON_PRIMARY,
                ),
                ft.Text(
                    "Total spent this month"
                    if month == date.today().replace(day=1)
                    else "Total spent",
                    color=ft.Colors.ON_PRIMARY,
                ),
                ft.Divider(color=ft.Colors.with_opacity(0.3, ft.Colors.ON_PRIMARY)),
                ft.Text(
                    f"{count} expense{'s' if count != 1 else ''}",
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_PRIMARY,
                ),
            ],
        ),
    )


@ft.component
def ExpenseRow(expense: Expense):
    page = ft.context.page
    state = ft.use_context(StateContext)
    category = state.category(expense.category)
    color = category_color(category)

    def open_details():
        page.navigate(f"/expenses/{expense.id}")

    return ft.Container(
        on_click=open_details,
        ink=True,
        padding=theme.Space.L,
        border=ft.Border.all(
            theme.LINE_WIDTH, ft.Colors.with_opacity(0.2, ft.Colors.OUTLINE)
        ),
        border_radius=theme.Radius.M,
        content=ft.Row(
            spacing=theme.Space.M,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    padding=theme.Space.M,
                    border_radius=theme.Radius.M,
                    bgcolor=ft.Colors.with_opacity(0.08, color),
                    content=ft.Icon(category_icon(category), color=color),
                ),
                ft.Column(
                    expand=True,
                    tight=True,
                    spacing=theme.Space.XS,
                    controls=[
                        ft.Text(
                            category.name if category else "Category removed",
                            theme_style=theme.Text.TITLE,
                        ),
                        ft.Text(
                            date_label(expense.date),
                            theme_style=theme.Text.LABEL,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        *(
                            [ft.Text(expense.note, theme_style=theme.Text.BODY)]
                            if expense.note
                            else []
                        ),
                    ],
                ),
                ft.Text(
                    money(expense.amount_cents, state.currency),
                    theme_style=theme.Text.TITLE,
                    weight=ft.FontWeight.W_600,
                    text_align=ft.TextAlign.RIGHT,
                ),
            ],
        ),
    )
