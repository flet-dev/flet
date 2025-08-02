import flet as ft


def main(page: ft.Page):
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

    def handle_dropdown_change(e: ft.Event[ft.Dropdown]):
        e.control.color = e.control.value
        page.update()

    page.add(
        ft.Dropdown(
            editable=True,
            label="Color",
            options=get_options(),
            on_change=handle_dropdown_change,
        )
    )


ft.run(main)
