import flet as ft


def clip_preview(clip_behavior: ft.ClipBehavior) -> ft.Container:
    return ft.Container(
        width=240,
        height=130,
        border=ft.Border.all(2, ft.Colors.OUTLINE),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE,
        content=ft.Stack(
            clip_behavior=clip_behavior,
            controls=[
                ft.Container(
                    width=160,
                    height=70,
                    left=-25,
                    top=30,
                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
                    border_radius=16,
                ),
                ft.Container(
                    width=90,
                    height=90,
                    left=150,
                    top=-20,
                    bgcolor=ft.Colors.TERTIARY_CONTAINER,
                    border_radius=45,
                ),
                ft.Container(
                    width=90,
                    height=90,
                    left=70,
                    top=22,
                    bgcolor=ft.Colors.SECONDARY,
                    border_radius=45,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.CROP, color=ft.Colors.WHITE),
                ),
            ],
        ),
    )


def showcase_card(clip_behavior: ft.ClipBehavior) -> ft.Container:
    return ft.Container(
        width=280,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(clip_behavior.name, weight=ft.FontWeight.BOLD),
                clip_preview(clip_behavior),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="ClipBehavior Showcase")
    page.add(
        ft.Text("Compare how overflow is clipped for each ClipBehavior value."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(cb) for cb in ft.ClipBehavior],
        ),
    )


ft.run(main)
