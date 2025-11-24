import flet as ft

name = "Row wrapping"


def example():
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                ft.Container(
                    content=ft.Text(value=str(i)),
                    alignment=ft.Alignment.CENTER,
                    width=50,
                    height=50,
                    bgcolor=ft.Colors.AMBER,
                    border_radius=ft.BorderRadius.all(5),
                )
            )
        return items

    def slider_change(e):
        row.width = float(e.control.value)
        row.update()

    width_slider = ft.Slider(
        min=0,
        max=500,
        divisions=20,
        value=100,
        label="{value}",
        on_change=slider_change,
    )

    row = ft.Row(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=items(30),
        width=500,
    )

    return ft.Column(
        [
            ft.Text(
                "Change the row width to see how child items wrap onto multiple rows:"
            ),
            width_slider,
            row,
        ]
    )
