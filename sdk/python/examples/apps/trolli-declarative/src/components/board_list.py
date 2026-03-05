# from __future__ import annotations

import flet as ft

from models import BoardList
from .card import CardView


@ft.component
def BoardListView(board_list: BoardList, move_list):
    is_list_over, set_is_list_over = ft.use_state(False)
    is_end_over, set_is_end_over = ft.use_state(False)
    new_card_text, set_new_card_text = ft.use_state("")
    card_list: list[ft.Control] = [CardView(card) for card in board_list.cards]

    def on_add_card_click(_: ft.Event[ft.TextButton]):
        if stripped := new_card_text.strip():
            board_list.add_card(stripped)
            set_new_card_text("")

    def on_add_card_submit(_: ft.Event[ft.TextField]):
        if stripped := new_card_text.strip():
            board_list.add_card(stripped)
            set_new_card_text("")

    def on_delete(_: ft.Event[ft.PopupMenuItem]):
        board_list.board.remove_list(board_list)

    def change_card_text(e: ft.Event[ft.TextField]):
        set_new_card_text(e.control.value)

    def on_end_accept(e: ft.DragTargetEvent):
        board_list.move_card_into(e.src.data)
        set_is_end_over(False)

    def on_list_accept(e: ft.DragTargetEvent):
        move_list(e.src.data, board_list)
        set_is_list_over(False)

    return ft.Row(
        spacing=4,
        intrinsic_height=True,
        controls=[
            ft.VerticalDivider(
                color=ft.Colors.BLACK_54,
                width=2,
                thickness=2,
                radius=2,
                leading_indent=15,
                trailing_indent=15,
                opacity=1.0 if is_list_over else 0.0,
            ),
            ft.Draggable(
                group="lists",
                data=board_list,
                content=ft.DragTarget(
                    group="cards",
                    data=board_list,
                    on_will_accept=lambda e: set_is_end_over(e.accept),
                    on_accept=on_end_accept,
                    on_leave=lambda: set_is_end_over(False),
                    content=ft.DragTarget(
                        group="lists",
                        data=board_list,
                        on_will_accept=lambda e: set_is_list_over(
                            e.accept and e.src.data != board_list
                        ),
                        on_accept=on_list_accept,
                        on_leave=lambda: set_is_list_over(False),
                        content=ft.Container(
                            border=ft.Border.all(
                                2,
                                (
                                    ft.Colors.BLACK_38
                                    if is_list_over
                                    else ft.Colors.BLACK_12
                                ),
                            ),
                            border_radius=ft.BorderRadius.all(8),
                            bgcolor=board_list.color,
                            padding=ft.Padding.all(10),
                            width=240,
                            content=ft.Column(
                                spacing=6,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text(
                                                board_list.title,
                                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                            ),
                                            ft.PopupMenuButton(
                                                items=[
                                                    ft.PopupMenuItem(
                                                        content=ft.Text("Delete"),
                                                        on_click=on_delete,
                                                    )
                                                ]
                                            ),
                                        ],
                                    ),
                                    ft.TextField(
                                        label="New card",
                                        bgcolor=ft.Colors.WHITE,
                                        value=new_card_text,
                                        on_change=change_card_text,
                                        on_submit=on_add_card_submit,
                                    ),
                                    ft.TextButton(
                                        content="Add card",
                                        icon=ft.Icons.ADD,
                                        on_click=on_add_card_click,
                                    ),
                                    ft.Column(
                                        spacing=2,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            *card_list,
                                            ft.Divider(
                                                color=ft.Colors.BLACK_38,
                                                thickness=2,
                                                height=2,
                                                radius=2,
                                                opacity=1.0 if is_end_over else 0.0,
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ],
    )
