from dataclasses import dataclass

import flet as ft


@dataclass
@ft.observable
class TargetState:
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    is_drag_over: bool = False


@ft.component
def App():
    target, _ = ft.use_state(TargetState())

    def on_will_accept(e: ft.DragWillAcceptEvent):
        target.is_drag_over = True

    def on_accept(e: ft.DragTargetEvent):
        target.bgcolor = e.src.data
        target.is_drag_over = False

    def on_leave(e: ft.DragTargetLeaveEvent):
        target.is_drag_over = False

    return ft.Row(
        controls=[
            ft.Column(
                controls=[
                    ft.Draggable(
                        group="color",
                        data=ft.Colors.CYAN,
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
                        data=ft.Colors.YELLOW,
                        content=ft.Container(
                            width=50,
                            height=50,
                            bgcolor=ft.Colors.YELLOW,
                            border_radius=5,
                        ),
                    ),
                    ft.Draggable(
                        group="color",
                        data=ft.Colors.GREEN,
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
                on_will_accept=on_will_accept,
                on_accept=on_accept,
                on_leave=on_leave,
                content=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=target.bgcolor,
                    border=ft.Border.all(2, ft.Colors.BLACK45)
                    if target.is_drag_over
                    else None,
                    border_radius=5,
                ),
            ),
        ]
    )


ft.run(lambda page: page.render(App))
