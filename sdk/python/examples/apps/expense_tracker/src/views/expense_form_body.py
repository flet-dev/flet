"""Scrollable expense form with receipt controls and one save action."""

import theme
from models import ExpenseDraft
from views.expense_fields import ExpenseFields
from views.expense_receipt import ExpenseReceipt

import flet as ft


@ft.component
def ExpenseFormBody(
    draft: ExpenseDraft,
    errors: dict,
    saving: bool,
    photo_busy: bool,
    editing: bool,
    edit,
    save,
    open_calendar,
    on_photo_busy,
):
    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        spacing=theme.Space.XL,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Container(height=theme.Space.XS),
            ExpenseFields(draft, errors, saving, edit, save, open_calendar),
            ExpenseReceipt(draft, saving, edit, on_photo_busy),
            ft.FilledButton(
                "Saving…" if saving else "Save changes" if editing else "Save expense",
                icon=ft.Icons.EDIT if editing else ft.Icons.ADD,
                on_click=save,
                disabled=saving or photo_busy,
            ),
            ft.Text(
                "Saved only on this device. No account needed.",
                theme_style=theme.Text.LABEL,
                color=ft.Colors.ON_SURFACE_VARIANT,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(height=theme.Space.XL),
        ],
    )
