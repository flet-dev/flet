import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    semantics = ft.SemanticsService()

    def showcase_card(assertiveness: ft.Assertiveness) -> ft.Container:
        status = ft.Text("Send an accessibility announcement.", size=11)

        async def announce():
            try:
                await semantics.announce_message(
                    f"Announcement with {assertiveness.name} assertiveness.",
                    assertiveness=assertiveness,
                )
                status.value = f"Sent with {assertiveness.value}."
            except Exception as ex:
                status.value = f"Error: {ex}"
            status.update()

        return ft.Container(
            width=320,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(assertiveness.name, weight=ft.FontWeight.BOLD),
                    ft.Text(
                        assertiveness.value,
                        size=11,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    ft.Button(
                        "Announce message",
                        icon=ft.Icons.RECORD_VOICE_OVER,
                        on_click=lambda: page.run_task(announce),
                    ),
                    status,
                ],
            ),
        )

    page.appbar = ft.AppBar(title="Assertiveness Showcase")
    page.add(
        ft.Text(
            "Compare announcement assertiveness levels. "
            "Enable a screen reader to hear the difference."
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(assertiveness) for assertiveness in ft.Assertiveness
            ],
        ),
    )


ft.run(main)
