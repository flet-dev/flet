"""Immutable records, form drafts and saved snapshots."""

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Category:
    id: str
    name: str
    color: str = "teal"
    icon: str = "other"
    budget_cents: int | None = None


@dataclass(frozen=True)
class CategoryDraft:
    name: str = ""
    color: str = "teal"
    icon: str = "other"
    budget: str = ""


@dataclass(frozen=True)
class Expense:
    id: str
    amount_cents: int
    category: str  # Category.id (the default categories use their names as ids)
    date: str
    note: str
    created_at: str
    receipt_ref: str | None = None


@dataclass(frozen=True)
class ExpenseDraft:
    amount: str = ""
    category: str = ""
    date: str = field(default_factory=lambda: date.today().isoformat())
    note: str = ""
    receipt_ref: str | None = None
    receipt_data: bytes | None = None


@dataclass(frozen=True)
class SavedData:
    expenses: tuple[Expense, ...]
    categories: tuple[Category, ...]
    currency: str = "USD"
