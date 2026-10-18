import flet_shadcn_ui as shad

import flet as ft


def panel(text: str) -> ft.Container:
    return ft.Container(
        alignment=ft.Alignment.CENTER,
        content=ft.Text(text, weight=ft.FontWeight.W_600),
    )


def main(page: ft.Page):
    page.title = "Shadcn Resizable"

    page.add(
        ft.SafeArea(
            content=ft.Container(
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                content=shad.ResizablePanelGroup(
                    width=480,
                    height=220,
                    show_handle=True,
                    panels=[
                        shad.ResizablePanel(
                            default_size=0.5,
                            min_size=0.2,
                            content=panel("One"),
                        ),
                        shad.ResizablePanel(
                            default_size=0.5,
                            min_size=0.2,
                            content=shad.ResizablePanelGroup(
                                vertical=True,
                                panels=[
                                    shad.ResizablePanel(
                                        default_size=0.3, content=panel("Two")
                                    ),
                                    shad.ResizablePanel(
                                        default_size=0.7, content=panel("Three")
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
