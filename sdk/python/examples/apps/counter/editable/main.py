import flet as ft

ft.context.disable_auto_update()


def main(page: ft.Page):
    page.title = "Counter"
    txt_number = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                            txt_number,
                            ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                        ]
                    )
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
