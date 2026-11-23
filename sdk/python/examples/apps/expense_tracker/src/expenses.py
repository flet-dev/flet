"""Money parsing, validation and monthly expense rules."""

import re
from datetime import date
from decimal import Decimal

from data import CURRENCIES
from models import Category, Expense, ExpenseDraft


def parse_cents(value: str) -> int:
    value = value.strip()
    if not re.fullmatch(r"\d{1,10}(?:\.\d{1,2})?", value):
        raise ValueError("Enter a positive amount with up to 2 decimal places.")
    cents = int(Decimal(value) * 100)
    if cents <= 0:
        raise ValueError("Amount must be greater than zero.")
    return cents


def validate(draft: ExpenseDraft, categories: list[Category]) -> dict[str, str]:
    errors = {}
    try:
        parse_cents(draft.amount)
    except ValueError as exc:
        errors["amount"] = str(exc)
    if not any(category.id == draft.category for category in categories):
        errors["category"] = "Choose a category."
    try:
        date.fromisoformat(draft.date)
    except ValueError:
        errors["date"] = "Choose a valid date."
    return errors


def currency_symbol(currency: str = "USD") -> str:
    return CURRENCIES.get(currency, CURRENCIES["USD"])[1]


def money(cents: int, currency: str = "USD") -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{currency_symbol(currency)}{cents // 100:,}.{cents % 100:02d}"


def date_label(value: str) -> str:
    day = date.fromisoformat(value)
    return f"{day:%b} {day.day}, {day.year}"


def shift_month(month: date, offset: int) -> date:
    index = month.year * 12 + month.month - 1 + offset
    year, month_index = divmod(index, 12)
    return date(year, month_index + 1, 1)


def for_month(items: list[Expense], month: date) -> list[Expense]:
    prefix = month.strftime("%Y-%m")
    return sorted(
        (item for item in items if item.date.startswith(prefix)),
        key=lambda item: (item.date, item.created_at, item.id),
        reverse=True,
    )
