import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Text("Default slider:"),
        ft.Slider(),
        ft.Text("Default disabled slider:"),
        ft.Slider(disabled=True),
    )


if __name__ == "__main__":
    ft.run(main)
