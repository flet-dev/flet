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


def showcase_section(title: str, *controls: ft.Control) -> ft.Container:
    return ft.Container(
        margin=ft.Margin.only(bottom=16),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    title,
                    # style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                *controls,
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
    preview_heading = "Palette preview"
    preview_body = (
        "Controls on this side use the current theme so you can compare "
        "tokens with real UI."
    )

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
                            padding=ft.Padding.only(left=4),
                            content=ft.Container(
                                expand=True,
                                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                                padding=16,
                                content=ft.Column(
                                    expand=True,
                                    scroll=ft.ScrollMode.AUTO,
                                    spacing=0,
                                    controls=[
                                        ft.Text(
                                            "Example",
                                            # style=ft.TextThemeStyle.HEADLINE_SMALL,
                                        ),
                                        ft.Container(height=16),
                                        showcase_section(
                                            "Buttons",
                                            ft.Row(
                                                wrap=True,
                                                spacing=12,
                                                run_spacing=12,
                                                controls=[
                                                    ft.FilledButton("Filled button"),
                                                    ft.OutlinedButton(
                                                        "Outlined button"
                                                    ),
                                                    ft.TextButton("Text button"),
                                                    ft.Button("Button"),
                                                ],
                                            ),
                                        ),
                                        showcase_section(
                                            "Inputs",
                                            ft.TextField(
                                                label="Theme name",
                                                hint_text="Material 3 palette",
                                                value="Sample scheme",
                                            ),
                                            ft.TextField(
                                                label="Description",
                                                multiline=True,
                                                min_lines=3,
                                                max_lines=5,
                                                value=(
                                                    "This preview shows controls "
                                                    "using the app theme colors."
                                                ),
                                            ),
                                        ),
                                        showcase_section(
                                            "Selection",
                                            ft.Row(
                                                wrap=True,
                                                spacing=16,
                                                run_spacing=12,
                                                controls=[
                                                    ft.Switch(
                                                        label="Use dark mode",
                                                        value=True,
                                                    ),
                                                    ft.Checkbox(
                                                        label="Enable accents",
                                                        value=True,
                                                    ),
                                                ],
                                            ),
                                            ft.RadioGroup(
                                                content=ft.Column(
                                                    spacing=8,
                                                    controls=[
                                                        ft.Radio(
                                                            value="system",
                                                            label="System",
                                                        ),
                                                        ft.Radio(
                                                            value="light",
                                                            label="Light",
                                                        ),
                                                        ft.Radio(
                                                            value="dark",
                                                            label="Dark",
                                                        ),
                                                    ],
                                                ),
                                                value="system",
                                            ),
                                            ft.Slider(value=70, min=0, max=100),
                                        ),
                                        showcase_section(
                                            "Progress",
                                            ft.ProgressBar(value=0.65),
                                            ft.Row(
                                                spacing=16,
                                                controls=[
                                                    ft.ProgressRing(value=0.75),
                                                    ft.FloatingActionButton(
                                                        icon=ft.Icons.PALETTE
                                                    ),
                                                ],
                                            ),
                                        ),
                                        showcase_section(
                                            "Card",
                                            ft.Card(
                                                content=ft.Container(
                                                    padding=16,
                                                    content=ft.Column(
                                                        spacing=12,
                                                        controls=[
                                                            ft.Row(
                                                                spacing=12,
                                                                controls=[
                                                                    ft.Icon(
                                                                        ft.Icons.COLOR_LENS
                                                                    ),
                                                                    ft.Text(
                                                                        preview_heading,
                                                                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                                    ),
                                                                ],
                                                            ),
                                                            ft.Text(preview_body),
                                                            ft.Row(
                                                                spacing=12,
                                                                controls=[
                                                                    ft.FilledButton(
                                                                        "Apply"
                                                                    ),
                                                                    ft.TextButton(
                                                                        "Reset"
                                                                    ),
                                                                ],
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ),
                                        ),
                                    ],
                                ),
                            ),
                        ),
                    ],
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
