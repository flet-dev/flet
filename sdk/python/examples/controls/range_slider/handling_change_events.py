import flet as ft


def main(page: ft.Page):
    page.scroll = ft.ScrollMode.AUTO

    def handle_slider_change_start(e: ft.Event[ft.RangeSlider]):
        print(f"on_change_start: {e.control.start_value}, {e.control.end_value}")

    def handle_slider_change(e: ft.Event[ft.RangeSlider]):
        print(f"on_change: {e.control.start_value}, {e.control.end_value}")

    def handle_slider_change_end(e: ft.Event[ft.RangeSlider]):
        print(f"on_change_end: {e.control.start_value}, {e.control.end_value}")
        message.value = f"on_change_end: {e.control.start_value}, {e.control.end_value}"
        page.update()

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Range slider with events",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=30),
                ft.RangeSlider(
                    divisions=100,
                    min=0,
                    max=100,
                    start_value=10,
                    end_value=20,
                    on_change_start=handle_slider_change_start,
                    on_change=handle_slider_change,
                    on_change_end=handle_slider_change_end,
                    label="{value}%",
                ),
                message := ft.Text(),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
