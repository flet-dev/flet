import flet as ft

LIGHT_SEED_COLOR = ft.Colors.DEEP_ORANGE
DARK_SEED_COLOR = ft.Colors.DEEP_PURPLE


def main(page: ft.Page):
    page.title = "AppBar Example"

    def handle_checked_item_click(e: ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        page.update()

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=False)
    page.dark_theme = ft.Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=False)
    page.update()

    def toggle_theme_mode(e: ft.Event[ft.IconButton]):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        theme_mode_toggle.icon = (
            ft.Icons.WB_SUNNY_OUTLINED
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.WB_SUNNY
        )
        page.update()

    theme_mode_toggle = ft.IconButton(
        icon=(
            ft.Icons.WB_SUNNY_OUTLINED
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.WB_SUNNY
        ),
        on_click=toggle_theme_mode,
    )

    def toggle_material(e: ft.Event[ft.IconButton]):
        use_material3 = not page.theme.use_material3
        page.theme = ft.Theme(
            color_scheme_seed=LIGHT_SEED_COLOR, use_material3=use_material3
        )
        page.dark_theme = ft.Theme(
            color_scheme_seed=DARK_SEED_COLOR, use_material3=use_material3
        )
        material_mode_toggle.icon = (
            ft.Icons.FILTER_3 if page.theme.use_material3 else ft.Icons.FILTER_2
        )
        page.update()

    material_mode_toggle = ft.IconButton(
        icon=ft.Icons.FILTER_3 if page.theme.use_material3 else ft.Icons.FILTER_2,
        on_click=toggle_material,
    )

    page.padding = 50
    page.appbar = ft.AppBar(
        # toolbar_height=100,
        bgcolor=ft.Colors.SECONDARY_CONTAINER,
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        actions=[
            theme_mode_toggle,
            material_mode_toggle,
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content="Item 1"),
                    ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, content="Check power"),
                    ft.PopupMenuItem(
                        on_click=lambda _: print(
                            "Button with a custom content clicked!"
                        ),
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                                ft.Text("Item with a custom content"),
                            ]
                        ),
                    ),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        content="Checked item",
                        checked=False,
                        on_click=handle_checked_item_click,
                    ),
                ]
            ),
        ],
    )
    page.add(
        ft.Text(
            value="Flet is a framework that allows building web, desktop and mobile applications in Python without prior experience in frontend development.You can build a UI for your program with Flet controls which are based on Flutter by Google. Flet goes beyond merely wrapping Flutter widgets. It adds its own touch by combining smaller widgets, simplifying complexities, implementing UI best practices, and applying sensible defaults. This ensures that your applications look stylish and polished without requiring additional design efforts on your part.",
            text_align=ft.TextAlign.END,
        ),
        ft.ElevatedButton("Click me!"),
    )


ft.run(main)
