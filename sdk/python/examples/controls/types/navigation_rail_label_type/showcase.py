import flet as ft


def showcase_card(label_type: ft.NavigationRailLabelType) -> ft.Container:
    rail = ft.NavigationRail(
        width=100,
        height=220,
        selected_index=1,
        label_type=label_type,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationRailDestination(icon=ft.Icons.SEARCH, label="Search"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Profile"),
        ],
    )

    return ft.Container(
        width=300,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(label_type.name, weight=ft.FontWeight.BOLD),
                rail,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="NavigationRailLabelType Showcase")
    page.add(
        ft.Text("Compare label visibility in compact navigation rail."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(t) for t in ft.NavigationRailLabelType],
        ),
    )


ft.run(main)
