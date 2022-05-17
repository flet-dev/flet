import flet
from flet import IconButton, Page, Text, icons


def main(page: Page):
    page.title = "Icon button with 'click' event"

    def button_clicked(e):
        b.data += 1
        t.value = f"Button clicked {b.data} time(s)"
        page.update()

    b = IconButton(
        icon=icons.PLAY_CIRCLE_FILL_OUTLINED, on_click=button_clicked, data=0
    )
    t = Text()

    page.add(b, t)


flet.app(target=main)
