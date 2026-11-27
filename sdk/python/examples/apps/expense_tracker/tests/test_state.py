from dataclasses import replace
from datetime import date

import pytest
from expenses import money, parse_cents, validate
from insights import category_totals
from models import CategoryDraft, ExpenseDraft
from state import AppState
from storage import SCHEMA_VERSION


async def test_first_start_has_default_categories(state):
    assert state.expenses == []
    assert [c.name for c in state.categories] == [
        "Food",
        "Transport",
        "Bills",
        "Fun",
        "Other",
    ]
    assert state.currency == "USD"


async def test_changes_survive_a_restart(state, storage, photos):
    await state.add_expense(ExpenseDraft("12.50", "Food", "2026-11-10", "Lunch"))
    await state.set_currency("EUR")

    fresh = AppState(storage, photos)
    await fresh.load()
    assert fresh.expenses == state.expenses
    assert fresh.categories == state.categories
    assert fresh.currency == "EUR"


async def test_newer_data_is_not_overwritten(storage, photos):
    storage.prefs.values["expense_tracker.data"] = (
        f'{{"schema_version": {SCHEMA_VERSION + 1}}}'
    )
    state = AppState(storage, photos)
    await state.load()
    assert state.status == "error"


def test_amounts():
    assert parse_cents("12.5") == 1250
    for bad in ("", "0", "-3", "1.234", "abc"):
        with pytest.raises(ValueError):
            parse_cents(bad)
    assert money(123456, "EUR") == "€1,234.56"


async def test_invalid_expense_is_rejected(state):
    draft = ExpenseDraft("", "Nope", "not a date")
    assert set(validate(draft, state.categories)) == {"amount", "category", "date"}
    with pytest.raises(ValueError):
        await state.add_expense(draft)
    assert state.expenses == []


async def test_delete_and_undo(state):
    item = await state.add_expense(ExpenseDraft("8.75", "Fun", "2026-11-11"))
    removed = await state.delete_expense(item.id)
    assert state.expense(item.id) is None

    await state.restore_expense(removed)
    assert state.expense(item.id) == item


async def test_category_budget_and_totals(state):
    await state.save_category(CategoryDraft("Dining", "purple", "food", "10"), "Food")
    await state.add_expense(ExpenseDraft("12.50", "Food", "2026-11-10"))

    dining = state.category("Food")
    assert dining.name == "Dining" and dining.budget_cents == 1000
    totals = category_totals(state.expenses, date(2026, 11, 1), state.categories)
    assert totals["Food"] == 1250  # over budget


async def test_category_names_are_unique(state):
    with pytest.raises(ValueError):
        await state.save_category(CategoryDraft("food"))


async def test_deleting_a_category_moves_its_expenses(state):
    pets = await state.save_category(CategoryDraft("Pets", "orange", "other"))
    item = await state.add_expense(ExpenseDraft("5", pets.id, "2026-11-11"))

    await state.delete_category(pets.id, "Other")
    assert state.category(pets.id) is None
    assert state.expense(item.id).category == "Other"


async def test_the_last_category_stays(state):
    first, *rest = state.categories
    for category in rest:
        await state.delete_category(category.id, first.id)
    with pytest.raises(ValueError):
        await state.delete_category(first.id, None)


async def test_failed_save_rolls_back(state, storage):
    before = (list(state.expenses), list(state.categories))
    storage.prefs.fail = True
    with pytest.raises(OSError):
        await state.save_category(CategoryDraft("Unsaved"))
    assert (state.expenses, state.categories) == before


async def test_undo_after_its_category_was_deleted(state):
    item = await state.add_expense(ExpenseDraft("3", "Fun", "2026-11-11"))
    removed = await state.delete_expense(item.id)
    await state.delete_category("Fun", "Other")

    await state.restore_expense(removed)
    assert state.expense(item.id) == replace(item, category="Food")
