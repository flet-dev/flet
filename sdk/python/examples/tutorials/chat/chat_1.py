import flet as ft


def main(page: ft.Page):
    chat = ft.Column()
    new_message = ft.TextField()

    def send_click(e):
        chat.controls.append(ft.Text(new_message.value))
        new_message.value = ""
        page.update()

    page.add(
        chat,
        ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=send_click)]),
    )


ft.app(target=main)
