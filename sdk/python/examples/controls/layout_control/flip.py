import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 20

    def toggle_x(e: ft.Event[ft.Button]):
        card.flip.flip_x = not card.flip.flip_x
        page.update()

    def toggle_y(e: ft.Event[ft.Button]):
        card.flip.flip_y = not card.flip.flip_y
        page.update()

    page.add(
        card := ft.Container(
            width=220,
            height=120,
            bgcolor=ft.Colors.BLUE_300,
            border_radius=16,
            alignment=ft.Alignment.CENTER,
            content=ft.Text("Flip me", size=24, weight=ft.FontWeight.BOLD),
            flip=ft.Flip(
                flip_x=False,
                flip_y=False,
                origin=ft.Offset(110, 60),
                filter_quality=ft.FilterQuality.MEDIUM,
            ),
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Button("Toggle X", on_click=toggle_x),
                ft.Button("Toggle Y", on_click=toggle_y),
            ],
        ),
    )


ft.run(main)
