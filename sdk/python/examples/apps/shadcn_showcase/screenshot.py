"""A compact Shadcn UI scene sized for a blog post screenshot.

Press D to switch between light and dark mode, and C to cycle color schemes.
"""

import datetime

import flet_shadcn_ui as shad

import flet as ft


def create_project_card() -> shad.Card:
    return shad.Card(
        width=340,
        title="Create project",
        description="Deploy your new project in one-click.",
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Container(height=0),
                shad.Input(label="Name", value="flet-dashboard"),
                shad.Select(
                    label="Framework",
                    value="flet",
                    width=290,
                    options=[
                        shad.SelectOption(value="flet", text="Flet"),
                        shad.SelectOption(value="fastapi", text="FastAPI"),
                        shad.SelectOption(value="django", text="Django"),
                    ],
                ),
                shad.Switch(
                    label="Deploy on push",
                    sublabel="Build every commit to main.",
                    value=True,
                ),
                ft.Container(height=8),
            ],
        ),
        footer=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                shad.Button("Cancel", variant=shad.ButtonVariant.OUTLINE),
                shad.Button("Deploy", leading=shad.LucideIcons.ROCKET),
            ],
        ),
    )


def calendar_card() -> shad.Card:
    return shad.Card(
        padding=8,
        content=shad.Calendar(value=datetime.date(2026, 11, 4)),
    )


def main(page: ft.Page):
    page.title = "Shadcn UI for Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 760
    page.window.height = 560
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    schemes = list(shad.ColorScheme)

    def handle_key(e: ft.KeyboardEvent):
        if e.key == "D":
            dark = page.theme_mode == ft.ThemeMode.DARK
            page.theme_mode = ft.ThemeMode.LIGHT if dark else ft.ThemeMode.DARK
        elif e.key == "C":
            i = schemes.index(theme.color_scheme)
            theme.color_scheme = schemes[(i + 1) % len(schemes)]
            page.title = f"Shadcn UI for Flet - {theme.color_scheme.name.title()}"
        page.update()

    page.on_keyboard_event = handle_key

    theme = shad.Theme(
        color_scheme=shad.ColorScheme.ZINC,
        content=ft.Column(
            tight=True,
            spacing=16,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Row(
                    tight=True,
                    spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[create_project_card(), calendar_card()],
                ),
                ft.Row(
                    tight=True,
                    spacing=8,
                    controls=[
                        shad.Badge("New"),
                        shad.Badge("Flet 1.1", variant=shad.BadgeVariant.SECONDARY),
                        shad.Badge("33 controls", variant=shad.BadgeVariant.OUTLINE),
                        shad.Badge("Lucide icons", variant=shad.BadgeVariant.OUTLINE),
                    ],
                ),
            ],
        ),
    )

    page.add(theme)


if __name__ == "__main__":
    ft.run(main)
