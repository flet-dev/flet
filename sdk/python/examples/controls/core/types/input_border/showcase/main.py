import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Outline",
                        border=ft.OutlineInputBorder(),
                        hint_text="The default border",
                    ),
                    ft.TextField(
                        label="Underline",
                        border=ft.UnderlineInputBorder(),
                        hint_text="A line along the bottom edge",
                    ),
                    ft.TextField(
                        label="Underline filled",
                        border=ft.UnderlineInputBorder(),
                        filled=True,
                        hint_text="The radius rounds the fill's top corners",
                    ),
                    ft.TextField(
                        label="None",
                        border=ft.InputBorder.none(),
                        filled=True,
                        hint_text="Draws no border at all",
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
