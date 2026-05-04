import flet as ft


def main(page: ft.Page):
    def refresh_position(e: ft.DragTargetEvent):
        lp_label.value = (
            f"local_position: ({e.local_position.x:.1f}, {e.local_position.y:.1f})"
        )
        gp_label.value = (
            f"global_position: ({e.global_position.x:.1f}, {e.global_position.y:.1f})"
        )
        target.update()

    def handle_will_accept(e: ft.DragWillAcceptEvent):
        target.content.border = ft.Border.all(3, ft.Colors.RED)
        target.update()

    def handle_move(e: ft.DragTargetEvent):
        refresh_position(e)

    def handle_accept(e: ft.DragTargetEvent):
        refresh_position(e)

    def handle_leave(e: ft.DragTargetLeaveEvent):
        target.content.border = ft.Border.all(3, ft.Colors.BLUE_GREY_300)
        target.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Draggable(
                                group="demo",
                                content_feedback=ft.Container(
                                    width=40,
                                    height=40,
                                    border_radius=18,
                                    alignment=ft.Alignment.CENTER,
                                    bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.RED),
                                    border=ft.Border.all(
                                        1.5,
                                        ft.Colors.with_opacity(
                                            0.35, ft.Colors.BLUE_500
                                        ),
                                    ),
                                    shadow=ft.BoxShadow(
                                        blur_radius=16,
                                        color=ft.Colors.with_opacity(
                                            0.16, ft.Colors.BLUE_500
                                        ),
                                        offset=ft.Offset(0, 6),
                                    ),
                                    content=ft.Icon(
                                        ft.Icons.OPEN_WITH_ROUNDED,
                                        color=ft.Colors.BLUE_600,
                                    ),
                                ),
                                content=ft.Container(
                                    width=72,
                                    height=72,
                                    border_radius=12,
                                    bgcolor=ft.Colors.BLUE_500,
                                    alignment=ft.Alignment.CENTER,
                                    content=ft.Text("Drag me", color=ft.Colors.WHITE),
                                ),
                            ),
                            target := ft.DragTarget(
                                group="demo",
                                on_will_accept=handle_will_accept,
                                on_move=handle_move,
                                on_accept=handle_accept,
                                on_leave=handle_leave,
                                content=ft.Container(
                                    width=290,
                                    height=180,
                                    padding=16,
                                    border=ft.Border.all(2, ft.Colors.BLUE_GREY_300),
                                    border_radius=12,
                                    bgcolor=ft.Colors.BLUE_GREY_50,
                                    content=ft.Column(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.Text(
                                                "Drop here",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                            lp_label := ft.Text(
                                                "local_position: -",
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                            gp_label := ft.Text(
                                                "global_position: -",
                                                text_align=ft.TextAlign.CENTER,
                                            ),
                                        ],
                                    ),
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
