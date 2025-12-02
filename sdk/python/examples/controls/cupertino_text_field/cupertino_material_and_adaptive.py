import flet as ft


def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Material text field",
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
        ft.CupertinoTextField(
            placeholder_text="Cupertino text field",
            placeholder_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
        ft.TextField(
            adaptive=True,
            label="Adaptive text field",
            label_style=ft.TextStyle(color=ft.Colors.GREY_400),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
