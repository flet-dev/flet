"""Shared ledger state; actions persist one atomic snapshot and roll back on failure."""

import asyncio
import logging
from dataclasses import replace
from datetime import date, datetime, timezone
from uuid import uuid4

from categories import budget_cents, validate_category
from data import CURRENCIES
from expenses import parse_cents, shift_month, validate
from models import Category, CategoryDraft, Expense, ExpenseDraft, SavedData
from storage import Storage

import flet as ft

log = logging.getLogger(f"app.{__name__}")


@ft.observable
class AppState:
    def __init__(self, storage: Storage, photos=None):
        self._storage = storage
        self._photos = photos
        self._lock = asyncio.Lock()
        self.status = "loading"
        self.expenses: list[Expense] = []
        self.categories: list[Category] = []
        self.currency = "USD"
        self.selected_month = date.today().replace(day=1)

    def change_month(self, offset: int):
        self.selected_month = shift_month(self.selected_month, offset)

    def go_to_this_month(self):
        self.selected_month = date.today().replace(day=1)

    def expense(self, expense_id: str | None) -> Expense | None:
        return next((item for item in self.expenses if item.id == expense_id), None)

    def category(self, category_id: str | None) -> Category | None:
        return next((item for item in self.categories if item.id == category_id), None)

    def _snapshot(self) -> SavedData:
        return SavedData(tuple(self.expenses), tuple(self.categories), self.currency)

    def _apply(self, snapshot: SavedData):
        self.expenses = list(snapshot.expenses)
        self.categories = list(snapshot.categories)
        self.currency = snapshot.currency

    async def load(self) -> None:
        self.status = "loading"
        try:
            self._apply(await self._storage.load_data())
            if self._photos:
                try:
                    await self._photos.collect_unused(
                        {item.receipt_ref for item in self.expenses if item.receipt_ref}
                    )
                except Exception:
                    log.warning("Unused receipt cleanup failed", exc_info=True)
            self.status = "ready"
        except Exception:
            log.exception("Loading ledger failed")
            self.status = "error"

    async def _commit(self, transform):
        if self.status != "ready":
            raise ValueError("Wait for your ledger to finish loading.")
        async with self._lock:
            previous = self._snapshot()
            updated = transform(previous)
            self._apply(updated)
            try:
                await self._storage.save_data(updated)
            except Exception:
                self._apply(previous)
                raise

    async def add_expense(self, draft: ExpenseDraft) -> Expense:
        if validate(draft, self.categories):
            raise ValueError("Please check the expense fields.")
        item = Expense(
            id=uuid4().hex,
            amount_cents=parse_cents(draft.amount),
            category=draft.category,
            date=draft.date,
            note=draft.note.strip(),
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return await self._save_expense_photo(item, draft, editing=False)

    async def update_expense(self, expense_id: str, draft: ExpenseDraft) -> Expense:
        if validate(draft, self.categories):
            raise ValueError("Please check the expense fields.")
        existing = self.expense(expense_id)
        if existing is None:
            raise ValueError("This expense no longer exists.")
        updated = replace(
            existing,
            amount_cents=parse_cents(draft.amount),
            category=draft.category,
            date=draft.date,
            note=draft.note.strip(),
        )
        return await self._save_expense_photo(updated, draft, editing=True)

    def can_take_receipt_photo(self) -> bool:
        return bool(self._photos and self._photos.can_take_photo())

    def validate_receipt_photo(self, data: bytes) -> bytes:
        if not self._photos:
            raise ValueError("Receipt photos are unavailable.")
        return self._photos.validate(data)

    async def pick_receipt_photo(self) -> bytes | None:
        if not self._photos:
            raise ValueError("Receipt photos are unavailable.")
        return await self._photos.pick()

    async def load_receipt_photo(self, ref: str) -> bytes | None:
        if not self._photos:
            raise ValueError("Receipt photos are unavailable.")
        return await self._photos.load(ref)

    async def _save_expense_photo(
        self, item: Expense, draft: ExpenseDraft, editing: bool
    ) -> Expense:
        ref = draft.receipt_ref
        new_ref = None
        if draft.receipt_data is not None:
            if not self._photos:
                raise ValueError("Receipt photos are unavailable.")
            new_ref = await self._photos.save(draft.receipt_data)
            ref = new_ref
        saved = replace(item, receipt_ref=ref)
        try:
            await self._commit(
                lambda data: replace(
                    data,
                    expenses=tuple(
                        saved if expense.id == saved.id else expense
                        for expense in data.expenses
                    )
                    if editing
                    else (*data.expenses, saved),
                )
            )
        except Exception:
            if new_ref:
                try:
                    await self._photos.delete(new_ref)
                except Exception:
                    log.warning("Failed attachment cleanup failed", exc_info=True)
            raise
        return saved

    async def delete_expense(self, expense_id: str) -> Expense:
        existing = self.expense(expense_id)
        if existing is None:
            raise ValueError("This expense no longer exists.")
        await self._commit(
            lambda data: replace(
                data,
                expenses=tuple(item for item in data.expenses if item.id != expense_id),
            )
        )
        return existing

    async def restore_expense(self, expense: Expense) -> None:
        def restore(data):
            if any(item.id == expense.id for item in data.expenses):
                return data
            # A category can be removed while the Undo message is still visible.
            category_id = (
                expense.category
                if self.category(expense.category)
                else data.categories[0].id
            )
            return replace(
                data, expenses=(*data.expenses, replace(expense, category=category_id))
            )

        await self._commit(restore)

    async def save_category(
        self, draft: CategoryDraft, category_id: str | None = None
    ) -> Category:
        if validate_category(draft, self.categories, category_id):
            raise ValueError("Please check the category fields.")
        if category_id and self.category(category_id) is None:
            raise ValueError("This category no longer exists.")
        item = Category(
            category_id or uuid4().hex,
            draft.name.strip(),
            draft.color,
            draft.icon,
            budget_cents(draft),
        )
        await self._commit(
            lambda data: replace(
                data,
                categories=tuple(
                    item if category.id == item.id else category
                    for category in data.categories
                )
                if category_id
                else (*data.categories, item),
            )
        )
        return item

    async def delete_category(self, category_id: str, replacement_id: str | None):
        def remove(data):
            remaining = tuple(
                item for item in data.categories if item.id != category_id
            )
            if len(remaining) == len(data.categories):
                raise ValueError("Category not found.")
            if not remaining:
                raise ValueError("Keep at least one category.")
            used = any(item.category == category_id for item in data.expenses)
            if used and not any(item.id == replacement_id for item in remaining):
                raise ValueError("Choose where to move these expenses.")
            expenses = tuple(
                replace(item, category=replacement_id)
                if item.category == category_id
                else item
                for item in data.expenses
            )
            return replace(data, expenses=expenses, categories=remaining)

        await self._commit(remove)

    async def set_currency(self, currency: str):
        if currency not in CURRENCIES:
            raise ValueError("Choose a supported currency.")
        await self._commit(lambda data: replace(data, currency=currency))


StateContext = ft.create_context(None)
