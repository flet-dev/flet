"""Confirmed category removal with safe expense reassignment."""

import theme
from components.feedback import run_action, show_message
from models import Category
from state import StateContext

import flet as ft


@ft.component
def CategoryDelete(category: Category, disabled: bool):
    page = ft.context.page
    state = ft.use_context(StateContext)
    confirming, set_confirming = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)
    others = [item for item in state.categories if item.id != category.id]
    replacement, set_replacement = ft.use_state(others[0].id if others else "")
    count = sum(item.category == category.id for item in state.expenses)

    async def remove():
        if deleting:
            return
        set_deleting(True)
        ok, _ = await run_action(
            state.delete_category(category.id, replacement),
            "Couldn't delete the category.",
        )
        set_deleting(False)
        if ok:
            set_confirming(False)
            page.navigate("/settings")
            show_message("Category deleted. Expenses have been kept.")

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Delete “{category.name}”?"),
            content=ft.Column(
                tight=True,
                spacing=theme.Space.L,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    ft.Text(
                        f"{count} expense{'s' if count != 1 else ''} will move to "
                        "the category below. "
                        "Its budget will not change."
                        if count
                        else "No expenses use this category."
                    ),
                    *(
                        [
                            ft.Dropdown(
                                label="Move expenses to",
                                value=replacement,
                                expand=True,
                                disabled=deleting,
                                options=[
                                    ft.DropdownOption(key=item.id, text=item.name)
                                    for item in others
                                ],
                                on_select=lambda e: set_replacement(e.control.value),
                            )
                        ]
                        if count
                        else []
                    ),
                    ft.Text(
                        "The category and its budget will be removed. "
                        "This cannot be undone."
                    ),
                ],
            ),
            actions=[
                ft.TextButton(
                    "Cancel", disabled=deleting, on_click=lambda: set_confirming(False)
                ),
                ft.FilledButton(
                    "Deleting…" if deleting else "Delete category",
                    disabled=deleting,
                    on_click=remove,
                ),
            ],
            on_dismiss=lambda: set_confirming(False),
        )
        if confirming
        else None
    )
    return ft.Column(
        tight=True,
        spacing=theme.Space.S,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.OutlinedButton(
                "Delete category",
                icon=ft.Icons.DELETE_OUTLINE,
                disabled=disabled or deleting or not others,
                on_click=lambda: set_confirming(True),
            ),
            *(
                [
                    ft.Text(
                        "Keep at least one category so you can add expenses.",
                        theme_style=theme.Text.LABEL,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    )
                ]
                if not others
                else []
            ),
        ],
    )
