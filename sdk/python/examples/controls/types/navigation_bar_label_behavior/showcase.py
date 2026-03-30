import flet as ft


def showcase_card(behavior: ft.NavigationBarLabelBehavior) -> ft.Container:
    bar = ft.NavigationBar(
        label_behavior=behavior,
        selected_index=1,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Profile"),
        ],
    )

    return ft.Container(
        width=380,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(behavior.name, weight=ft.FontWeight.BOLD),
                bar,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="NavigationBarLabelBehavior Showcase")
    page.add(
        ft.Text("Compare destination label visibility strategies."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(behavior) for behavior in ft.NavigationBarLabelBehavior
            ],
        ),
    )


ft.run(main)
