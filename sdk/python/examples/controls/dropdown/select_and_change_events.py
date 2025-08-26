import flet as ft


def main(page: ft.Page):
    colors = [
        ft.Colors.RED,
        ft.Colors.BLUE,
        ft.Colors.YELLOW,
        ft.Colors.PURPLE,
        ft.Colors.LIME,
    ]

    def get_options():
        options = []
        for color in colors:
            options.append(
                ft.DropdownOption(
                    key=color.value,
                    content=ft.Text(
                        value=color.value,
                        color=color,
                    ),
                    leading_icon=ft.Icon(ft.Icons.PALETTE, color=color),
                )
            )
        return options

    def dropdown_select(e):
        e.control.color = e.control.value
        display_value.value = f"VALUE changed to {e.control.value}"

    def dropdown_change(e):
        display_text.value = f"TEXT changed to {e.control.text}"

    page.scroll = ft.ScrollMode.AUTO
    page.add(
        display_value := ft.Text(),
        display_text := ft.Text(),
        ft.Dropdown(
            editable=True,
            label="Color",
            width=float("inf"),
            options=get_options(),
            on_select=dropdown_select,
            on_change=dropdown_change,
        ),
    )


ft.run(main)
