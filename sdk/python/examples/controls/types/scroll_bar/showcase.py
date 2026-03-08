from typing import Union

import flet as ft


def showcase_card(
    title: str, scroll: Union[ft.ScrollMode, ft.Scrollbar]
) -> ft.Container:
    return ft.Container(
        width=320,
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Container(
                    height=210,
                    border=ft.Border.all(1, ft.Colors.OUTLINE),
                    border_radius=8,
                    padding=8,
                    content=ft.Column(
                        spacing=4,
                        scroll=scroll,
                        controls=[ft.Text(f"Item {i + 1}") for i in range(35)],
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title="ScrollBar Showcase")

    page.add(
        ft.Text("Legacy ScrollMode and new Scrollbar object can be mixed."),
        ft.Row(
            wrap=True,
            spacing=12,
            run_spacing=12,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                showcase_card("Legacy: ScrollMode.AUTO", ft.ScrollMode.AUTO),
                showcase_card(
                    "Custom: ALWAYS + thick + track",
                    ft.Scrollbar(
                        mode=ft.ScrollMode.ALWAYS,
                        thickness=12,
                        radius=8,
                        thumb_visibility=True,
                        track_visibility=True,
                    ),
                ),
                showcase_card(
                    "Custom: ADAPTIVE + non-interactive",
                    ft.Scrollbar(
                        mode=ft.ScrollMode.ADAPTIVE,
                        orientation=ft.ScrollbarOrientation.LEFT,
                        interactive=False,
                        thickness=6,
                    ),
                ),
            ],
        ),
    )


ft.run(main)
