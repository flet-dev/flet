from datetime import time

from palette_constants import (
    COLOR_ROLE_BY_LABEL,
    LIGHT_SEED_COLOR,
    MATERIAL_COLORS,
)
from palette_theme_io import build_export_code, parse_import_theme_code
from palette_ui import (
    build_left_pane_controls,
    build_preview_tabs,
    material_color_circle,
    material_shade_swatch,
)

import flet as ft
from flet_color_pickers import HueRingPicker

ft.context.disable_auto_update()


def main(page: ft.Page):
    page.title = "Palette Editor"
    page.bgcolor = ft.Colors.SURFACE
    page.padding = 14
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed=LIGHT_SEED_COLOR)
    page.dark_theme = ft.Theme(color_scheme_seed=LIGHT_SEED_COLOR)
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
    light_theme_color_overrides: dict[str, ft.ColorValue] = {}
    dark_theme_color_overrides: dict[str, ft.ColorValue] = {}

    def close_color_editor(_):
        color_editor_pane.visible = False
        page.update()

    def rebuild_theme():
        page.theme = ft.Theme(
            color_scheme_seed=LIGHT_SEED_COLOR,
            color_scheme=ft.ColorScheme(**light_theme_color_overrides),
        )
        page.dark_theme = ft.Theme(
            color_scheme_seed=LIGHT_SEED_COLOR,
            color_scheme=ft.ColorScheme(**dark_theme_color_overrides),
        )

    def current_theme_color_overrides() -> dict[str, ft.ColorValue]:
        return (
            light_theme_color_overrides
            if page.theme_mode == ft.ThemeMode.LIGHT
            else dark_theme_color_overrides
        )

    def update_hex_picker(color_value: ft.ColorValue | None):
        hex_color_picker.color = color_value

    def get_current_role_color_value(role_attr: str | None) -> ft.ColorValue | None:
        if role_attr is None:
            return None
        override = current_theme_color_overrides().get(role_attr)
        if override is not None:
            return override
        token_name = role_attr.upper()
        if hasattr(ft.Colors, token_name):
            return getattr(ft.Colors, token_name)
        return None

    def set_selected_material_from_value(color_value: ft.ColorValue | None):
        if color_value is None:
            selected_material_color["label"] = None
            selected_material_color["value"] = None
            selected_shade["label"] = None
            selected_shade["value"] = None
            update_hex_picker(None)
            return

        for label, value in MATERIAL_COLORS:
            if value == color_value:
                selected_material_color["label"] = label
                selected_material_color["value"] = value
                selected_shade["label"] = None
                selected_shade["value"] = None
                update_hex_picker(color_value)
                return

        for material_label, material_value in MATERIAL_COLORS:
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
            for label, color in MATERIAL_COLORS
        ]

    def rebuild_left_pane_controls():
        left_pane_controls.controls = build_left_pane_controls(
            selected_label=selected_role["label"],
            swatch_width=swatch_width,
            swatch_height=swatch_height,
            theme_mode=page.theme_mode,
            on_color_click=on_color_click,
            on_reset=reset_from_seed,
            on_export=export_theme,
            on_import=open_import_dialog,
            on_toggle_theme=toggle_theme_mode,
        )

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
            current_theme_color_overrides()[selected_role["attr"]] = color_value
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
            current_theme_color_overrides()[selected_role["attr"]] = shade_value
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
        current_theme_color_overrides()[selected_role["attr"]] = e.data
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
    preview_time_text = ft.Text(
        value="19:30",
    )

    def handle_preview_time_change(e: ft.Event[ft.TimePicker]):
        preview_time_text.value = str(preview_time_picker.value.strftime("%H:%M"))
        page.update()

    preview_time_picker = ft.TimePicker(
        value=time(hour=19, minute=30),
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        entry_mode=ft.TimePickerEntryMode.DIAL,
        on_change=handle_preview_time_change,
    )
    import_format_hint = (
        "Use this format:\n"
        "ft.Theme(\n"
        "  color_scheme=ft.ColorScheme(\n"
        "      primary='#ff87581b',\n"
        "      on_primary=ft.Colors.WHITE,\n"
        "  )\n"
        ")"
    )

    def on_color_click(label: str):
        def handler(_):
            selected_role["label"] = label
            selected_role["attr"] = COLOR_ROLE_BY_LABEL[label]
            set_selected_material_from_value(
                get_current_role_color_value(selected_role["attr"])
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
        current_theme_color_overrides().clear()
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

    async def copy_export_theme(_):
        export_code = build_export_code(current_theme_color_overrides())
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

        current_overrides = current_theme_color_overrides()
        current_overrides.clear()
        current_overrides.update(parsed_overrides)
        rebuild_theme()
        if selected_role["attr"] is not None:
            set_selected_material_from_value(
                get_current_role_color_value(selected_role["attr"])
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
        export_code_text.value = build_export_code(current_theme_color_overrides())
        export_copy_button.icon = ft.Icons.CONTENT_COPY
        page.show_dialog(export_dialog)
        page.update()

    def open_import_dialog(_):
        import_code_text.value = ""
        import_error_text.value = ""
        import_error_text.visible = False
        page.show_dialog(import_dialog)
        page.update()

    def open_preview_time_picker(_):
        page.show_dialog(preview_time_picker)
        page.update()

    def toggle_theme_mode(_):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        if selected_role["attr"] is not None:
            set_selected_material_from_value(
                get_current_role_color_value(selected_role["attr"])
            )
            rebuild_material_color_controls()
            rebuild_shade_controls()
        rebuild_left_pane_controls()
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
                                content=build_preview_tabs(
                                    preview_heading=preview_heading,
                                    preview_body=preview_body,
                                    preview_time_text=preview_time_text,
                                    open_preview_time_picker=open_preview_time_picker,
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
