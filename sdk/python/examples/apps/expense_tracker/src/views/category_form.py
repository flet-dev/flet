"""Add or edit a category without changing its stable expense links."""

from dataclasses import replace

import theme
from categories import validate_category
from components.feedback import run_action
from components.screen import Screen
from components.states import EmptyState, ErrorState, LoadingState
from models import CategoryDraft
from state import StateContext
from views.category_delete import CategoryDelete
from views.category_fields import CategoryFields

import flet as ft


@ft.component
def CategoryFormScreen():
    page = ft.context.page
    state = ft.use_context(StateContext)
    category_id = ft.use_route_params().get("id")
    existing = state.category(category_id)
    draft, set_draft = ft.use_state(CategoryDraft)
    submitted, set_submitted = ft.use_state(False)
    saving, set_saving = ft.use_state(False)
    initialized = ft.use_ref(None)
    errors = (
        validate_category(draft, state.categories, category_id) if submitted else {}
    )

    def populate():
        if existing and initialized.current != category_id:
            budget = existing.budget_cents
            set_draft(
                CategoryDraft(
                    existing.name,
                    existing.color,
                    existing.icon,
                    f"{budget // 100}.{budget % 100:02d}" if budget is not None else "",
                )
            )
            initialized.current = category_id

    ft.use_effect(populate, [category_id, existing is not None])

    def edit(**changes):
        set_draft(lambda previous: replace(previous, **changes))

    async def save():
        if saving:
            return
        set_submitted(True)
        if validate_category(draft, state.categories, category_id):
            return
        set_saving(True)
        ok, _ = await run_action(
            state.save_category(draft, category_id), "Couldn't save the category."
        )
        set_saving(False)
        if ok:
            page.navigate("/settings")

    if state.status == "loading":
        body = LoadingState()
    elif state.status == "error":
        body = ErrorState("Couldn't load your categories.", on_retry=state.load)
    elif category_id and existing is None:
        body = EmptyState(
            ft.Icons.CATEGORY,
            "Category not found",
            "This category may have been deleted.",
        )
    else:
        body = ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=theme.Space.XL,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(height=theme.Space.S),
                CategoryFields(draft, errors, saving, state.currency, edit),
                ft.FilledButton(
                    "Saving…" if saving else "Save category",
                    on_click=save,
                    disabled=saving,
                ),
                *(
                    [ft.Divider(), CategoryDelete(existing, disabled=saving)]
                    if existing
                    else []
                ),
                ft.Container(height=theme.Space.XL),
            ],
        )
    return Screen("Edit category" if category_id else "Add category", body, modal=True)
