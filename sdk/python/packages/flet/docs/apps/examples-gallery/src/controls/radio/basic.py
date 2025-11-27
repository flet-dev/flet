import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.Button]):
        message.value = f"Your favorite color is:  {group.value}"
        page.update()

    page.add(
        ft.Text("Select your favorite color:"),
        group := ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.Radio(value="red", label="Red"),
                    ft.Radio(value="green", label="Green"),
                    ft.Radio(value="blue", label="Blue"),
                ]
            )
        ),
        ft.Button(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
