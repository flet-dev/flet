import flet as ft


def showcase_card(direction: ft.DismissDirection) -> ft.Container:
    status = ft.Text("Swipe the tile", size=12, color=ft.Colors.ON_SURFACE_VARIANT)

    def create_item() -> ft.Dismissible:
        return ft.Dismissible(
            dismiss_direction=direction,
            on_dismiss=lambda _: on_dismiss(),
            background=ft.Container(
                bgcolor=ft.Colors.GREEN_200,
                alignment=ft.Alignment.CENTER_LEFT,
                padding=10,
                content=ft.Icon(ft.Icons.CHECK, color=ft.Colors.GREEN_900),
            ),
            secondary_background=ft.Container(
                bgcolor=ft.Colors.RED_200,
                alignment=ft.Alignment.CENTER_RIGHT,
                padding=10,
                content=ft.Icon(ft.Icons.DELETE, color=ft.Colors.RED_900),
            ),
            content=ft.Container(
                height=52,
                border_radius=8,
                bgcolor=ft.Colors.SURFACE,
                border=ft.Border.all(1, ft.Colors.OUTLINE),
                alignment=ft.Alignment.CENTER,
                content=ft.Text("Dismiss me"),
            ),
        )

    def on_dismiss():
        slot.content = ft.Container(
            height=52,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Dismissed"),
        )
        status.value = f"Dismissed via {direction.name}"
        slot.update()
        status.update()

    def reset_item(_):
        slot.content = create_item()
        status.value = "Swipe the tile"
        slot.update()
        status.update()

    slot = ft.Container(content=create_item())

    return ft.Container(
        width=360,
        padding=12,
        border=ft.Border.all(1, ft.Colors.RED),
        border_radius=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(direction.name, weight=ft.FontWeight.BOLD),
                status,
                slot,
                ft.Button("Reset", on_click=reset_item),
            ],
        ),
    )


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.appbar = ft.AppBar(title="DismissDirection Showcase")
    page.add(
        ft.Text("Try swipe directions to see which ones are allowed."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(direction) for direction in ft.DismissDirection],
        ),
    )


ft.run(main)
