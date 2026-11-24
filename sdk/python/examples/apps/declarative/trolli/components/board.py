from __future__ import annotations

from models import Board

import flet as ft

from .board_list import BoardListView
from .dialogs import show_new_list_dialog


@ft.component
def BoardView(board: Board):
    return ft.Column(
        expand=True,
        spacing=10,
        controls=[
            ft.Row(
                # height=30,
                expand_loose=True,
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.FilledButton(
                        "Add list",
                        icon=ft.Icons.ADD,
                        on_click=lambda _: show_new_list_dialog(board),
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(board.name, theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ],
            ),
            ft.Row(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    *[
                        BoardListView(bl, move_list=board.move_list)
                        for bl in board.lists
                    ],
                ],
            ),
        ],
    )
