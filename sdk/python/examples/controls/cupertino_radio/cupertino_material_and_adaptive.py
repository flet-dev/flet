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
                    ft.CupertinoRadio(
                        value="red",
                        label="Red - Cupertino Radio",
                        active_color=ft.Colors.RED,
                        inactive_color=ft.Colors.RED,
                    ),
                    ft.Radio(
                        value="green",
                        label="Green - Material Radio",
                        fill_color=ft.Colors.GREEN,
                    ),
                    ft.Radio(
                        value="blue",
                        label="Blue - Adaptive Radio",
                        adaptive=True,
                        active_color=ft.Colors.BLUE,
                    ),
                ]
            )
        ),
        ft.Button(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
