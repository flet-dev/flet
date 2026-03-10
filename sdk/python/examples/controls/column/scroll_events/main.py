import flet as ft


def main(page: ft.Page):
    def handle_column_scroll(e: ft.OnScrollEvent):
        print(e)

    page.add(
        ft.Container(
            border=ft.Border.all(1),
            content=ft.Column(
                spacing=10,
                height=200,
                width=200,
                scroll=ft.ScrollMode.ALWAYS,
                on_scroll=handle_column_scroll,
                controls=[
                    ft.Text(f"Text line {i}", key=ft.ScrollKey(str(i)))
                    for i in range(0, 50)
                ],
            ),
        ),
    )


ft.run(main)
