import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0")

    page.add(
        result,
        ft.Button(text="AC"),
        ft.Button(text="+/-"),
        ft.Button(text="%"),
        ft.Button(text="/"),
        ft.Button(text="7"),
        ft.Button(text="8"),
        ft.Button(text="9"),
        ft.Button(text="*"),
        ft.Button(text="4"),
        ft.Button(text="5"),
        ft.Button(text="6"),
        ft.Button(text="-"),
        ft.Button(text="1"),
        ft.Button(text="2"),
        ft.Button(text="3"),
        ft.Button(text="+"),
        ft.Button(text="0"),
        ft.Button(text="."),
        ft.Button(text="="),
    )


ft.run(main)
