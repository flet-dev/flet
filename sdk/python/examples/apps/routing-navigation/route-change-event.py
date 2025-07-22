import flet
from flet import Page, Text


def main(page: Page):
    page.add(Text(f"Initial route: {page.route}"))

    def route_change(e):
        page.add(Text(f"New route: {e.route}"))

    page.on_route_change = route_change
    page.update()


flet.app(target=main, view=flet.AppView.WEB_BROWSER)
