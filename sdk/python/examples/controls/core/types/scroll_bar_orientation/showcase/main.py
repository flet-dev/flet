import flet as ft


def showcase_card(orientation: ft.ScrollbarOrientation) -> ft.Container:
    is_vertical = orientation in (
        ft.ScrollbarOrientation.LEFT,
        ft.ScrollbarOrientation.RIGHT,
    )
    scrollbar = ft.Scrollbar(
        orientation=orientation,
        thumb_visibility=True,
        track_visibility=True,
        thickness=10,
        radius=8,
    )

    if is_vertical:
        viewport = ft.Container(
            height=220,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            padding=8,
            content=ft.Column(
                spacing=4,
                scroll=scrollbar,
                controls=[ft.Text(f"Item {i + 1}") for i in range(35)],
            ),
        )
    else:
        viewport = ft.Container(
            height=130,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            padding=8,
            content=ft.Row(
                spacing=8,
                scroll=scrollbar,
                controls=[
                    ft.Container(
                        width=84,
                        height=72,
                        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                        border_radius=8,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text(f"{i + 1}"),
                    )
                    for i in range(20)
                ],
            ),
        )

    return ft.Container(
        width=330,
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(orientation.name, weight=ft.FontWeight.BOLD),
                viewport,
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ScrollbarOrientation Showcase")
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "LEFT/RIGHT apply to vertical scrollables, TOP/BOTTOM apply to "
                        "horizontal scrollables.",
                    ),
                    ft.Row(
                        wrap=True,
                        spacing=12,
                        run_spacing=12,
                        scroll=ft.ScrollMode.AUTO,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            showcase_card(orientation)
                            for orientation in ft.ScrollbarOrientation
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
