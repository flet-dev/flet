import flet as ft


async def main(page: ft.Page):
    print("Test mode:", page.test)
    page.window.width = 400
    page.add(ft.Text("Hello, world!"))


if __name__ == "__main__":
    ft.run(main)
