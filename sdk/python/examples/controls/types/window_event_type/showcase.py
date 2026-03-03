import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    log = ft.Column(
        spacing=4,
        scroll=ft.ScrollMode.AUTO,
        height=220,
    )

    def add_log(message: str):
        log.controls.insert(0, ft.Text(message, size=12))
        if len(log.controls) > 20:
            log.controls.pop()
        log.update()

    def on_window_event(e: ft.WindowEvent):
        add_log(f"Received: {e.type.name}")

    page.window.on_event = on_window_event

    page.appbar = ft.AppBar(title="WindowEventType Showcase")
    page.add(
        ft.Text("Interact with the app window and watch incoming event types."),
        ft.Text(
            "Desktop only. Try focus, blur, resize, move, minimize, maximize.",
            size=11,
        ),
        ft.Row(
            wrap=True,
            spacing=8,
            controls=[
                ft.Container(
                    padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=12,
                    content=ft.Text(event_type.name, size=11),
                )
                for event_type in ft.WindowEventType
            ],
        ),
        ft.Container(
            width=720,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=log,
        ),
    )


ft.run(main)
