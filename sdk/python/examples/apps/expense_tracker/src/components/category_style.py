"""Shared rendering of saved category icons and palette choices."""

import theme
from models import Category

import flet as ft

ICONS = {
    "food": ft.Icons.RESTAURANT,
    "transport": ft.Icons.DIRECTIONS_BUS,
    "bills": ft.Icons.RECEIPT_LONG,
    "fun": ft.Icons.CELEBRATION,
    "other": ft.Icons.CATEGORY,
    "shopping": ft.Icons.SHOPPING_CART,
    "home": ft.Icons.HOME,
    "gift": ft.Icons.CARD_GIFTCARD,
}


def category_icon(category: Category | None):
    return ICONS.get(category.icon if category else "other", ft.Icons.CATEGORY)


def category_color(category: Category | None):
    return theme.CATEGORY_COLORS.get(
        category.color if category else "teal", ft.Colors.PRIMARY
    )


@ft.component
def CategoryBadge(category: Category):
    color = category_color(category)
    return ft.Container(
        padding=theme.Space.M,
        border_radius=theme.Radius.M,
        bgcolor=ft.Colors.with_opacity(0.1, color),
        content=ft.Icon(category_icon(category), color=color),
    )
