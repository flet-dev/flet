import flet as ft

LIGHT_SEED_COLOR = ft.Colors.BLUE

MATERIAL_COLORS = [
    ("AMBER", ft.Colors.AMBER),
    ("BLACK", ft.Colors.BLACK),
    ("BLUE", ft.Colors.BLUE),
    ("BLUE_GREY", ft.Colors.BLUE_GREY),
    ("BROWN", ft.Colors.BROWN),
    ("CYAN", ft.Colors.CYAN),
    ("DEEP_ORANGE", ft.Colors.DEEP_ORANGE),
    ("DEEP_PURPLE", ft.Colors.DEEP_PURPLE),
    ("GREEN", ft.Colors.GREEN),
    ("GREY", ft.Colors.GREY),
    ("INDIGO", ft.Colors.INDIGO),
    ("LIGHT_BLUE", ft.Colors.LIGHT_BLUE),
    ("LIGHT_GREEN", ft.Colors.LIGHT_GREEN),
    ("LIME", ft.Colors.LIME),
    ("ORANGE", ft.Colors.ORANGE),
    ("PINK", ft.Colors.PINK),
    ("PURPLE", ft.Colors.PURPLE),
    ("RED", ft.Colors.RED),
    ("TEAL", ft.Colors.TEAL),
    ("TRANSPARENT", ft.Colors.TRANSPARENT),
    ("WHITE", ft.Colors.WHITE),
    ("YELLOW", ft.Colors.YELLOW),
]

COLOR_ROLE_BY_LABEL = {
    "PRIMARY": "primary",
    "ON_PRIMARY": "on_primary",
    "PRIMARY_CONTAINER": "primary_container",
    "ON_PRIMARY_CONTAINER": "on_primary_container",
    "SECONDARY": "secondary",
    "ON_SECONDARY": "on_secondary",
    "SECONDARY_CONTAINER": "secondary_container",
    "ON_SECONDARY_CONTAINER": "on_secondary_container",
    "TERTIARY": "tertiary",
    "ON_TERTIARY": "on_tertiary",
    "TERTIARY_CONTAINER": "tertiary_container",
    "ON_TERTIARY_CONTAINER": "on_tertiary_container",
}

COLOR_ROLE_EXPORT_ORDER = list(dict.fromkeys(COLOR_ROLE_BY_LABEL.values()))
