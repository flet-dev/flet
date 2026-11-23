"""Current-month expense summary and newest-first list."""

import theme
from components.month_picker import MonthPicker
from components.screen import PrimaryAction, Screen
from components.states import EmptyState, ErrorState, LoadingState
from expenses import for_month
from state import StateContext
from views.month_summary import ExpenseRow, MonthSummary

import flet as ft


@ft.component
def HomeScreen():
    page = ft.context.page
    state = ft.use_context(StateContext)
    month = state.selected_month
    items = for_month(state.expenses, month)

    def add_expense():
        page.navigate("/expenses/new")

    if state.status == "loading":
        body = LoadingState("Loading your expenses…")
    elif state.status == "error":
        body = ErrorState(
            "Your saved expenses couldn't be loaded. Please try again.",
            on_retry=state.load,
        )
    else:
        body = ft.Column(
            expand=True,
            spacing=theme.Space.XL,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(height=theme.Space.XS),
                MonthPicker(),
                MonthSummary(
                    sum(item.amount_cents for item in items), len(items), month
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Expenses", theme_style=theme.Text.TITLE),
                        ft.Text(
                            "Newest first",
                            theme_style=theme.Text.LABEL,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                ),
                ft.ListView(
                    expand=True,
                    spacing=theme.Space.M,
                    padding=ft.Padding.only(bottom=theme.LIST_BOTTOM_SPACE),
                    controls=[ExpenseRow(item, key=item.id) for item in items],
                )
                if items
                else EmptyState(
                    ft.Icons.RECEIPT_LONG,
                    "A fresh start",
                    f"No expenses for {month:%B %Y}.\nTap + to add an expense.",
                ),
            ],
        )
    return Screen(
        "Expense Tracker",
        body,
        tab="/",
        primary=PrimaryAction("Add expense", ft.Icons.ADD, add_expense)
        if state.status == "ready"
        else None,
    )
