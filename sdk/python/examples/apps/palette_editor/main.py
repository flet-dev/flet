import flet as ft

ft.context.disable_auto_update()


def color_band(
    label: str,
    background: ft.ColorValue,
    foreground: ft.ColorValue,
    *,
    width: int,
    height: int,
) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=background,
        padding=ft.Padding.symmetric(horizontal=12),
        alignment=ft.Alignment.CENTER_LEFT,
        content=ft.Text(
            label,
            color=foreground,
        ),
    )


def color_group(
    items: list[tuple[str, ft.ColorValue, ft.ColorValue]],
    *,
    width: int,
    height: int,
) -> ft.Container:
    return ft.Container(
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                color_band(label, background, foreground, width=width, height=height)
                for label, background, foreground in items
            ],
        ),
    )


def main(page: ft.Page):
    page.title = "Palette Editor"
    page.bgcolor = ft.Colors.SURFACE
    page.padding = 14
    # page.window.width = 420
    # page.window.height = 460
    swatch_width = 250
    swatch_height = 40

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                content=ft.Row(
                    expand=True,
                    spacing=0,
                    controls=[
                        ft.Container(
                            width=swatch_width,
                            alignment=ft.Alignment.TOP_LEFT,
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=8,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                                controls=[
                                    color_group(
                                        [
                                            (
                                                "PRIMARY",
                                                ft.Colors.PRIMARY,
                                                ft.Colors.ON_PRIMARY,
                                            ),
                                            (
                                                "ON_PRIMARY",
                                                ft.Colors.ON_PRIMARY,
                                                ft.Colors.PRIMARY,
                                            ),
                                            (
                                                "PRIMARY_CONTAINER",
                                                ft.Colors.PRIMARY_CONTAINER,
                                                ft.Colors.ON_PRIMARY_CONTAINER,
                                            ),
                                            (
                                                "ON_PRIMARY_CONTAINER",
                                                ft.Colors.ON_PRIMARY_CONTAINER,
                                                ft.Colors.PRIMARY_CONTAINER,
                                            ),
                                        ],
                                        width=swatch_width,
                                        height=swatch_height,
                                    ),
                                    color_group(
                                        [
                                            (
                                                "SECONDARY",
                                                ft.Colors.SECONDARY,
                                                ft.Colors.ON_SECONDARY,
                                            ),
                                            (
                                                "ON_SECONDARY",
                                                ft.Colors.ON_SECONDARY,
                                                ft.Colors.SECONDARY,
                                            ),
                                            (
                                                "SECONDARY_CONTAINER",
                                                ft.Colors.SECONDARY_CONTAINER,
                                                ft.Colors.ON_SECONDARY_CONTAINER,
                                            ),
                                            (
                                                "ON_SECONDARY_CONTAINER",
                                                ft.Colors.ON_SECONDARY_CONTAINER,
                                                ft.Colors.SECONDARY_CONTAINER,
                                            ),
                                        ],
                                        width=swatch_width,
                                        height=swatch_height,
                                    ),
                                ],
                            ),
                        ),
                        ft.VerticalDivider(
                            width=24, thickness=1, color=ft.Colors.OUTLINE_VARIANT
                        ),
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                expand=True,
                                scroll=ft.ScrollMode.AUTO,
                                controls=[
                                    ft.Container(
                                        height=1200,
                                        bgcolor=ft.Colors.GREY_300,
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
