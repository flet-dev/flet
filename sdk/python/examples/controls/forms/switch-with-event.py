import flet
from flet import Page, Switch


def main(page: Page):
    def theme_changed(e):
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        c.label = "Light theme" if page.theme_mode == "light" else "Dark theme"
        page.update()

    page.theme_mode = "light"
    c = Switch(label="Light theme", on_change=theme_changed)
    page.add(c)


flet.app(target=main)
