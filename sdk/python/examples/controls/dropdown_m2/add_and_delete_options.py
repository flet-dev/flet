import flet as ft


def main(page: ft.Page):
    def find_option(option_name):
        for option in dropdown.options:
            if option_name == option.key:
                return option
        return None

    def handle_addition(e: ft.Event[ft.Button]):
        dropdown.options.append(ft.dropdownm2.Option(input_field.value))
        dropdown.value = input_field.value
        input_field.value = ""
        page.update()

    def handle_deletion(e: ft.Event[ft.OutlinedButton]):
        option = find_option(dropdown.value)
        if option is not None:
            dropdown.options.remove(option)
            # d.value = None
            page.update()

    page.add(
        dropdown := ft.DropdownM2(options=[], color=ft.Colors.BLUE_400),
        ft.Row(
            controls=[
                input_field := ft.TextField(hint_text="Enter item name"),
                ft.Button(content="Add", on_click=handle_addition),
                ft.OutlinedButton(
                    content="Delete selected",
                    on_click=handle_deletion,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.RED),
                ),
            ]
        ),
    )


ft.run(main)
