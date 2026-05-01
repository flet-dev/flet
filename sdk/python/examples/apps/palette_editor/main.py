import flet as ft

ft.context.disable_auto_update()


def color_band(
    label: str,
    background: ft.ColorValue,
    foreground: ft.ColorValue,
    *,
    width: int,
    height: int,
    on_click=None,
) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=background,
        padding=ft.Padding.symmetric(horizontal=12),
        alignment=ft.Alignment.CENTER_LEFT,
        ink=True,
        on_click=on_click,
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
    title: str | None = None,
    hint: str | None = None,
    on_color_click=None,
) -> ft.Container:
    return ft.Container(
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    visible=title is not None or hint is not None,
                    height=25,
                    padding=ft.Padding.only(left=8, right=2),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(title or "", weight=ft.FontWeight.W_600),
                            ft.Container(
                                visible=hint is not None,
                                content=ft.IconButton(
                                    icon=ft.Icons.INFO_OUTLINE,
                                    icon_size=14,
                                    tooltip=ft.Tooltip(
                                        message=hint or "",
                                        bgcolor=ft.Colors.SURFACE_BRIGHT,
                                        padding=ft.Padding.symmetric(
                                            horizontal=12, vertical=8
                                        ),
                                        prefer_below=False,
                                        vertical_offset=8,
                                        text_style=ft.TextStyle(
                                            color=ft.Colors.ON_SURFACE,
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ),
                *[
                    color_band(
                        label,
                        background,
                        foreground,
                        width=width,
                        height=height,
                        on_click=on_color_click(label) if on_color_click else None,
                    )
                    for label, background, foreground in items
                ],
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
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme=ft.ColorScheme())
    # page.window.width = 420
    # page.window.height = 460
    swatch_width = 250
    swatch_height = 40
    preview_heading = "Palette preview"
    preview_body = (
        "Controls on this side use the current theme so you can compare "
        "tokens with real UI."
    )
    selected_color_heading = ft.Text("Color editor", weight=ft.FontWeight.W_600)
    selected_color_text = ft.Text("Choose a color role to edit.")

    def close_color_editor(_):
        color_editor_pane.visible = False
        page.update()

    color_editor_pane = ft.Container(
        visible=False,
        width=swatch_width,
        padding=ft.Padding.only(left=8, right=8),
        content=ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            padding=16,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                spacing=12,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            selected_color_heading,
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_size=16,
                                tooltip="Close color editor",
                                on_click=close_color_editor,
                            ),
                        ],
                    ),
                    selected_color_text,
                ],
            ),
        ),
    )
    color_role_by_label = {
        "PRIMARY": "primary",
        "ON_PRIMARY": "on_primary",
        "PRIMARY_CONTAINER": "primary_container",
        "ON_PRIMARY_CONTAINER": "on_primary_container",
        "SECONDARY": "secondary",
        "ON_SECONDARY": "on_secondary",
        "SECONDARY_CONTAINER": "secondary_container",
        "ON_SECONDARY_CONTAINER": "on_secondary_container",
    }

    def on_color_click(label: str):
        def handler(_):
            color_role = color_role_by_label[label]
            setattr(page.theme.color_scheme, color_role, ft.Colors.GREEN)
            selected_color_heading.value = f"{label} editor"
            selected_color_text.value = f"{label} color changed to GREEN."
            color_editor_pane.visible = True
            page.update()

        return handler

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
                                        title="Primary roles",
                                        hint=(
                                            "Use primary roles for the most\n"
                                            "prominent components across the UI,\n"
                                            "such as the FAB,\n"
                                            "high-emphasis buttons, and active states."
                                        ),
                                        on_color_click=on_color_click,
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
                                        title="Secondary roles",
                                        hint=(
                                            "Use secondary roles for less prominent\n"
                                            "components in the UI such as filter chips."
                                        ),
                                        on_color_click=on_color_click,
                                    ),
                                ],
                            ),
                        ),
                        color_editor_pane,
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
