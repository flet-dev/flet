"""Pure spending aggregations for the Insights screen."""

from datetime import date

from expenses import currency_symbol, for_month, shift_month
from models import Category, Expense


def category_totals(
    items: list[Expense], month: date, categories: list[Category]
) -> dict[str, int]:
    totals = dict.fromkeys((category.id for category in categories), 0)
    for item in for_month(items, month):
        totals[item.category] = totals.get(item.category, 0) + item.amount_cents
    return totals


def six_month_totals(items: list[Expense], today: date) -> list[tuple[date, int]]:
    current = today.replace(day=1)
    months = [shift_month(current, offset) for offset in range(-5, 1)]
    return [
        (month, sum(item.amount_cents for item in for_month(items, month)))
        for month in months
    ]


def axis_money(amount: float, currency: str = "USD") -> str:
    symbol = currency_symbol(currency)
    if amount >= 1_000_000:
        return f"{symbol}{amount / 1_000_000:.1f}m"
    if amount >= 1_000:
        return f"{symbol}{amount / 1_000:.1f}k"
    return f"{symbol}{amount:g}"
