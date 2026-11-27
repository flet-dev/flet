"""Add and edit expenses using one validated form."""

from dataclasses import replace
from datetime import date

from components.feedback import run_action, show_message
from components.screen import Screen
from components.states import EmptyState, ErrorState, LoadingState
from expenses import validate
from models import ExpenseDraft
from state import StateContext
from views.expense_form_body import ExpenseFormBody

import flet as ft


@ft.component
def ExpenseFormScreen():
    page = ft.context.page
    state = ft.use_context(StateContext)
    expense_id = ft.use_route_params().get("id")
    existing = state.expense(expense_id)
    draft, set_draft = ft.use_state(ExpenseDraft)
    submitted, set_submitted = ft.use_state(False)
    saving, set_saving = ft.use_state(False)
    photo_busy, set_photo_busy = ft.use_state(False)
    picking_date, set_picking_date = ft.use_state(False)
    initialized = ft.use_ref(None)
    errors = validate(draft, state.categories) if submitted else {}

    def populate_draft():
        if existing and initialized.current != expense_id:
            set_draft(
                ExpenseDraft(
                    amount=f"{existing.amount_cents / 100:.2f}",
                    category=existing.category,
                    date=existing.date,
                    note=existing.note,
                    receipt_ref=existing.receipt_ref,
                )
            )
            initialized.current = expense_id
        elif not expense_id and state.categories and initialized.current is None:
            set_draft(
                lambda previous: replace(previous, category=state.categories[0].id)
            )
            initialized.current = "new"

    ft.use_effect(
        populate_draft, [expense_id, existing is not None, bool(state.categories)]
    )

    def edit(**changes):
        set_draft(lambda previous: replace(previous, **changes))

    async def save():
        if saving or photo_busy:
            return
        set_submitted(True)
        if validate(draft, state.categories):
            return
        set_saving(True)
        action = (
            state.update_expense(expense_id, draft)
            if expense_id
            else state.add_expense(draft)
        )
        ok, _ = await run_action(action, "Couldn't save the expense. Please try again.")
        set_saving(False)
        if ok:
            page.navigate(f"/expenses/{expense_id}" if expense_id else "/")
            if not expense_id and draft.date[:7] != state.selected_month.strftime(
                "%Y-%m"
            ):
                show_message(
                    "Saved on your device. This expense is outside the selected month."
                )

    def pick_date(e):
        set_picking_date(False)
        if e.control.value:
            edit(date=e.control.value.astimezone().date().isoformat())

    ft.use_dialog(
        ft.DatePicker(
            value=date.fromisoformat(draft.date),
            first_date=date(1900, 1, 1),
            last_date=date(2200, 12, 31),
            on_change=pick_date,
            on_dismiss=lambda: set_picking_date(False),
        )
        if picking_date
        else None
    )

    if state.status == "loading":
        body = LoadingState()
    elif state.status == "error":
        body = ErrorState("Couldn't load your expenses.", on_retry=state.load)
    elif expense_id and existing is None:
        body = EmptyState(
            ft.Icons.RECEIPT_LONG,
            "Expense not found",
            "This expense may have been deleted.",
        )
    else:
        body = ExpenseFormBody(
            draft,
            errors,
            saving,
            photo_busy,
            bool(expense_id),
            edit,
            save,
            lambda: set_picking_date(True),
            set_photo_busy,
        )
    return Screen("Edit expense" if expense_id else "Add expense", body, modal=True)
