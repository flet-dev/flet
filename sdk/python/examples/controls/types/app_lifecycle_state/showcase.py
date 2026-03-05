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

    def on_lifecycle(e: ft.AppLifecycleStateChangeEvent):
        add_log(f"Received: {e.state.name}")

    page.on_app_lifecycle_state_change = on_lifecycle

    page.appbar = ft.AppBar(title="AppLifecycleState Showcase")
    page.add(
        ft.Text("Switch app focus/visibility to see lifecycle state changes."),
        ft.Text(
            "Ex: minimize/restore app, switch tabs, or background/foreground app.",
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
                    content=ft.Text(state.name, size=11),
                )
                for state in ft.AppLifecycleState
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
