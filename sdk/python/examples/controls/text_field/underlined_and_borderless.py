import flet as ft


def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Underlined",
            border=ft.InputBorder.UNDERLINE,
            hint_text="Enter text here",
        ),
        ft.TextField(
            label="Underlined filled",
            border=ft.InputBorder.UNDERLINE,
            filled=True,
            hint_text="Enter text here",
        ),
        ft.TextField(
            label="Borderless",
            border=ft.InputBorder.NONE,
            hint_text="Enter text here",
        ),
        ft.TextField(
            label="Borderless filled",
            border=ft.InputBorder.NONE,
            filled=True,
            hint_text="Enter text here",
        ),
    )


if __name__ == "__main__":
    ft.run(main)
