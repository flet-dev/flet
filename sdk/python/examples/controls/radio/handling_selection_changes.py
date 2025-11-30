import flet as ft


def main(page: ft.Page):
    def handle_selection_change(e: ft.Event[ft.RadioGroup]):
        message.value = f"Your favorite color is:  {e.control.value}"
        page.update()

    page.add(
        ft.Text("Select your favorite color:"),
        ft.RadioGroup(
            on_change=handle_selection_change,
            content=ft.Column(
                controls=[
                    ft.Radio(value="red", label="Red"),
                    ft.Radio(value="green", label="Green"),
                    ft.Radio(value="blue", label="Blue"),
                ]
            ),
        ),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
