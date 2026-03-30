import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def open_url(target: ft.UrlTarget):
        url = "https://flet.dev"
        await ft.UrlLauncher().launch_url(ft.Url(url=url, target=target))
        status.value = f"Opened {url} with target {target.name}"
        status.update()

    def showcase_card(target: ft.UrlTarget) -> ft.Container:
        return ft.Container(
            width=280,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(target.name, weight=ft.FontWeight.BOLD),
                    ft.Text(target.value, size=12, color=ft.Colors.ON_SURFACE_VARIANT),
                    ft.Button(
                        "Open flet.dev",
                        icon=ft.Icons.OPEN_IN_NEW,
                        on_click=lambda: page.run_task(open_url, target),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="UrlTarget Showcase")
    page.add(
        ft.Text("Click a card to launch URL with the selected browser target."),
        status := ft.Text(),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(target) for target in ft.UrlTarget],
        ),
    )


ft.run(main)
