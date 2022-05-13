import flet
from flet import Text


def main(page):
    page.title = "TextField Examples"
    page.theme_mode = "dark"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.add(Text("Hello, world!", expand=True))

    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)

    page.on_resize = page_resize


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
