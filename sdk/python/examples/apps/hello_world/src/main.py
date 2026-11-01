import flet as ft


def main(page: ft.Page):
    page.add(ft.SafeArea(content=ft.Text("Hello, world!")))


if __name__ == "__main__":
    ft.run(main)
