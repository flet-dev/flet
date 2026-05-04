import flet as ft
from flet_color_pickers import HueRingPicker

ft.context.disable_auto_update()

LIGHT_SEED_COLOR = ft.Colors.BLUE


def color_band(
    label: str,
    background: ft.ColorValue,
    foreground: ft.ColorValue,
    *,
    width: int,
    height: int,
    selected: bool = False,
    on_click=None,
) -> ft.Container:
    return ft.Container(
        width=width,
        height=height,
        bgcolor=background,
        border=ft.Border.all(
            2 if selected else 0,
            ft.Colors.BLACK if selected else ft.Colors.TRANSPARENT,
        ),
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
    selected_label: str | None = None,
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
                        selected=selected_label == label,
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


def material_color_circle(
    color: ft.ColorValue, label: str, *, selected: bool = False, on_click=None
) -> ft.Container:
    return ft.Container(
        width=28,
        height=28,
        border_radius=14,
        bgcolor=color,
        border=ft.Border.all(
            2 if selected else 1,
            ft.Colors.BLACK if selected else ft.Colors.OUTLINE_VARIANT,
        ),
        tooltip=label,
        ink=True,
        on_click=on_click,
    )


def material_shade_swatch(
    color: ft.ColorValue, label: str, *, selected: bool = False, on_click=None
) -> ft.Container:
    return ft.Container(
        width=32,
        height=44,
        border_radius=22 if selected else 0,
        bgcolor=color,
        alignment=ft.Alignment.TOP_CENTER,
        padding=ft.Padding.only(top=5),
        tooltip=label,
        ink=True,
        on_click=on_click,
        content=ft.Text(
            label,
            size=11,
            color=ft.Colors.BLACK if label in {"50", "100", "200"} else ft.Colors.WHITE,
        ),
    )


def main(page: ft.Page):
    page.title = "Palette Editor"
    page.bgcolor = ft.Colors.SURFACE
    page.padding = 14
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=LIGHT_SEED_COLOR)
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
    selected_role = {"label": None, "attr": None}
    selected_material_color = {"label": None, "value": None}
    selected_shade = {"label": None, "value": None}
    theme_color_overrides: dict[str, ft.ColorValue] = {}
    material_colors = [
        ("AMBER", ft.Colors.AMBER),
        ("BLACK", ft.Colors.BLACK),
        ("BLUE", ft.Colors.BLUE),
        ("BLUE_GREY", ft.Colors.BLUE_GREY),
        ("BROWN", ft.Colors.BROWN),
        ("CYAN", ft.Colors.CYAN),
        ("DEEP_ORANGE", ft.Colors.DEEP_ORANGE),
        ("DEEP_PURPLE", ft.Colors.DEEP_PURPLE),
        ("GREEN", ft.Colors.GREEN),
        ("GREY", ft.Colors.GREY),
        ("INDIGO", ft.Colors.INDIGO),
        ("LIGHT_BLUE", ft.Colors.LIGHT_BLUE),
        ("LIGHT_GREEN", ft.Colors.LIGHT_GREEN),
        ("LIME", ft.Colors.LIME),
        ("ORANGE", ft.Colors.ORANGE),
        ("PINK", ft.Colors.PINK),
        ("PURPLE", ft.Colors.PURPLE),
        ("RED", ft.Colors.RED),
        ("TEAL", ft.Colors.TEAL),
        ("TRANSPARENT", ft.Colors.TRANSPARENT),
        ("WHITE", ft.Colors.WHITE),
        ("YELLOW", ft.Colors.YELLOW),
    ]

    def close_color_editor(_):
        color_editor_pane.visible = False
        page.update()

    def rebuild_theme():
        page.theme = ft.Theme(
            color_scheme_seed=LIGHT_SEED_COLOR,
            color_scheme=ft.ColorScheme(**theme_color_overrides),
        )

    def update_hex_picker(color_value: ft.ColorValue | None):
        hex_color_picker.color = color_value

    def set_selected_material_from_value(color_value: ft.ColorValue | None):
        if color_value is None:
            selected_material_color["label"] = None
            selected_material_color["value"] = None
            selected_shade["label"] = None
            selected_shade["value"] = None
            update_hex_picker(None)
            return

        for label, value in material_colors:
            if value == color_value:
                selected_material_color["label"] = label
                selected_material_color["value"] = value
                selected_shade["label"] = None
                selected_shade["value"] = None
                update_hex_picker(color_value)
                return

        for material_label, material_value in material_colors:
            for shade_label, shade_value in get_shades(material_label):
                if shade_value == color_value:
                    selected_material_color["label"] = material_label
                    selected_material_color["value"] = material_value
                    selected_shade["label"] = shade_label
                    selected_shade["value"] = shade_value
                    update_hex_picker(color_value)
                    return

        selected_material_color["label"] = None
        selected_material_color["value"] = None
        selected_shade["label"] = None
        selected_shade["value"] = None
        update_hex_picker(color_value)

    def get_shades(color_label: str | None) -> list[tuple[str, ft.ColorValue]]:
        if color_label is None or color_label in {"BLACK", "WHITE", "TRANSPARENT"}:
            return []
        shades: list[tuple[str, ft.ColorValue]] = []
        for shade in [
            "50",
            "100",
            "200",
            "300",
            "400",
            "500",
            "600",
            "700",
            "800",
            "900",
        ]:
            shades.append((shade, getattr(ft.Colors, f"{color_label}_{shade}")))
        accent_name = f"{color_label}_ACCENT"
        if hasattr(ft.Colors, accent_name):
            for shade in ["100", "200", "400", "700"]:
                shades.append(
                    (f"A{shade}", getattr(ft.Colors, f"{accent_name}_{shade}"))
                )
        return shades

    def rebuild_material_color_controls():
        material_color_row.controls = [
            material_color_circle(
                color,
                label,
                selected=selected_material_color["label"] == label,
                on_click=on_material_color_click(label, color),
            )
            for label, color in material_colors
        ]

    def rebuild_left_pane_controls():
        left_pane_controls.controls = [
            ft.Row(
                spacing=8,
                controls=[
                    ft.IconButton(
                        icon=ft.Icons.PALETTE,
                        tooltip="Reset from seed",
                        on_click=reset_from_seed,
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DOWNLOAD,
                        tooltip="Export",
                        on_click=export_theme,
                    ),
                ],
            ),
            color_group(
                [
                    ("PRIMARY", ft.Colors.PRIMARY, ft.Colors.ON_PRIMARY),
                    ("ON_PRIMARY", ft.Colors.ON_PRIMARY, ft.Colors.PRIMARY),
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
                selected_label=selected_role["label"],
                on_color_click=on_color_click,
            ),
            color_group(
                [
                    ("SECONDARY", ft.Colors.SECONDARY, ft.Colors.ON_SECONDARY),
                    ("ON_SECONDARY", ft.Colors.ON_SECONDARY, ft.Colors.SECONDARY),
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
                selected_label=selected_role["label"],
                on_color_click=on_color_click,
            ),
        ]

    def rebuild_shade_controls():
        shades = get_shades(selected_material_color["label"])
        shade_row.visible = len(shades) > 0
        shade_row.controls = [
            material_shade_swatch(
                color,
                label,
                selected=selected_shade["label"] == label,
                on_click=on_shade_click(label, color),
            )
            for label, color in shades
        ]

    def on_material_color_click(color_label: str, color_value: ft.ColorValue):
        def handler(_):
            selected_material_color["label"] = color_label
            selected_material_color["value"] = color_value
            selected_shade["label"] = None
            selected_shade["value"] = None
            update_hex_picker(color_value)
            rebuild_material_color_controls()
            rebuild_shade_controls()
            if selected_role["attr"] is None or selected_role["label"] is None:
                return
            theme_color_overrides[selected_role["attr"]] = color_value
            rebuild_theme()
            selected_color_text.value = (
                f"{selected_role['label']} color changed to {color_label}."
            )
            page.update()

        return handler

    def on_shade_click(shade_label: str, shade_value: ft.ColorValue):
        def handler(_):
            selected_shade["label"] = shade_label
            selected_shade["value"] = shade_value
            update_hex_picker(shade_value)
            rebuild_shade_controls()
            if selected_role["attr"] is None or selected_role["label"] is None:
                return
            theme_color_overrides[selected_role["attr"]] = shade_value
            rebuild_theme()
            selected_color_text.value = (
                f"{selected_role['label']} color changed to "
                f"{selected_material_color['label']} {shade_label}."
            )
            page.update()

        return handler

    def on_hex_color_change(e: ft.ControlEvent):
        if selected_role["attr"] is None or selected_role["label"] is None:
            return
        theme_color_overrides[selected_role["attr"]] = e.data
        set_selected_material_from_value(e.data)
        rebuild_material_color_controls()
        rebuild_shade_controls()
        rebuild_theme()
        selected_color_text.value = (
            f"{selected_role['label']} color changed to {e.data}."
        )
        page.update()

    material_color_row = ft.Row(
        wrap=True,
        spacing=8,
        run_spacing=8,
        controls=[],
    )
    shade_row = ft.Row(
        visible=False,
        scroll=ft.ScrollMode.AUTO,
        spacing=0,
        controls=[],
    )
    left_pane_controls = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=8,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[],
    )
    hex_color_picker = HueRingPicker(
        color=None,
        on_color_change=on_hex_color_change,
        color_picker_height=220,
        enable_alpha=False,
        hue_ring_stroke_width=18,
        picker_area_border_radius=ft.BorderRadius.all(12),
    )
    rebuild_material_color_controls()
    rebuild_shade_controls()

    color_editor_pane = ft.Container(
        visible=False,
        width=swatch_width * 2,
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
                    material_color_row,
                    shade_row,
                    hex_color_picker,
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
    color_role_export_order = list(dict.fromkeys(color_role_by_label.values()))

    def format_color_value(color_value: ft.ColorValue) -> str:
        if hasattr(color_value, "name"):
            return f"ft.Colors.{color_value.name}"
        return repr(color_value)

    def on_color_click(label: str):
        def handler(_):
            selected_role["label"] = label
            selected_role["attr"] = color_role_by_label[label]
            set_selected_material_from_value(
                theme_color_overrides.get(selected_role["attr"])
            )
            selected_color_heading.value = f"{label} editor"
            selected_color_text.value = f"Choose a material color for {label}."
            color_editor_pane.visible = True
            rebuild_left_pane_controls()
            rebuild_material_color_controls()
            rebuild_shade_controls()
            page.update()

        return handler

    def reset_from_seed(_):
        theme_color_overrides.clear()
        selected_role["label"] = None
        selected_role["attr"] = None
        selected_material_color["label"] = None
        selected_material_color["value"] = None
        selected_shade["label"] = None
        selected_shade["value"] = None
        selected_color_heading.value = "Color editor"
        selected_color_text.value = "Choose a color role to edit."
        color_editor_pane.visible = False
        rebuild_left_pane_controls()
        rebuild_material_color_controls()
        rebuild_shade_controls()
        rebuild_theme()
        page.update()

    def build_export_code() -> str:
        lines = ["ft.Theme(", "  color_scheme=ft.ColorScheme("]
        for color_role in color_role_export_order:
            color_value = theme_color_overrides.get(color_role)
            if color_value is None:
                continue
            lines.append(f"      {color_role}={format_color_value(color_value)},")
        lines.append("  )")
        lines.append(")")
        return "\n".join(lines)

    async def copy_export_theme(_):
        export_code = build_export_code()
        print(export_code)
        await ft.Clipboard().set(export_code)

    export_code_text = ft.TextField(
        multiline=True,
        min_lines=12,
        max_lines=16,
        read_only=True,
        value="",
    )
    export_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Export palette"),
        content=ft.Container(
            width=520,
            content=export_code_text,
        ),
        actions=[
            ft.IconButton(
                icon=ft.Icons.CONTENT_COPY,
                tooltip="Copy to clipboard",
                on_click=copy_export_theme,
            ),
            ft.TextButton("Close", on_click=lambda _: page.pop_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def export_theme(_):
        export_code_text.value = build_export_code()
        page.show_dialog(export_dialog)
        page.update()

    rebuild_left_pane_controls()

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
                            content=left_pane_controls,
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
