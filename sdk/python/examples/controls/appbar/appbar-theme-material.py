from time import sleep

import flet
from flet import ElevatedButton, Page, Text, colors, icons, theme
from flet.app_bar import AppBar
from flet.icon import Icon
from flet.icon_button import IconButton
from flet.popup_menu_button import PopupMenuButton, PopupMenuItem
from flet.row import Row

LIGHT_SEED_COLOR = colors.DEEP_ORANGE
DARK_SEED_COLOR = colors.INDIGO


def main(page: Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.title = "AppBar Example"
    page.theme_mode = "light"
    page.theme = theme.Theme(color_scheme_seed=LIGHT_SEED_COLOR, use_material3=True)
    page.dark_theme = theme.Theme(color_scheme_seed=DARK_SEED_COLOR, use_material3=True)
    page.update()

    def toggle_theme_mode(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        lightMode.icon = (
            icons.WB_SUNNY_OUTLINED if page.theme_mode == "light" else icons.WB_SUNNY
        )
        page.update()

    lightMode = IconButton(
        icons.WB_SUNNY_OUTLINED if page.theme_mode == "light" else icons.WB_SUNNY,
        on_click=toggle_theme_mode,
    )

    def toggle_material(e):
        use_material3 = not page.theme.use_material3
        page.theme = theme.Theme(
            color_scheme_seed=LIGHT_SEED_COLOR, use_material3=use_material3
        )
        page.dark_theme = theme.Theme(
            color_scheme_seed=DARK_SEED_COLOR, use_material3=use_material3
        )
        materialMode.icon = (
            icons.FILTER_3 if page.theme.use_material3 else icons.FILTER_2
        )
        page.update()

    materialMode = IconButton(
        icons.FILTER_3 if page.theme.use_material3 else icons.FILTER_2,
        on_click=toggle_material,
    )

    page.padding = 50
    page.appbar = AppBar(
        # toolbar_height=100,
        # bgcolor=colors.SECONDARY_CONTAINER,
        leading=Icon(icons.PALETTE),
        leading_width=40,
        title=Text("AppBar Example"),
        center_title=False,
        actions=[
            lightMode,
            materialMode,
            PopupMenuButton(
                items=[
                    PopupMenuItem(text="Item 1"),
                    PopupMenuItem(icon=icons.POWER_INPUT, text="Check power"),
                    PopupMenuItem(
                        content=Row(
                            [
                                Icon(icons.HOURGLASS_TOP_OUTLINED),
                                Text("Item with a custom content"),
                            ]
                        ),
                        on_click=lambda _: print(
                            "Button with a custom content clicked!"
                        ),
                    ),
                    PopupMenuItem(),  # divider
                    PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )
    page.add(Text("Body!"), ElevatedButton("Click me!"))


flet.app(target=main)
