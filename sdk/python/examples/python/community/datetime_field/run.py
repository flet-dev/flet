import flet as ft

from .datetime_field import DatetimeField

callback = lambda e: print(e)


def main(page: ft.Page):
    calendar = DatetimeField(page=page, on_change=callback)
    page.add(calendar)


ft.app(target=main)
