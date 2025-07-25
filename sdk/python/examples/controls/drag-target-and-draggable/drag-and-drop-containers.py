import flet as ft


def main(page: ft.Page):
    def handle_drag_will_accept(e: ft.DragWillAcceptEvent):
        e.control.content.border = ft.Border.all(
            2, ft.Colors.BLACK45 if e.accept else ft.Colors.RED
        )
        e.control.update()

    def handle_drag_accept(e: ft.DragTargetEvent):
        src = page.get_control(e.src_id)
        e.control.content.bgcolor = src.content.bgcolor
        e.control.content.border = None
        e.control.update()

    def handle_drag_leave(e: ft.DragTargetLeaveEvent):
        e.control.content.border = None
        e.control.update()

    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.Colors.CYAN,
                                border_radius=5,
                            ),
                            content_feedback=ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.Colors.CYAN,
                                border_radius=3,
                            ),
                        ),
                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.Colors.YELLOW,
                                border_radius=5,
                            ),
                        ),
                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.Colors.GREEN,
                                border_radius=5,
                            ),
                        ),
                    ]
                ),
                ft.Container(width=100),
                ft.DragTarget(
                    group="color",
                    on_will_accept=handle_drag_will_accept,
                    on_accept=handle_drag_accept,
                    on_leave=handle_drag_leave,
                    content=ft.Container(
                        width=50,
                        height=50,
                        bgcolor=ft.Colors.BLUE_GREY_100,
                        border_radius=5,
                    ),
                ),
            ]
        )
    )


ft.run(main)
