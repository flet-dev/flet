import flet as ft


def main(page: ft.Page):
    message = ft.Text()

    group = ft.RadioGroup(
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
            ],
        )
    )

    def handle_button_click(_: ft.Event[ft.Button]):
        message.value = f"Your favorite color is: {group.value}"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Select your favorite color:"),
                    group,
                    ft.Button(content="Submit", on_click=handle_button_click),
                    message,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
