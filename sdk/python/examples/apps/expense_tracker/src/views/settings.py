"""Currency and category management."""

import theme
from components.category_style import CategoryBadge
from components.screen import PrimaryAction, Screen
from components.states import ErrorState, LoadingState
from expenses import money
from models import Category
from state import StateContext
from views.settings_currency import CurrencySetting

import flet as ft


@ft.component
def CategorySetting(category: Category):
    page = ft.context.page
    state = ft.use_context(StateContext)

    def edit_category():
        page.navigate(f"/settings/categories/{category.id}")

    return ft.ListTile(
        leading=CategoryBadge(category),
        title=ft.Text(category.name),
        subtitle=ft.Text(
            f"Monthly budget: {money(category.budget_cents, state.currency)}"
            if category.budget_cents
            else "No monthly budget"
        ),
        trailing=ft.Icon(ft.Icons.EDIT),
        on_click=edit_category,
        content_padding=theme.Space.S,
    )


@ft.component
def SettingsScreen():
    page = ft.context.page
    state = ft.use_context(StateContext)

    def add_category():
        page.navigate("/settings/categories/new")

    if state.status == "loading":
        body = LoadingState()
    elif state.status == "error":
        body = ErrorState("Couldn't load your settings.", on_retry=state.load)
    else:
        body = ft.ListView(
            expand=True,
            spacing=theme.Space.L,
            padding=ft.Padding.only(top=theme.Space.L, bottom=theme.LIST_BOTTOM_SPACE),
            controls=[
                CurrencySetting(),
                ft.Text("Categories", theme_style=theme.Text.TITLE),
                ft.Text(
                    "Choose a category to edit its name, color, icon or "
                    "monthly budget.",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                *[
                    CategorySetting(category, key=category.id)
                    for category in state.categories
                ],
            ],
        )
    return Screen(
        "Settings",
        body,
        tab="/settings",
        primary=PrimaryAction("Add category", ft.Icons.ADD, add_category)
        if state.status == "ready"
        else None,
    )
