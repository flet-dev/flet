import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    slider_value = ft.Text("0.0")
    slider_status = ft.Text()

    def handle_change_start(_: ft.Event[ft.CupertinoSlider]):
        slider_status.value = "Sliding"

    def handle_change(e: ft.Event[ft.CupertinoSlider]):
        slider_value.value = str(e.control.value)

    def handle_change_end(_: ft.Event[ft.CupertinoSlider]):
        slider_status.value = "Finished sliding"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    slider_value,
                    ft.CupertinoSlider(
                        divisions=20,
                        min=0,
                        max=100,
                        active_color=ft.Colors.PURPLE,
                        thumb_color=ft.Colors.PURPLE,
                        on_change_start=handle_change_start,
                        on_change_end=handle_change_end,
                        on_change=handle_change,
                    ),
                    slider_status,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
