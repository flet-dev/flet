import ast

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
    selected_border_color = (
        getattr(ft.Colors, f"{label}_900")
        if hasattr(ft.Colors, f"{label}_900")
        else ft.Colors.BLACK
    )
    return ft.Container(
        width=28,
        height=28,
        border_radius=14,
        bgcolor=color,
        border=ft.Border.all(
            2 if selected else 1,
            selected_border_color if selected else ft.Colors.OUTLINE_VARIANT,
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
                    ft.IconButton(
                        icon=ft.Icons.UPLOAD,
                        tooltip="Import",
                        on_click=open_import_dialog,
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
            color_group(
                [
                    ("TERTIARY", ft.Colors.TERTIARY, ft.Colors.ON_TERTIARY),
                    ("ON_TERTIARY", ft.Colors.ON_TERTIARY, ft.Colors.TERTIARY),
                    (
                        "TERTIARY_CONTAINER",
                        ft.Colors.TERTIARY_CONTAINER,
                        ft.Colors.ON_TERTIARY_CONTAINER,
                    ),
                    (
                        "ON_TERTIARY_CONTAINER",
                        ft.Colors.ON_TERTIARY_CONTAINER,
                        ft.Colors.TERTIARY_CONTAINER,
                    ),
                ],
                width=swatch_width,
                height=swatch_height,
                title="Tertiary roles",
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
        "TERTIARY": "tertiary",
        "ON_TERTIARY": "on_tertiary",
        "TERTIARY_CONTAINER": "tertiary_container",
        "ON_TERTIARY_CONTAINER": "on_tertiary_container",
    }
    color_role_export_order = list(dict.fromkeys(color_role_by_label.values()))
    import_format_hint = (
        "Use this format:\n"
        "ft.Theme(\n"
        "  color_scheme=ft.ColorScheme(\n"
        "      primary='#ff87581b',\n"
        "      on_primary=ft.Colors.WHITE,\n"
        "  )\n"
        ")"
    )

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

    def get_attribute_path(node: ast.AST) -> list[str] | None:
        parts: list[str] = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.append(current.id)
            return list(reversed(parts))
        return None

    def parse_import_color_value(node: ast.AST) -> ft.ColorValue:
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value
        attr_path = get_attribute_path(node)
        if attr_path and len(attr_path) == 3 and attr_path[:2] == ["ft", "Colors"]:
            color_name = attr_path[2]
            if hasattr(ft.Colors, color_name):
                return getattr(ft.Colors, color_name)
        raise ValueError

    def parse_import_theme_code(code: str) -> dict[str, ft.ColorValue]:
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            raise ValueError from exc

        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
            raise ValueError

        theme_call = tree.body[0].value
        if not isinstance(theme_call, ast.Call):
            raise ValueError

        theme_path = get_attribute_path(theme_call.func)
        if theme_path != ["ft", "Theme"]:
            raise ValueError

        color_scheme_call: ast.Call | None = None
        for keyword in theme_call.keywords:
            if keyword.arg == "color_scheme" and isinstance(keyword.value, ast.Call):
                color_scheme_call = keyword.value
                break
        if color_scheme_call is None:
            raise ValueError

        color_scheme_path = get_attribute_path(color_scheme_call.func)
        if color_scheme_path != ["ft", "ColorScheme"]:
            raise ValueError

        parsed_overrides: dict[str, ft.ColorValue] = {}
        for keyword in color_scheme_call.keywords:
            if keyword.arg not in color_role_export_order:
                raise ValueError
            parsed_overrides[keyword.arg] = parse_import_color_value(keyword.value)

        return parsed_overrides

    async def copy_export_theme(_):
        export_code = build_export_code()
        print(export_code)
        await ft.Clipboard().set(export_code)
        export_copy_button.icon = ft.Icons.CHECK
        page.update()

    export_code_text = ft.TextField(
        multiline=True,
        min_lines=12,
        max_lines=16,
        read_only=True,
        value="",
    )
    export_copy_button = ft.IconButton(
        icon=ft.Icons.CONTENT_COPY,
        tooltip="Copy to clipboard",
        on_click=copy_export_theme,
    )
    export_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Export palette"),
        content=ft.Container(
            width=520,
            content=export_code_text,
        ),
        actions=[
            export_copy_button,
            ft.TextButton("Close", on_click=lambda _: page.pop_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    import_code_text = ft.TextField(
        multiline=True,
        min_lines=12,
        max_lines=16,
        value="",
        hint_text=import_format_hint,
    )
    import_error_text = ft.Text(
        "",
        color=ft.Colors.ERROR,
        visible=False,
    )

    def close_import_dialog(_):
        page.pop_dialog()
        page.update()

    def import_theme(_):
        try:
            parsed_overrides = parse_import_theme_code(import_code_text.value or "")
        except ValueError:
            import_error_text.value = (
                f"Couldn't parse theme code.\n\n{import_format_hint}"
            )
            import_error_text.visible = True
            page.update()
            return

        theme_color_overrides.clear()
        theme_color_overrides.update(parsed_overrides)
        rebuild_theme()
        if selected_role["attr"] is not None:
            set_selected_material_from_value(
                theme_color_overrides.get(selected_role["attr"])
            )
        else:
            selected_material_color["label"] = None
            selected_material_color["value"] = None
            selected_shade["label"] = None
            selected_shade["value"] = None
            update_hex_picker(None)
        rebuild_left_pane_controls()
        rebuild_material_color_controls()
        rebuild_shade_controls()
        import_error_text.visible = False
        page.pop_dialog()
        page.update()

    import_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Import palette"),
        content=ft.Container(
            width=520,
            content=ft.Column(
                tight=True,
                spacing=12,
                controls=[import_code_text, import_error_text],
            ),
        ),
        actions=[
            ft.TextButton("Import", on_click=import_theme),
            ft.TextButton("Close", on_click=close_import_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def export_theme(_):
        export_code_text.value = build_export_code()
        export_copy_button.icon = ft.Icons.CONTENT_COPY
        page.show_dialog(export_dialog)
        page.update()

    def open_import_dialog(_):
        import_code_text.value = ""
        import_error_text.value = ""
        import_error_text.visible = False
        page.show_dialog(import_dialog)
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
                    vertical_alignment=ft.CrossAxisAlignment.START,
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
                                                    ft.FilledTonalButton(
                                                        "Filled tonal button"
                                                    ),
                                                    ft.OutlinedButton(
                                                        "Outlined button"
                                                    ),
                                                    ft.TextButton("Text button"),
                                                    ft.Button("Button"),
                                                ],
                                            ),
                                            ft.FloatingActionButton(
                                                icon=ft.Icons.PALETTE
                                            ),
                                            ft.SegmentedButton(
                                                selected=["grid"],
                                                segments=[
                                                    ft.Segment(
                                                        value="list",
                                                        icon=ft.Icon(
                                                            ft.Icons.VIEW_LIST
                                                        ),
                                                        label=ft.Text("List"),
                                                    ),
                                                    ft.Segment(
                                                        value="grid",
                                                        icon=ft.Icon(
                                                            ft.Icons.GRID_VIEW
                                                        ),
                                                        label=ft.Text("Grid"),
                                                    ),
                                                ],
                                            ),
                                        ),
                                        showcase_section(
                                            "Chips",
                                            ft.Row(
                                                wrap=True,
                                                spacing=12,
                                                run_spacing=12,
                                                controls=[
                                                    ft.Chip(
                                                        label=ft.Text("Filter chip"),
                                                        on_select=lambda e: None,
                                                    ),
                                                    ft.Chip(
                                                        label=ft.Text("Assist chip"),
                                                        leading=ft.Icon(
                                                            ft.Icons.MAP_SHARP
                                                        ),
                                                        on_click=lambda e: None,
                                                    ),
                                                    ft.Chip(
                                                        label=ft.Text("Selected"),
                                                        selected=True,
                                                        on_select=lambda e: None,
                                                    ),
                                                ],
                                            ),
                                        ),
                                        showcase_section(
                                            "Secondary roles",
                                            ft.Row(
                                                wrap=True,
                                                spacing=12,
                                                run_spacing=12,
                                                controls=[
                                                    ft.Container(
                                                        bgcolor=ft.Colors.SECONDARY,
                                                        padding=12,
                                                        border_radius=12,
                                                        content=ft.Text(
                                                            "SECONDARY",
                                                            color=ft.Colors.ON_SECONDARY,
                                                        ),
                                                    ),
                                                    ft.Container(
                                                        bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                                        padding=12,
                                                        border_radius=12,
                                                        content=ft.Text(
                                                            "SECONDARY_CONTAINER",
                                                            color=ft.Colors.ON_SECONDARY_CONTAINER,
                                                        ),
                                                    ),
                                                ],
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
