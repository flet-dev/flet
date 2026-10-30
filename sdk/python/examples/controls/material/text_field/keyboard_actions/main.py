import flet as ft


def main(page: ft.Page):
    def send(e: ft.Event[ft.TextField]):
        status.value = f"Sent from {name.value} <{email.value}>: {message.value}"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    name := ft.TextField(
                        key="name",
                        label="Name",
                        text_input_action=ft.TextInputAction.NEXT,
                    ),
                    email := ft.TextField(
                        key="email",
                        label="Email",
                        keyboard_type=ft.KeyboardType.EMAIL,
                        text_input_action=ft.TextInputAction.NEXT,
                    ),
                    message := ft.TextField(
                        key="message",
                        label="Message",
                        text_input_action=ft.TextInputAction.SEND,
                        on_submit=send,
                    ),
                    status := ft.Text(),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
