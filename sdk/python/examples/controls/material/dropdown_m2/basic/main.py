import flet as ft


def main(page: ft.Page):
    message = ft.Text()

    dd = ft.DropdownM2(
        width=100,
        value="Green",
        options=[
            ft.dropdownm2.Option("Red"),
            ft.dropdownm2.Option("Green"),
            ft.dropdownm2.Option("Blue"),
        ],
    )

    def handle_button_click(_: ft.Event[ft.Button]):
        message.value = f"Dropdown value is: {dd.value}"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    dd,
                    ft.Button(content="Submit", on_click=handle_button_click),
                    message,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
