"""Shared fields for adding and editing an expense."""

import theme
from components.category_style import category_icon
from expenses import currency_symbol, date_label
from models import ExpenseDraft
from state import StateContext

import flet as ft


@ft.component
def ExpenseFields(
    draft: ExpenseDraft, errors: dict, saving: bool, edit, save, open_calendar
):
    state = ft.use_context(StateContext)
    return ft.Column(
        spacing=theme.Space.XL,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.TextField(
                label=f"Amount ({state.currency})",
                prefix=ft.Text(currency_symbol(state.currency)),
                hint_text="0.00",
                value=draft.amount,
                autofocus=True,
                error=errors.get("amount"),
                keyboard_type=ft.KeyboardType.NUMBER,
                disabled=saving,
                on_change=lambda e: edit(amount=e.control.value),
                on_submit=save,
            ),
            ft.Dropdown(
                label="Category",
                value=draft.category,
                expand=True,
                disabled=saving,
                options=[
                    ft.DropdownOption(
                        key=category.id,
                        text=category.name,
                        leading_icon=category_icon(category),
                    )
                    for category in state.categories
                ],
                error_text=errors.get("category"),
                on_select=lambda e: edit(category=e.control.value),
            ),
            ft.TextField(
                label="Date",
                value=date_label(draft.date),
                read_only=True,
                suffix_icon=ft.Icons.CALENDAR_MONTH,
                disabled=saving,
                error=errors.get("date"),
                on_click=open_calendar,
            ),
            ft.TextField(
                label="Note (optional)",
                hint_text="What was it for?",
                value=draft.note,
                multiline=True,
                min_lines=2,
                max_lines=4,
                disabled=saving,
                on_change=lambda e: edit(note=e.control.value),
            ),
        ],
    )
