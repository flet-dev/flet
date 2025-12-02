import flet as ft


def main(page: ft.Page):
    page.title = "OutlinedButton Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_button_click(e: ft.Event[ft.OutlinedButton]):
        button.data += 1
        message.value = f"Button clicked {button.data} time(s)"
        page.update()

    button = ft.OutlinedButton(
        content="Button with 'click' event",
        data=0,
        on_click=handle_button_click,
    )
    message = ft.Text()

    page.add(
        ft.Container(
            content=ft.Column(controls=[button, message]),
            alignment=ft.Alignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.run(main)
