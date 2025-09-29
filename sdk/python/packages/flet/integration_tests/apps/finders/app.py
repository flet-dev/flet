import flet as ft


async def main(page: ft.Page):
    print("Test mode:", page.test)
    page.window.width = 800
    page.add(ft.Text("Hello, world!"))
    page.add(ft.Button("Button_1"))
    page.add(ft.Button("Button_2"))
    page.add(ft.Text("Hello, world!!!"))
    page.add(ft.Text("__world!"))
    page.add(
        ft.Text(
            spans=[
                ft.TextSpan(
                    "Hello, world!",
                    style=ft.TextStyle(weight=ft.FontWeight.BOLD, italic=True),
                )
            ]
        )
    )
    page.add(ft.IconButton(ft.Icons.ADD_A_PHOTO))
    page.add(ft.Checkbox(label="Hello", key=ft.ValueKey("value_key_1")))
    page.add(ft.TextField(label="Full name", key=ft.ScrollKey("scroll_key_1")))
    page.add(ft.Button("Click me", tooltip="Tooltip1"))


if __name__ == "__main__":
    ft.run(main)
