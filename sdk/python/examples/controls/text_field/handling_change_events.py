import flet as ft


def main(page: ft.Page):
    def handle_field_change(e: ft.Event[ft.TextField]):
        message.value = e.control.value
        page.update()

    page.add(
        ft.TextField(
            label="Textbox with 'change' event:",
            on_change=handle_field_change,
        ),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
