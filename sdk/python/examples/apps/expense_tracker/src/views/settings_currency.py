"""Saved currency choice with no implicit exchange-rate conversion."""

import theme
from components.feedback import run_action
from data import CURRENCIES
from state import StateContext

import flet as ft


@ft.component
def CurrencySetting():
    state = ft.use_context(StateContext)
    saving, set_saving = ft.use_state(False)

    async def choose(e):
        currency = e.control.value
        if saving or currency == state.currency:
            return
        set_saving(True)
        await run_action(
            state.set_currency(currency),
            "Couldn't save the currency. Please try again.",
        )
        set_saving(False)

    return ft.Container(
        padding=theme.Space.L,
        border_radius=theme.Radius.L,
        border=ft.Border.all(theme.LINE_WIDTH, ft.Colors.OUTLINE),
        content=ft.Column(
            tight=True,
            spacing=theme.Space.L,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Text("Currency", theme_style=theme.Text.TITLE),
                ft.Dropdown(
                    label="Display currency",
                    value=state.currency,
                    expand=True,
                    disabled=saving,
                    options=[
                        ft.DropdownOption(key=code, text=f"{code} · {name}")
                        for code, (name, _) in CURRENCIES.items()
                    ],
                    on_select=choose,
                ),
                ft.Text(
                    "Changing currency updates labels for all expenses and budgets. "
                    "It does not convert amounts.",
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
            ],
        ),
    )
