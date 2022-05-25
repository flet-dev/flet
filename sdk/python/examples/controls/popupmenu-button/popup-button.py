import flet
from flet import Icon, Page, PopupMenuButton, PopupMenuItem, Row, Text, icons


def main(page: Page):
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = PopupMenuButton(
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
                on_click=lambda _: print("Button with a custom content clicked!"),
            ),
            PopupMenuItem(),  # divider
            PopupMenuItem(
                text="Checked item", checked=False, on_click=check_item_clicked
            ),
        ]
    )
    page.add(pb)


flet.app(target=main)
