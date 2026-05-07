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
    "PRIMARY_FIXED": "primary_fixed",
    "PRIMARY_FIXED_DIM": "primary_fixed_dim",
    "ON_PRIMARY_FIXED": "on_primary_fixed",
    "ON_PRIMARY_FIXED_VARIANT": "on_primary_fixed_variant",
    "SECONDARY": "secondary",
    "ON_SECONDARY": "on_secondary",
    "SECONDARY_CONTAINER": "secondary_container",
    "ON_SECONDARY_CONTAINER": "on_secondary_container",
    "SECONDARY_FIXED": "secondary_fixed",
    "SECONDARY_FIXED_DIM": "secondary_fixed_dim",
    "ON_SECONDARY_FIXED": "on_secondary_fixed",
    "ON_SECONDARY_FIXED_VARIANT": "on_secondary_fixed_variant",
    "TERTIARY": "tertiary",
    "ON_TERTIARY": "on_tertiary",
    "TERTIARY_CONTAINER": "tertiary_container",
    "ON_TERTIARY_CONTAINER": "on_tertiary_container",
    "TERTIARY_FIXED": "tertiary_fixed",
    "TERTIARY_FIXED_DIM": "tertiary_fixed_dim",
    "ON_TERTIARY_FIXED": "on_tertiary_fixed",
    "ON_TERTIARY_FIXED_VARIANT": "on_tertiary_fixed_variant",
    "ERROR": "error",
    "ON_ERROR": "on_error",
    "ERROR_CONTAINER": "error_container",
    "ON_ERROR_CONTAINER": "on_error_container",
    "SURFACE": "surface",
    "ON_SURFACE": "on_surface",
    "ON_SURFACE_VARIANT": "on_surface_variant",
    "SURFACE_TINT": "surface_tint",
    "SURFACE_DIM": "surface_dim",
    "SURFACE_BRIGHT": "surface_bright",
    "SURFACE_CONTAINER": "surface_container",
    "SURFACE_CONTAINER_LOW": "surface_container_low",
    "SURFACE_CONTAINER_LOWEST": "surface_container_lowest",
    "SURFACE_CONTAINER_HIGH": "surface_container_high",
    "SURFACE_CONTAINER_HIGHEST": "surface_container_highest",
    "SCAFFOLD_BGCOLOR": "scaffold_bgcolor",
    "OUTLINE": "outline",
    "OUTLINE_VARIANT": "outline_variant",
    "SHADOW": "shadow",
    "SCRIM": "scrim",
    "INVERSE_SURFACE": "inverse_surface",
    "ON_INVERSE_SURFACE": "on_inverse_surface",
    "INVERSE_PRIMARY": "inverse_primary",
}

THEME_COLOR_ROLE_NAMES = {"scaffold_bgcolor"}

COLOR_ROLE_EXPORT_ORDER = list(dict.fromkeys(COLOR_ROLE_BY_LABEL.values()))

SEED_COLOR_OPTIONS = [
    ("Deep purple", ft.Colors.DEEP_PURPLE),
    ("Indigo", ft.Colors.INDIGO),
    ("Blue (default)", ft.Colors.BLUE),
    ("Teal", ft.Colors.TEAL),
    ("Green", ft.Colors.GREEN),
    ("Yellow", ft.Colors.YELLOW),
    ("Orange", ft.Colors.ORANGE),
    ("Deep orange", ft.Colors.DEEP_ORANGE),
    ("Pink", ft.Colors.PINK),
]

LEFT_PANE_ROLE_TABS = [
    {
        "label": "Accent",
        "groups": [
            {
                "title": "Primary roles",
                "hint": (
                    "Use primary roles for the most\n"
                    "prominent components across the UI,\n"
                    "such as the FAB,\n"
                    "high-emphasis buttons, and active states."
                ),
                "items": [
                    ("PRIMARY", "PRIMARY", "ON_PRIMARY"),
                    ("ON_PRIMARY", "ON_PRIMARY", "PRIMARY"),
                    (
                        "PRIMARY_CONTAINER",
                        "PRIMARY_CONTAINER",
                        "ON_PRIMARY_CONTAINER",
                    ),
                    (
                        "ON_PRIMARY_CONTAINER",
                        "ON_PRIMARY_CONTAINER",
                        "PRIMARY_CONTAINER",
                    ),
                ],
            },
            {
                "title": "Secondary roles",
                "hint": (
                    "Use secondary roles for less prominent\n"
                    "components in the UI such as filter chips."
                ),
                "items": [
                    ("SECONDARY", "SECONDARY", "ON_SECONDARY"),
                    ("ON_SECONDARY", "ON_SECONDARY", "SECONDARY"),
                    (
                        "SECONDARY_CONTAINER",
                        "SECONDARY_CONTAINER",
                        "ON_SECONDARY_CONTAINER",
                    ),
                    (
                        "ON_SECONDARY_CONTAINER",
                        "ON_SECONDARY_CONTAINER",
                        "SECONDARY_CONTAINER",
                    ),
                ],
            },
            {
                "title": "Tertiary roles",
                "hint": (
                    "Use tertiary roles for contrasting accents\n"
                    "that balance primary and secondary colors\n"
                    "or bring heightened attention to an element\n"
                    "such as an input field."
                ),
                "items": [
                    ("TERTIARY", "TERTIARY", "ON_TERTIARY"),
                    ("ON_TERTIARY", "ON_TERTIARY", "TERTIARY"),
                    (
                        "TERTIARY_CONTAINER",
                        "TERTIARY_CONTAINER",
                        "ON_TERTIARY_CONTAINER",
                    ),
                    (
                        "ON_TERTIARY_CONTAINER",
                        "ON_TERTIARY_CONTAINER",
                        "TERTIARY_CONTAINER",
                    ),
                ],
            },
            {
                "title": "Error roles",
                "hint": (
                    "Use error roles to communicate error states,\n"
                    "such as an incorrect password entered\n"
                    "into a text field."
                ),
                "items": [
                    ("ERROR", "ERROR", "ON_ERROR"),
                    ("ON_ERROR", "ON_ERROR", "ERROR"),
                    ("ERROR_CONTAINER", "ERROR_CONTAINER", "ON_ERROR_CONTAINER"),
                    ("ON_ERROR_CONTAINER", "ON_ERROR_CONTAINER", "ERROR_CONTAINER"),
                ],
            },
        ],
    },
    {
        "label": "Surface",
        "groups": [
            {
                "title": "Surface roles",
                "hint": (
                    "Use surface roles for more neutral\n"
                    "backgrounds, and container colors for\n"
                    "components like cards, sheets, and dialogs."
                ),
                "items": [
                    ("SURFACE", "SURFACE", "ON_SURFACE"),
                    ("ON_SURFACE", "ON_SURFACE", "SURFACE"),
                    ("SURFACE_DIM", "SURFACE_DIM", "ON_SURFACE"),
                    ("SURFACE_BRIGHT", "SURFACE_BRIGHT", "ON_SURFACE"),
                    ("SURFACE_TINT", "SURFACE_TINT", "ON_SURFACE"),
                    ("ON_SURFACE_VARIANT", "ON_SURFACE_VARIANT", "SURFACE"),
                ],
            },
            {
                "title": "Surface containers",
                "hint": (
                    "Five surface container roles are named\n"
                    "based on their level of emphasis."
                ),
                "items": [
                    ("SURFACE_CONTAINER", "SURFACE_CONTAINER", "ON_SURFACE"),
                    ("SURFACE_CONTAINER_LOW", "SURFACE_CONTAINER_LOW", "ON_SURFACE"),
                    (
                        "SURFACE_CONTAINER_LOWEST",
                        "SURFACE_CONTAINER_LOWEST",
                        "ON_SURFACE",
                    ),
                    ("SURFACE_CONTAINER_HIGH", "SURFACE_CONTAINER_HIGH", "ON_SURFACE"),
                    (
                        "SURFACE_CONTAINER_HIGHEST",
                        "SURFACE_CONTAINER_HIGHEST",
                        "ON_SURFACE",
                    ),
                ],
            },
            {
                "title": "Page background",
                "hint": "Customizes the page background color.",
                "items": [
                    ("SCAFFOLD_BGCOLOR", "SCAFFOLD_BGCOLOR", "ON_SURFACE"),
                ],
            },
            {
                "title": "Outline roles",
                "items": [
                    ("OUTLINE", "OUTLINE", "SURFACE"),
                    ("OUTLINE_VARIANT", "OUTLINE_VARIANT", "ON_SURFACE"),
                ],
            },
        ],
    },
    {
        "label": "Add-on",
        "groups": [
            {
                "title": "Primary fixed roles",
                "items": [
                    ("PRIMARY_FIXED", "PRIMARY_FIXED", "ON_PRIMARY_FIXED"),
                    ("PRIMARY_FIXED_DIM", "PRIMARY_FIXED_DIM", "ON_PRIMARY_FIXED"),
                    ("ON_PRIMARY_FIXED", "ON_PRIMARY_FIXED", "PRIMARY_FIXED"),
                    (
                        "ON_PRIMARY_FIXED_VARIANT",
                        "ON_PRIMARY_FIXED_VARIANT",
                        "PRIMARY_FIXED",
                    ),
                ],
            },
            {
                "title": "Secondary fixed roles",
                "items": [
                    ("SECONDARY_FIXED", "SECONDARY_FIXED", "ON_SECONDARY_FIXED"),
                    (
                        "SECONDARY_FIXED_DIM",
                        "SECONDARY_FIXED_DIM",
                        "ON_SECONDARY_FIXED",
                    ),
                    ("ON_SECONDARY_FIXED", "ON_SECONDARY_FIXED", "SECONDARY_FIXED"),
                    (
                        "ON_SECONDARY_FIXED_VARIANT",
                        "ON_SECONDARY_FIXED_VARIANT",
                        "SECONDARY_FIXED",
                    ),
                ],
            },
            {
                "title": "Tertiary fixed roles",
                "items": [
                    ("TERTIARY_FIXED", "TERTIARY_FIXED", "ON_TERTIARY_FIXED"),
                    (
                        "TERTIARY_FIXED_DIM",
                        "TERTIARY_FIXED_DIM",
                        "ON_TERTIARY_FIXED",
                    ),
                    ("ON_TERTIARY_FIXED", "ON_TERTIARY_FIXED", "TERTIARY_FIXED"),
                    (
                        "ON_TERTIARY_FIXED_VARIANT",
                        "ON_TERTIARY_FIXED_VARIANT",
                        "TERTIARY_FIXED",
                    ),
                ],
            },
            {
                "title": "Utility roles",
                "items": [
                    ("SHADOW", "SHADOW", "SURFACE"),
                    ("SCRIM", "SCRIM", "SURFACE"),
                    ("INVERSE_SURFACE", "INVERSE_SURFACE", "ON_INVERSE_SURFACE"),
                    ("ON_INVERSE_SURFACE", "ON_INVERSE_SURFACE", "INVERSE_SURFACE"),
                    ("INVERSE_PRIMARY", "INVERSE_PRIMARY", "ON_PRIMARY"),
                ],
            },
        ],
    },
]
