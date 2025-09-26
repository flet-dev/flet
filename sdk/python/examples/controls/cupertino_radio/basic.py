import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.ElevatedButton]):
        message.value = f"Your favorite color is:  {group.value}"
        page.update()

    page.add(
        ft.Text("Select your favorite color:"),
        group := ft.RadioGroup(
            content=ft.Column(
                controls=[
                    ft.CupertinoRadio(
                        value="red",
                        label="Red",
                        active_color=ft.Colors.RED_200,
                        inactive_color=ft.Colors.RED_600,
                    ),
                    ft.CupertinoRadio(
                        value="green",
                        label="Green",
                        fill_color=ft.Colors.GREEN,
                    ),
                    ft.CupertinoRadio(
                        value="blue",
                        label="Blue",
                        active_color=ft.Colors.BLUE,
                    ),
                ]
            )
        ),
        ft.ElevatedButton(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
