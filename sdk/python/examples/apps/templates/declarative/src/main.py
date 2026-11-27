import logging

import theme
from app import App

import flet as ft

LOG_LEVEL = logging.INFO  # switch to logging.DEBUG while diagnosing
logging.basicConfig(format="%(levelname)s %(name)s: %(message)s")
logging.getLogger("app").setLevel(LOG_LEVEL)


def main(page: ft.Page):
    page.title = "Flet app"
    page.theme = theme.build_theme()
    page.dark_theme = theme.build_dark_theme()
    page.render_views(App)


ft.run(main)
