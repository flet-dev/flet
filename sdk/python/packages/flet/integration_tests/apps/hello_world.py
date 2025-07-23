import flet as ft


async def main(page: ft.Page):
    page.add(ft.Text("Hello, world!"))


if __name__ == "__main__":
    ft.run(main)
