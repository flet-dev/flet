import flet as ft

HEIGHT = 400


def main(page: ft.Page):
    def items(count: int):
        return [
            ft.Container(
                content=ft.Text(value=str(i)),
                alignment=ft.Alignment.CENTER,
                width=30,
                height=30,
                bgcolor=ft.Colors.AMBER,
                border_radius=ft.BorderRadius.all(5),
            )
            for i in range(1, count + 1)
        ]

    def handle_slider_change(e: ft.Event[ft.Slider]):
        col.height = float(e.control.value)
        col.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text(
                    "Change the column height to see how child items wrap onto multiple columns:"
                ),
                ft.Slider(
                    min=0,
                    max=HEIGHT,
                    divisions=20,
                    value=HEIGHT,
                    label="{value}",
                    width=500,
                    on_change=handle_slider_change,
                ),
            ]
        ),
        ft.Container(
            bgcolor=ft.Colors.TRANSPARENT,
            content=(
                col := ft.Column(
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    controls=items(10),
                    height=HEIGHT,
                )
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
