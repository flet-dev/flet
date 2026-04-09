from models import Card

import flet as ft


@ft.component
def CardView(card: Card):
    is_over, set_is_over = ft.use_state(False)

    def on_accept(e: ft.DragTargetEvent):
        card.board_list.move_card_at(e.src.data, card)
        set_is_over(False)

    return ft.Column(
        spacing=2,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Divider(
                color=ft.Colors.BLACK_38,
                thickness=2,
                height=2,
                radius=2,
                opacity=1.0 if is_over else 0.0,
            ),
            ft.Draggable(
                group="cards",
                data=card,
                content=ft.DragTarget(
                    group="cards",
                    data=card,
                    on_will_accept=lambda e: set_is_over(
                        e.accept and e.src.data != card
                    ),
                    on_accept=on_accept,
                    on_leave=lambda: set_is_over(False),
                    content=ft.Card(
                        elevation=1,
                        content=ft.Container(
                            padding=7,
                            width=200,
                            content=ft.Row(
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    ft.Icon(ft.Icons.CIRCLE_OUTLINED),
                                    ft.Container(
                                        expand=True,
                                        content=ft.Text(
                                            value=card.text,
                                            no_wrap=False,
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ),
                ),
            ),
        ],
    )
