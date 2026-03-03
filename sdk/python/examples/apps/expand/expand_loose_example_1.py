import flet as ft


class Message(ft.Container):
    def __init__(self, author, body):
        super().__init__()
        self.content = ft.Column(
            controls=[
                ft.Text(author, weight=ft.FontWeight.BOLD),
                ft.Text(body),
            ],
        )
        self.border = ft.Border.all(1, ft.Colors.BLACK)
        self.border_radius = ft.BorderRadius.all(10)
        self.bgcolor = ft.Colors.GREEN_200
        self.padding = 10
        self.expand = True
        self.expand_loose = True


def main(page: ft.Page):
    page.window.width = 393
    page.window.height = 600
    page.window.always_on_top = False

    chat = ft.ListView(
        padding=10,
        spacing=10,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body="Hi, how are you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Hi I am good thanks, how about you?",
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.START,
                controls=[
                    Message(
                        author="John",
                        body=(
                            "Lorem Ipsum is simply dummy text of the printing and "
                            "typesetting industry. Lorem Ipsum has been the industry's "
                            "standard dummy text ever since the 1500s, when an unknown "
                            "printer took a galley of type and scrambled it to make a "
                            "type specimen book."
                        ),
                    ),
                ],
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.END,
                controls=[
                    Message(
                        author="Jake",
                        body="Thank you!",
                    ),
                ],
            ),
        ],
    )

    page.add(chat)


if __name__ == "__main__":
    ft.run(main)
