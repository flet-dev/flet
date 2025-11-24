import flet as ft


def example(page):
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        e.control.page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        e.control.page.update()

    return ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
    )


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.window_width = 390
    page.window_height = 844
    page.add(example(page))


if __name__ == "__main__":
    ft.run(main)
