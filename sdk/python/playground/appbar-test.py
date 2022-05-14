from time import sleep

import flet
from flet import ElevatedButton, Page, Text, colors, icons, theme
from flet.app_bar import AppBar
from flet.icon import Icon
from flet.icon_button import IconButton
from flet.popup_menu_button import PopupMenuButton, PopupMenuItem
from flet.row import Row


def main(page: Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.title = "AppBar Example"
    page.theme_mode = "light"
    page.theme = theme.Theme(color_scheme_seed=colors.DEEP_ORANGE, use_material3=True)
    page.update()

    page.padding = 50
    page.appbar = AppBar(
        bgcolor=colors.SECONDARY_CONTAINER,
        leading=Icon(icons.PALETTE),
        leading_width=40,
        title=Text("Hello app!"),
        center_title=False,
        actions=[
            IconButton(icons.LIGHT),
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


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
