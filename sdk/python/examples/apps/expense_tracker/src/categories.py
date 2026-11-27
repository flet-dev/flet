"""Category defaults, validation and budget parsing."""

from data import COLOR_NAMES, DEFAULT_CATEGORY_STYLES, ICON_NAMES
from expenses import parse_cents
from models import Category, CategoryDraft


def default_categories() -> tuple[Category, ...]:
    return tuple(
        Category(name, name, color, icon)
        for name, color, icon in DEFAULT_CATEGORY_STYLES
    )


def validate_category(
    draft: CategoryDraft, categories: list[Category], category_id=None
) -> dict[str, str]:
    errors = {}
    name = draft.name.strip()
    if not name:
        errors["name"] = "Enter a category name."
    elif len(name) > 40:
        errors["name"] = "Use 40 characters or fewer."
    elif any(
        item.id != category_id and item.name.casefold() == name.casefold()
        for item in categories
    ):
        errors["name"] = "A category with this name already exists."
    if draft.color not in COLOR_NAMES:
        errors["color"] = "Choose a color."
    if draft.icon not in ICON_NAMES:
        errors["icon"] = "Choose an icon."
    if draft.budget.strip():
        try:
            parse_cents(draft.budget)
        except ValueError:
            errors["budget"] = "Enter a budget greater than zero, or leave it blank."
    return errors


def budget_cents(draft: CategoryDraft) -> int | None:
    return parse_cents(draft.budget) if draft.budget.strip() else None
