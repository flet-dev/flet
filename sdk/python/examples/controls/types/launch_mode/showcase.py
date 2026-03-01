import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    launcher = ft.UrlLauncher()

    def showcase_card(mode: ft.LaunchMode) -> ft.Container:
        status = ft.Text("Click to check support on this platform.", size=11)

        async def check_support():
            try:
                supported = await launcher.supports_launch_mode(mode)
                closable = await launcher.supports_close_for_launch_mode(mode)
                status.value = (
                    f"supports_launch_mode={supported} / supports_close={closable}"
                )
            except Exception as ex:
                status.value = f"Error: {ex}"
            status.update()

        return ft.Container(
            width=360,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(mode.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Check support",
                        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                        on_click=lambda: page.run_task(check_support),
                    ),
                    status,
                ],
            ),
        )

    page.appbar = ft.AppBar(title="LaunchMode Showcase")
    page.add(
        ft.Text("Check launch-mode support reported by the current platform."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(mode) for mode in ft.LaunchMode],
        ),
    )


ft.run(main)
