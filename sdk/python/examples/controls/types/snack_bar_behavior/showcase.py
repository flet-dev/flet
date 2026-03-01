import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def open_snack(behavior: ft.SnackBarBehavior):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(f"Behavior: {behavior.name}"),
                behavior=behavior,
                margin=ft.Margin.only(bottom=100),
                action=ft.SnackBarAction(label="Close"),
            )
        )

    def showcase_card(behavior: ft.SnackBarBehavior) -> ft.Container:
        return ft.Container(
            width=300,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(behavior.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open SnackBar",
                        icon=ft.Icons.MESSAGE,
                        on_click=lambda _, b=behavior: open_snack(b),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="SnackBarBehavior Showcase")
    page.add(
        ft.Text("Compare snack bar placement: fixed vs floating."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(behavior) for behavior in ft.SnackBarBehavior],
        ),
    )


ft.run(main)
