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
        row.spacing = int(e.control.value)
        row.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("Spacing between items"),
                ft.Slider(
                    key="slider",
                    min=0,
                    max=50,
                    divisions=50,
                    value=0,
                    label="{value}",
                    on_change=handle_slider_change,
                ),
            ]
        ),
        row := ft.Row(
            spacing=0, controls=generate_items(10), scroll=ft.ScrollMode.AUTO
        ),
    )


if __name__ == "__main__":
    ft.run(main)
