"""Month navigation shared with the monthly summary."""

from datetime import date

import theme
from state import StateContext

import flet as ft


@ft.component
def MonthPicker():
    state = ft.use_context(StateContext)
    month = state.selected_month
    return ft.Column(
        spacing=theme.Space.XS,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        controls=[
            ft.Row(
                spacing=theme.Space.S,
                controls=[
                    ft.IconButton(
                        ft.Icons.CHEVRON_LEFT,
                        tooltip="Previous month",
                        disabled=month.year == 1 and month.month == 1,
                        on_click=lambda: state.change_month(-1),
                    ),
                    ft.Text(
                        month.strftime("%B %Y"),
                        expand=True,
                        text_align=ft.TextAlign.CENTER,
                        theme_style=theme.Text.TITLE,
                    ),
                    ft.IconButton(
                        ft.Icons.CHEVRON_RIGHT,
                        tooltip="Next month",
                        disabled=month.year == 9999 and month.month == 12,
                        on_click=lambda: state.change_month(1),
                    ),
                ],
            ),
            *(
                [ft.TextButton("Back to this month", on_click=state.go_to_this_month)]
                if month != date.today().replace(day=1)
                else []
            ),
        ],
    )
