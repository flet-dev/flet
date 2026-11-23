"""Monthly budget progress and explicit over-budget warnings."""

import theme
from components.category_style import category_color, category_icon
from expenses import money
from models import Category
from state import StateContext

import flet as ft


@ft.component
def BudgetProgress(category: Category, spent: int, currency: str):
    budget = category.budget_cents
    ratio = spent / budget
    over = spent > budget
    color = ft.Colors.ERROR if over else category_color(category)
    return ft.Column(
        tight=True,
        spacing=theme.Space.S,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                spacing=theme.Space.S,
                controls=[
                    ft.Icon(category_icon(category), color=category_color(category)),
                    ft.Text(category.name, expand=True, theme_style=theme.Text.TITLE),
                    ft.Text(
                        f"{ratio:.0%} used", color=color, weight=ft.FontWeight.W_600
                    ),
                ],
            ),
            ft.Text(f"{money(spent, currency)} of {money(budget, currency)}"),
            ft.ProgressBar(
                value=min(ratio, 1),
                color=color,
                bgcolor=ft.Colors.with_opacity(0.12, color),
                bar_height=theme.BUDGET_BAR_HEIGHT,
                border_radius=theme.Radius.S,
            ),
            ft.Row(
                spacing=theme.Space.S,
                controls=[
                    *(
                        [ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.ERROR)]
                        if over
                        else []
                    ),
                    ft.Text(
                        f"Over budget by {money(spent - budget, currency)}"
                        if over
                        else "Budget fully used"
                        if spent == budget
                        else f"{money(budget - spent, currency)} remaining",
                        expand=True,
                        color=ft.Colors.ERROR if over else ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ],
            ),
        ],
    )


@ft.component
def BudgetUsage(totals: dict[str, int]):
    page = ft.context.page
    state = ft.use_context(StateContext)
    categories = [category for category in state.categories if category.budget_cents]
    over = sum(
        totals.get(category.id, 0) > category.budget_cents for category in categories
    )

    def open_settings():
        page.navigate("/settings")

    return ft.Container(
        padding=theme.Space.L,
        border_radius=theme.Radius.L,
        border=ft.Border.all(
            theme.LINE_WIDTH, ft.Colors.ERROR if over else ft.Colors.OUTLINE
        ),
        content=ft.Column(
            tight=True,
            spacing=theme.Space.XL,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Monthly budgets", theme_style=theme.Text.TITLE),
                *(
                    [
                        ft.Text(
                            "1 category is over budget."
                            if over == 1
                            else f"{over} categories are over budget.",
                            color=ft.Colors.ERROR,
                            weight=ft.FontWeight.BOLD,
                        )
                    ]
                    if over
                    else []
                ),
                *[
                    BudgetProgress(
                        category,
                        totals.get(category.id, 0),
                        state.currency,
                        key=category.id,
                    )
                    for category in categories
                ],
                *(
                    [
                        ft.Text(
                            "Set optional category budgets in Settings to track "
                            "your monthly limits.",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        )
                    ]
                    if not categories
                    else []
                ),
                ft.TextButton("Manage budgets in Settings", on_click=open_settings),
            ],
        ),
    )
