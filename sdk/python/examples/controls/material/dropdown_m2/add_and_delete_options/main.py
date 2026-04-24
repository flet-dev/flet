import flet as ft


def main(page: ft.Page):
    dropdown = ft.DropdownM2(options=[], color=ft.Colors.BLUE_400)
    input_field = ft.TextField(hint_text="Enter item name")

    def find_option(option_name: str):
        for option in dropdown.options:
            if option_name == option.key:
                return option
        return None

    def handle_addition(_: ft.Event[ft.Button]):
        dropdown.options.append(ft.dropdownm2.Option(input_field.value))
        dropdown.value = input_field.value
        input_field.value = ""
        dropdown.update()
        input_field.update()

    def handle_deletion(_: ft.Event[ft.OutlinedButton]):
        option = find_option(dropdown.value)
        if option is not None:
            dropdown.options.remove(option)
            dropdown.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    dropdown,
                    ft.Row(
                        controls=[
                            input_field,
                            ft.Button(content="Add", on_click=handle_addition),
                            ft.OutlinedButton(
                                content="Delete selected",
                                on_click=handle_deletion,
                                style=ft.ButtonStyle(bgcolor=ft.Colors.RED),
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
