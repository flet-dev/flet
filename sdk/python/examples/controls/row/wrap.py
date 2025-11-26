import flet as ft


def main(page: ft.Page):
    def generate_items(count: int):
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
        row.width = float(e.control.value)
        row.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Change the row width to see how child items wrap onto multiple rows:"
                ),
                ft.Slider(
                    min=0,
                    max=page.window.width,
                    divisions=20,
                    value=page.window.width,
                    label="{value}",
                    on_change=handle_slider_change,
                ),
            ]
        ),
        row := ft.Row(
            wrap=True,
            spacing=10,
            run_spacing=10,
            controls=generate_items(30),
            width=page.window.width,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
