import flet as ft


def main(page: ft.Page):
    def dropdown_changed(e: ft.Event[ft.DropdownM2]):
        message.value = f"Dropdown changed to {e.control.value}"
        page.update()

    page.add(
        ft.DropdownM2(
            width=200,
            color=ft.Colors.BLUE_GREY_700,
            on_change=dropdown_changed,
            options=[
                ft.dropdownm2.Option("Red"),
                ft.dropdownm2.Option("Green"),
                ft.dropdownm2.Option("Blue"),
            ],
        ),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
