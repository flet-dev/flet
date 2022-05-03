import flet
from flet import Text


def main(page):
    page.title = "TextField Examples"
    page.theme_mode = "light"
    page.add(Text("Hello, world!"))
    page.update()


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
