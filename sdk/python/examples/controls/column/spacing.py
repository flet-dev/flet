import flet as ft


def main(page: ft.Page):
    def generate_items(count: int):
        """Generates a list of custom Containers with length `count`."""
        return [
            ft.Container(
                content=ft.Text(value=str(i)),
                alignment=ft.Alignment.CENTER,
                width=50,
                height=50,
                bgcolor=ft.Colors.AMBER,
                border_radius=ft.BorderRadius.all(5),
            )
            for i in range(1, count + 1)
        ]

    def handle_slider_change(e: ft.Event[ft.Slider]):
        """Updates the spacing between items based on slider value."""
        column.spacing = int(e.control.value)
        column.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("Spacing between items"),
                ft.Slider(
                    min=0,
                    max=100,
                    divisions=10,
                    value=0,
                    label="{value}",
                    width=500,
                    on_change=handle_slider_change,
                ),
            ]
        ),
        column := ft.Column(spacing=0, controls=generate_items(5)),
    )


ft.run(main)
