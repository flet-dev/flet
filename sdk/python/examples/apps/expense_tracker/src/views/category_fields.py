"""Category draft fields and a live appearance preview."""

import theme
from components.category_style import ICONS, CategoryBadge
from data import COLOR_NAMES, ICON_NAMES
from expenses import currency_symbol
from models import Category, CategoryDraft

import flet as ft


@ft.component
def CategoryFields(
    draft: CategoryDraft, errors: dict, saving: bool, currency: str, edit
):
    preview = Category(
        "preview", draft.name.strip() or "Your category", draft.color, draft.icon
    )
    return ft.Column(
        spacing=theme.Space.XL,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                controls=[
                    CategoryBadge(preview),
                    ft.Text(preview.name, expand=True, theme_style=theme.Text.TITLE),
                ]
            ),
            ft.TextField(
                label="Category name",
                value=draft.name,
                autofocus=True,
                disabled=saving,
                error=errors.get("name"),
                on_change=lambda e: edit(name=e.control.value),
            ),
            ft.Dropdown(
                label="Color",
                value=draft.color,
                expand=True,
                disabled=saving,
                error_text=errors.get("color"),
                leading_icon=ft.Icon(
                    ft.Icons.CATEGORY, color=theme.CATEGORY_COLORS[draft.color]
                ),
                options=[
                    ft.DropdownOption(
                        key=key,
                        text=name,
                        leading_icon=ft.Icon(
                            ft.Icons.CATEGORY, color=theme.CATEGORY_COLORS[key]
                        ),
                    )
                    for key, name in COLOR_NAMES.items()
                ],
                on_select=lambda e: edit(color=e.control.value),
            ),
            ft.Dropdown(
                label="Icon",
                value=draft.icon,
                expand=True,
                disabled=saving,
                error_text=errors.get("icon"),
                leading_icon=ICONS[draft.icon],
                options=[
                    ft.DropdownOption(key=key, text=name, leading_icon=ICONS[key])
                    for key, name in ICON_NAMES.items()
                ],
                on_select=lambda e: edit(icon=e.control.value),
            ),
            ft.TextField(
                label=f"Monthly budget ({currency}, optional)",
                prefix=ft.Text(currency_symbol(currency)),
                hint_text="Leave blank for no budget",
                value=draft.budget,
                keyboard_type=ft.KeyboardType.NUMBER,
                disabled=saving,
                error=errors.get("budget"),
                on_change=lambda e: edit(budget=e.control.value),
            ),
            ft.Text(
                "This budget repeats each month. "
                "Clear the amount to remove the budget.",
                color=ft.Colors.ON_SURFACE_VARIANT,
                theme_style=theme.Text.LABEL,
            ),
        ],
    )
