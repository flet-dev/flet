import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Text("Slider with value:"),
        ft.Slider(value=0.3),
        ft.Text("Slider with a custom range and label:"),
        ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
    )


if __name__ == "__main__":
    ft.run(main)
