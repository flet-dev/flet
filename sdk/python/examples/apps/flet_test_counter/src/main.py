import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50)

    def increment(e):
        counter.value = str(int(counter.value) + 1)
        counter.update()

    def decrement(e):
        counter.value = str(int(counter.value) - 1)
        counter.update()

    page.add(
        ft.SafeArea(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.IconButton(ft.Icons.REMOVE, key="decrement", on_click=decrement),
                    counter,
                    ft.IconButton(ft.Icons.ADD, key="increment", on_click=increment),
                ],
            )
        )
    )


ft.run(main)
