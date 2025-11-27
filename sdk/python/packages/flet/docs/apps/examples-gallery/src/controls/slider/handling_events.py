import flet as ft


def main(page: ft.Page):
    def slider_changed(e: ft.Event[ft.Slider]):
        message.value = f"Slider changed to {e.control.value}"
        message.update()

    page.add(
        ft.Text("Slider with 'on_change' event:"),
        ft.Slider(
            key="slider",
            min=0,
            max=100,
            divisions=10,
            label="{value}%",
            on_change=slider_changed,
        ),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
