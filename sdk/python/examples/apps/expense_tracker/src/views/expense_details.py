"""Expense details, editing and undoable deletion."""

import theme
from components.category_style import category_icon
from components.feedback import run_action, show_message
from components.receipt_image import ReceiptImage
from components.screen import PrimaryAction, Screen
from components.states import EmptyState, ErrorState, LoadingState
from expenses import date_label, money
from state import StateContext

import flet as ft


@ft.component
def ExpenseDetailsScreen():
    page = ft.context.page
    state = ft.use_context(StateContext)
    expense_id = ft.use_route_params()["id"]
    deleting, set_deleting = ft.use_state(False)
    item = state.expense(expense_id)
    category = state.category(item.category) if item else None

    def edit_expense():
        page.navigate(f"/expenses/{expense_id}/edit")

    async def delete_expense():
        if deleting:
            return
        set_deleting(True)
        ok, removed = await run_action(
            state.delete_expense(expense_id),
            "Couldn't delete the expense. Please try again.",
        )
        set_deleting(False)
        if ok:
            page.navigate("/")

            async def undo():
                restored, _ = await run_action(
                    state.restore_expense(removed),
                    "Couldn't restore the expense. Try Undo again.",
                )
                if restored:
                    show_message("Expense restored")
                else:
                    show_message(
                        "Couldn't restore the expense.", action="Undo", on_action=undo
                    )

            show_message("Expense deleted", action="Undo", on_action=undo)

    if state.status == "loading":
        body = LoadingState()
    elif state.status == "error":
        body = ErrorState("Couldn't load your expenses.", on_retry=state.load)
    elif item is None:
        body = EmptyState(
            ft.Icons.RECEIPT_LONG,
            "Expense not found",
            "This expense may have been deleted.",
        )
    else:
        body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=theme.Space.XL,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(height=theme.Space.S),
                ft.Container(
                    padding=theme.Space.XL,
                    border_radius=theme.Radius.L,
                    bgcolor=ft.Colors.PRIMARY,
                    content=ft.Column(
                        tight=True,
                        spacing=theme.Space.M,
                        controls=[
                            ft.Icon(
                                category_icon(category), color=ft.Colors.ON_PRIMARY
                            ),
                            ft.Text(
                                money(item.amount_cents, state.currency),
                                theme_style=theme.Text.DISPLAY,
                                color=ft.Colors.ON_PRIMARY,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                category.name if category else "Category removed",
                                color=ft.Colors.ON_PRIMARY,
                                theme_style=theme.Text.TITLE,
                            ),
                        ],
                    ),
                ),
                ft.Text(
                    "Date",
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Text(date_label(item.date), theme_style=theme.Text.TITLE),
                ft.Text(
                    "Note",
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Text(item.note or "No note added", selectable=True),
                *(
                    [
                        ft.Text("Receipt", theme_style=theme.Text.TITLE),
                        ReceiptImage(item.receipt_ref),
                    ]
                    if item.receipt_ref
                    else []
                ),
                ft.Divider(),
                ft.OutlinedButton(
                    "Deleting…" if deleting else "Delete expense",
                    icon=ft.Icons.DELETE_OUTLINE,
                    disabled=deleting,
                    on_click=delete_expense,
                ),
                ft.Text(
                    "Deleted expenses can be restored with Undo.",
                    theme_style=theme.Text.LABEL,
                    color=ft.Colors.ON_SURFACE_VARIANT,
                ),
                ft.Container(height=theme.LIST_BOTTOM_SPACE),
            ],
        )
    return Screen(
        "Expense details",
        body,
        primary=PrimaryAction("Edit expense", ft.Icons.EDIT, edit_expense)
        if item and state.status == "ready" and not deleting
        else None,
    )
