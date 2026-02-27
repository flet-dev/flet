import flet as ft

from models import TrolliState
from .dialogs import show_new_board_dialog


@ft.component
def BoardsView(app: TrolliState):
    return ft.Column(
        expand=True,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    ft.FilledButton(
                        "Add new board",
                        icon=ft.Icons.ADD,
                        on_click=lambda _: show_new_board_dialog(app),
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    ft.Text(
                        "Your Boards", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM
                    ),
                ],
            ),
            ft.Row(
                wrap=True,
                controls=[
                    ft.Container(
                        width=260,
                        padding=ft.Padding.all(10),
                        border=ft.Border.all(1, ft.Colors.BLACK_38),
                        border_radius=ft.BorderRadius.all(8),
                        bgcolor=ft.Colors.WHITE_60,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.TextButton(
                                    b.name,
                                    on_click=lambda _, b=b: ft.context.page.go(
                                        f"/board/{b.board_id}"
                                    ),
                                ),
                                ft.PopupMenuButton(
                                    items=[
                                        ft.PopupMenuItem(
                                            content=ft.Text("Delete"),
                                            on_click=lambda _, b=b: app.delete_board(b),
                                        )
                                    ]
                                ),
                            ],
                        ),
                    )
                    for b in app.boards
                ],
            ),
        ],
    )
