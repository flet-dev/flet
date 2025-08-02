import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_vertical_change(e: ft.Event[ft.Slider]):
        segmented_button.controls[1].padding = ft.Padding.only(
            top=e.control.value, bottom=e.control.value
        )
        page.update()

    def handle_horizontal_change(e: ft.Event[ft.Slider]):
        segmented_button.controls[2].padding = ft.Padding.only(
            left=e.control.value, right=e.control.value
        )
        page.update()

    page.add(
        segmented_button := ft.CupertinoSegmentedButton(
            selected_index=1,
            selected_color=ft.Colors.RED_400,
            unselected_color=ft.Colors.GREY_400,
            on_change=lambda e: print(f"selected_index: {e.data}"),
            controls=[
                ft.Text("All"),
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=30, horizontal=0),
                    content=ft.Text("None"),
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=0, horizontal=30),
                    content=ft.Text("Some"),
                ),
            ],
        ),
        ft.Text("Vertical padding button 1: "),
        ft.Slider(
            label="{value}",
            min=0,
            max=50,
            divisions=50,
            value=30,
            on_change=handle_vertical_change,
        ),
        ft.Text("Horizontal padding button 2:"),
        ft.Slider(
            label="{value}",
            min=0,
            max=50,
            divisions=50,
            value=30,
            on_change=handle_horizontal_change,
        ),
        ft.Text(
            value="*note that padding changes to one segment can effect padding on other segments*",
            theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
            color=ft.Colors.ORANGE_ACCENT,
        ),
    )


ft.run(main)
