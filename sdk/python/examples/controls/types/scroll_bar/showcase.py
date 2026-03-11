from typing import Optional

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title="Scrollbar Dataclass Showcase")

    def get_scrollbar() -> ft.Scrollbar:
        def str_as_bool(value: Optional[str]) -> Optional[bool]:
            return True if value == "true" else False if value == "false" else None

        return ft.Scrollbar(
            thumb_visibility=str_as_bool(thumb_visibility.value),
            track_visibility=str_as_bool(track_visibility.value),
            interactive=str_as_bool(interactive.value),
            thickness=thickness_value.value if use_thickness.value else None,
            radius=radius_value.value if use_radius.value else None,
            orientation=None
            if orientation.value == "none"
            else ft.ScrollbarOrientation(orientation.value),
        )

    def get_preview_content(scrollbar: ft.Scrollbar) -> tuple[str, ft.Control]:
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

    def update_preview():
        thickness_value.disabled = not use_thickness.value
        radius_value.disabled = not use_radius.value

        scrollbar = get_scrollbar()
        title, content = get_preview_content(scrollbar)
        preview_title.value = title
        preview_viewport.content = content
        page.update()

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
                            thumb_visibility := ft.Dropdown(
                                label="thumb_visibility",
                                value="none",
                                on_select=update_preview,
                                options=[
                                    ft.DropdownOption("none", "None (theme default)"),
                                    ft.DropdownOption("true", "True"),
                                    ft.DropdownOption("false", "False"),
                                ],
                            ),
                            track_visibility := ft.Dropdown(
                                label="track_visibility",
                                value="none",
                                on_select=update_preview,
                                options=[
                                    ft.DropdownOption("none", "None (theme default)"),
                                    ft.DropdownOption("true", "True"),
                                    ft.DropdownOption("false", "False"),
                                ],
                            ),
                            interactive := ft.Dropdown(
                                label="interactive",
                                value="none",
                                on_select=update_preview,
                                options=[
                                    ft.DropdownOption(
                                        "none", "None (platform default)"
                                    ),
                                    ft.DropdownOption("true", "True"),
                                    ft.DropdownOption("false", "False"),
                                ],
                            ),
                            orientation := ft.Dropdown(
                                label="orientation",
                                value="none",
                                options=[ft.DropdownOption("none", "None (auto side)")]
                                + [
                                    ft.DropdownOption(o.value, o.name)
                                    for o in ft.ScrollbarOrientation
                                ],
                            ),
                            use_thickness := ft.Checkbox(
                                label="Set thickness",
                                value=False,
                                on_change=update_preview,
                            ),
                            thickness_value := ft.Slider(
                                min=0,
                                max=20,
                                divisions=20,
                                value=8,
                                label="{value}",
                                on_change=update_preview,
                            ),
                            use_radius := ft.Checkbox(
                                label="Set radius",
                                value=False,
                                on_change=update_preview,
                            ),
                            radius_value := ft.Slider(
                                min=0,
                                max=20,
                                divisions=20,
                                value=8,
                                label="{value}",
                                on_change=update_preview,
                            ),
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
                            preview_title := ft.Text(weight=ft.FontWeight.BOLD),
                            preview_viewport := ft.Container(
                                height=260,
                                border=ft.Border.all(1, ft.Colors.OUTLINE),
                                border_radius=8,
                                padding=8,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    update_preview()


ft.run(main)
