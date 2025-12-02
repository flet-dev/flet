import flet as ft


def main(page: ft.Page):
    def show_menu(e: ft.Event[ft.Button]):
        container.offset = ft.Offset(0, 0)
        container.update()

    def hide_menu(e: ft.Event[ft.IconButton]):
        container.offset = ft.Offset(-2, 0)
        container.update()

    page.overlay.append(
        container := ft.Container(
            left=10,
            top=10,
            width=200,
            height=300,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=5,
            offset=ft.Offset(-2, 0),
            animate_offset=ft.Animation(300, ft.AnimationCurve.EASE_IN),
            content=ft.Column(
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(icon=ft.Icons.CLOSE, on_click=hide_menu)
                        ],
                    ),
                    ft.ListTile(
                        title=ft.Text("Menu A"),
                        on_click=lambda _: print("Menu A clicked"),
                    ),
                    ft.ListTile(
                        title=ft.Text("Menu B"),
                        on_click=lambda _: print("Menu B clicked"),
                    ),
                ]
            ),
        )
    )

    page.add(ft.Button("Show menu", on_click=show_menu))


if __name__ == "__main__":
    ft.run(main)
