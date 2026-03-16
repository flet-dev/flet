from dataclasses import field

import flet as ft


@ft.control
class Message(ft.Container):
    author: str = ""
    body: str = ""
    border: ft.Border = field(default_factory=lambda: ft.Border.all(1, ft.Colors.BLACK))
    border_radius: ft.BorderRadius = field(
        default_factory=lambda: ft.BorderRadius.all(10)
    )
    bgcolor: ft.Colors = ft.Colors.GREEN_200
    padding: ft.PaddingValue = 10
    expand: bool = True
    expand_loose: bool = True

    def init(self):
        self.content = ft.Column(
            controls=[
                ft.Text(self.author, weight=ft.FontWeight.BOLD),
                ft.Text(self.body),
            ],
        )


def main(page: ft.Page):
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

    page.add(
        ft.Container(
            content=chat,
            width=300,
            height=500,
        )
    )


if __name__ == "__main__":
    ft.run(main)
