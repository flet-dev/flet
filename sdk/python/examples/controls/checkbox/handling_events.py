import flet as ft


def main(page: ft.Page):
    def handle_checkbox_change(e: ft.Event[ft.Checkbox]):
        page.add(ft.Text(f"Checkbox value changed to {e.control.value}"))
        page.update()

    page.add(
        ft.Checkbox(
            label="Checkbox with 'change' event",
            on_change=handle_checkbox_change,
        )
    )


if __name__ == "__main__":
    ft.run(main)
