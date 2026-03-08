from typing import Optional

import flet as ft


def parse_optional_bool(value: Optional[str]):
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title="Scrollbar Dataclass Showcase")

    thumb_visibility = ft.Dropdown(
        label="thumb_visibility",
        value="none",
        options=[
            ft.dropdown.Option("none", "None (theme/default)"),
            ft.dropdown.Option("true", "True"),
            ft.dropdown.Option("false", "False"),
        ],
    )
    track_visibility = ft.Dropdown(
        label="track_visibility",
        value="none",
        options=[
            ft.dropdown.Option("none", "None (theme/default)"),
            ft.dropdown.Option("true", "True"),
            ft.dropdown.Option("false", "False"),
        ],
    )
    interactive = ft.Dropdown(
        label="interactive",
        value="none",
        options=[
            ft.dropdown.Option("none", "None (platform default)"),
            ft.dropdown.Option("true", "True"),
            ft.dropdown.Option("false", "False"),
        ],
    )
    orientation = ft.Dropdown(
        label="orientation",
        value="none",
        options=[ft.dropdown.Option("none", "None (auto side)")]
        + [ft.dropdown.Option(o.value, o.name) for o in ft.ScrollbarOrientation],
    )
    use_thickness = ft.Checkbox(label="Set thickness", value=False)
    thickness_value = ft.Slider(min=0, max=20, divisions=20, value=8, label="{value}")
    use_radius = ft.Checkbox(label="Set radius", value=False)
    radius_value = ft.Slider(min=0, max=20, divisions=20, value=8, label="{value}")

    code_preview = ft.TextField(
        label="Generated Scrollbar()",
        read_only=True,
        multiline=True,
        min_lines=4,
        max_lines=8,
    )
    current_mode_hint = ft.Text(size=12, color=ft.Colors.ON_SURFACE_VARIANT)
    preview_title = ft.Text(weight=ft.FontWeight.BOLD)
    preview_viewport = ft.Container(
        height=260,
        border=ft.Border.all(1, ft.Colors.OUTLINE),
        border_radius=8,
        padding=8,
    )

    def parse_orientation():
        if orientation.value == "none":
            return None
        return ft.ScrollbarOrientation(orientation.value)

    def build_scrollbar() -> ft.Scrollbar:
        thickness = float(thickness_value.value) if use_thickness.value else None
        radius = float(radius_value.value) if use_radius.value else None
        return ft.Scrollbar(
            thumb_visibility=parse_optional_bool(thumb_visibility.value),
            track_visibility=parse_optional_bool(track_visibility.value),
            interactive=parse_optional_bool(interactive.value),
            thickness=thickness,
            radius=radius,
            orientation=parse_orientation(),
        )

    def build_scrollbar_code(scrollbar: ft.Scrollbar) -> str:
        args: list[str] = []
        if scrollbar.thumb_visibility is not None:
            args.append(f"thumb_visibility={scrollbar.thumb_visibility}")
        if scrollbar.track_visibility is not None:
            args.append(f"track_visibility={scrollbar.track_visibility}")
        if scrollbar.interactive is not None:
            args.append(f"interactive={scrollbar.interactive}")
        if scrollbar.thickness is not None:
            thickness = (
                int(scrollbar.thickness)
                if float(scrollbar.thickness).is_integer()
                else scrollbar.thickness
            )
            args.append(f"thickness={thickness}")
        if scrollbar.radius is not None:
            radius = (
                int(scrollbar.radius)
                if float(scrollbar.radius).is_integer()
                else scrollbar.radius
            )
            args.append(f"radius={radius}")
        if scrollbar.orientation is not None:
            args.append(
                f"orientation=ft.ScrollbarOrientation.{scrollbar.orientation.name}"
            )

        if not args:
            return "ft.Scrollbar()"

        return "ft.Scrollbar(\n" + "".join([f"    {arg},\n" for arg in args]) + ")"

    def build_preview_content(scrollbar: ft.Scrollbar) -> tuple[str, ft.Control]:
        selected_orientation = scrollbar.orientation
        is_horizontal = selected_orientation in (
            ft.ScrollbarOrientation.TOP,
            ft.ScrollbarOrientation.BOTTOM,
        )
        if is_horizontal:
            return (
                "Horizontal preview (TOP/BOTTOM orientation)",
                ft.Row(
                    spacing=8,
                    scroll=scrollbar,
                    controls=[
                        ft.Container(
                            width=110,
                            height=80,
                            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            alignment=ft.Alignment.CENTER,
                            content=ft.Text(f"Tile {i + 1}"),
                        )
                        for i in range(18)
                    ],
                ),
            )

        return (
            "Vertical preview (None/LEFT/RIGHT orientation)",
            ft.Column(
                spacing=4,
                scroll=scrollbar,
                controls=[ft.Text(f"Item {i + 1}") for i in range(40)],
            ),
        )

    def mode_hint(scrollbar: ft.Scrollbar) -> str:
        if scrollbar.thickness == 0:
            return "Equivalent legacy mode: ScrollMode.HIDDEN"

        thumb = scrollbar.thumb_visibility
        thickness = scrollbar.thickness
        mobile_default_thickness = (
            4.0 if page.platform.is_mobile() and not page.web else None
        )

        if thumb is True and thickness == mobile_default_thickness:
            return "Equivalent legacy mode: ScrollMode.ALWAYS"
        if (
            thumb == (not (page.platform.is_mobile() and not page.web))
            and thickness == mobile_default_thickness
        ):
            return "Equivalent legacy mode: ScrollMode.ADAPTIVE"
        if thumb is None and thickness == mobile_default_thickness:
            return "Equivalent legacy mode: ScrollMode.AUTO"
        return "Custom configuration (no exact ScrollMode equivalent)"

    def update_preview(_=None):
        thickness_value.disabled = not use_thickness.value
        radius_value.disabled = not use_radius.value

        scrollbar = build_scrollbar()
        title, content = build_preview_content(scrollbar)
        preview_title.value = title
        preview_viewport.content = content
        code_preview.value = build_scrollbar_code(scrollbar)
        current_mode_hint.value = mode_hint(scrollbar)
        page.update()

    dropdowns = [thumb_visibility, track_visibility, interactive, orientation]
    for c in dropdowns:
        c.on_select = update_preview

    controls_with_on_change = [use_thickness, thickness_value, use_radius, radius_value]
    for c in controls_with_on_change:
        c.on_change = update_preview

    page.add(
        ft.Text(
            "Interactive playground for the Scrollbar dataclass. Change each property "
            "and inspect the live result."
        ),
        ft.Row(
            wrap=True,
            spacing=12,
            run_spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=360,
                    padding=12,
                    border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text("Configuration", weight=ft.FontWeight.BOLD),
                            thumb_visibility,
                            track_visibility,
                            interactive,
                            orientation,
                            use_thickness,
                            thickness_value,
                            use_radius,
                            radius_value,
                        ],
                    ),
                ),
                ft.Container(
                    width=420,
                    padding=12,
                    border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                    border_radius=10,
                    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                    content=ft.Column(
                        spacing=10,
                        controls=[
                            ft.Text("Live preview", weight=ft.FontWeight.BOLD),
                            preview_title,
                            preview_viewport,
                            current_mode_hint,
                            code_preview,
                        ],
                    ),
                ),
            ],
        ),
    )

    update_preview()


ft.run(main)
