import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.TextField(
                        key="underlined_field",
                        label="Underlined",
                        border=ft.InputBorder.UNDERLINE,
                        hint_text="Enter text here",
                    ),
                    ft.TextField(
                        key="underlined_filled_field",
                        label="Underlined filled",
                        border=ft.InputBorder.UNDERLINE,
                        filled=True,
                        hint_text="Enter text here",
                    ),
                    ft.TextField(
                        key="borderless_field",
                        label="Borderless",
                        border=ft.InputBorder.NONE,
                        hint_text="Enter text here",
                    ),
                    ft.TextField(
                        key="borderless_filled_field",
                        label="Borderless filled",
                        border=ft.InputBorder.NONE,
                        filled=True,
                        hint_text="Enter text here",
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
