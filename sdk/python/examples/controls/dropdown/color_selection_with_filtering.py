import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def get_options():
        colors = [
            ft.Colors.RED,
            ft.Colors.BLUE,
            ft.Colors.YELLOW,
            ft.Colors.PURPLE,
            ft.Colors.LIME,
        ]
        return [
            ft.DropdownOption(
                key=color.value,
                content=ft.Text(value=color.value, color=color),
            )
            for color in colors
        ]

    def handle_dropdown_select(e: ft.Event[ft.Dropdown]):
        e.control.color = e.control.value
        page.update()

    page.add(
        ft.Dropdown(
            editable=True,
            label="Color",
            options=get_options(),
            on_select=handle_dropdown_select,
        )
    )


ft.run(main)
