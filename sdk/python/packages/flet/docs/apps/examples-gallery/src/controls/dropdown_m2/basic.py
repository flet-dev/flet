import flet as ft


def main(page: ft.Page):
    # page.theme_mode = ft.ThemeMode.DARK

    def handle_button_click(e):
        message.value = f"Dropdown value is:  {dd.value}"
        page.update()

    page.add(
        dd := ft.DropdownM2(
            width=100,
            value="Green",
            options=[
                ft.dropdownm2.Option("Red"),
                ft.dropdownm2.Option("Green"),
                ft.dropdownm2.Option("Blue"),
            ],
        ),
        ft.Button(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
