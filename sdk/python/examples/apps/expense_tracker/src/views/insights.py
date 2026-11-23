"""Current-month insights and a six-month spending history."""

from datetime import date

import theme
from components.screen import Screen
from components.states import ErrorState, LoadingState
from insights import category_totals, six_month_totals
from state import StateContext
from views.insights_budgets import BudgetUsage
from views.insights_categories import CategorySpending
from views.insights_months import MonthlySpending

import flet as ft


@ft.component
def InsightsScreen():
    state = ft.use_context(StateContext)
    today = date.today()
    if state.status == "loading":
        body = LoadingState("Loading your insights…")
    elif state.status == "error":
        body = ErrorState(
            "Your saved expenses couldn't be loaded.", on_retry=state.load
        )
    else:
        totals = category_totals(state.expenses, today, state.categories)
        body = ft.ListView(
            expand=True,
            spacing=theme.Space.XL,
            padding=ft.Padding.symmetric(vertical=theme.Space.L),
            controls=[
                ft.Text(today.strftime("%B %Y"), theme_style=theme.Text.TITLE),
                ft.Text(
                    "Your spending, at a glance.", color=ft.Colors.ON_SURFACE_VARIANT
                ),
                BudgetUsage(totals),
                CategorySpending(totals),
                MonthlySpending(six_month_totals(state.expenses, today)),
                ft.Container(height=theme.Space.S),
            ],
        )
    return Screen("Insights", body, tab="/insights")
