import flet
from flet import Dropdown, Page, Row, Text, TextField


def main(page: Page):
    page.add(Row(
        [Dropdown(
        #expand=True,
        autofocus=True,
    )]
    ))


flet.app(target=main, view=flet.WEB_BROWSER)
