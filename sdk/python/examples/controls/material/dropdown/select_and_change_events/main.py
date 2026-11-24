import flet as ft


def main(page: ft.Page):
    colors = [
        ft.Colors.RED,
        ft.Colors.BLUE,
        ft.Colors.YELLOW,
        ft.Colors.PURPLE,
        ft.Colors.LIME,
    ]

    def get_options() -> list[ft.DropdownOption]:
        options: list[ft.DropdownOption] = []
        for color in colors:
            options.append(
                ft.DropdownOption(
                    key=color.value,
                    content=ft.Text(value=color.value, color=color),
                    leading_icon=ft.Icon(ft.Icons.PALETTE, color=color),
                )
            )
        return options

    display_value = ft.Text()
    display_text = ft.Text()

    def dropdown_select(e: ft.Event[ft.Dropdown]):
        e.control.color = e.control.value
        display_value.value = f"VALUE changed to {e.control.value}"

    def dropdown_text_change(e: ft.Event[ft.Dropdown]):
        display_text.value = f"TEXT changed to {e.control.text}"

    page.scroll = ft.ScrollMode.AUTO
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    display_value,
                    display_text,
                    ft.Dropdown(
                        key="select_change_dropdown",
                        editable=True,
                        label="Color",
                        width=float("inf"),
                        options=get_options(),
                        on_select=dropdown_select,
                        on_text_change=dropdown_text_change,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
