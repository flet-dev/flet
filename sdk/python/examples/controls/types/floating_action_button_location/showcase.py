import flet as ft


def showcase_card(location: ft.FloatingActionButtonLocation) -> ft.Container:
    mini = location.name.startswith("MINI_")
    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(location.name, weight=ft.FontWeight.BOLD),
                ft.Pagelet(
                    width=260,
                    height=200,
                    bgcolor=ft.Colors.SURFACE,
                    appbar=ft.AppBar(
                        title=ft.Text("AppBar", size=12),
                        center_title=True,
                        toolbar_height=38,
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                    ),
                    content=ft.Container(
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Body", size=12),
                    ),
                    bottom_appbar=ft.BottomAppBar(
                        height=42,
                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    ),
                    floating_action_button=ft.FloatingActionButton(
                        icon=ft.Icons.ADD,
                        mini=mini,
                        bgcolor=ft.Colors.LIGHT_BLUE_400,
                    ),
                    floating_action_button_location=location,
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="FloatingActionButtonLocation Showcase")
    page.add(
        ft.Text("Compare FloatingActionButton placement presets."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(location) for location in ft.FloatingActionButtonLocation
            ],
        ),
    )


ft.run(main)
