import flet as ft


def main(page: ft.Page):
    page.title = "Containers with different background color"

    page.add(
        ft.Container(
            content=ft.Text("Container_1"),
            bgcolor="#FFCC0000",
            padding=5,
        ),
        ft.Container(
            content=ft.Text("Container_2"),
            bgcolor="#CC0000",
            padding=5,
        ),
        ft.Container(
            content=ft.Text("Container_3"),
            bgcolor=ft.Colors.RED,
            padding=5,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
