import flet as ft
import flet.canvas as cv


def example(page):
    class State:
        x: float
        y: float

    state = State()
    state.color = "black"

    colors = [
        "red",
        "yellow",
        "blue",
        "green",
        "orange",
        "purple",
        "pink",
        "lime",
        "black",
        "white",
    ]

    color_buttons = []

    def color_changed(e):
        state.color = e.control.bgcolor
        for color_button in color_buttons:
            color_button.border = ft.border.all(1, ft.Colors.BLACK12)
            color_button.update()
        e.control.border = ft.border.all(3)
        e.control.update()

    for color in colors:
        color_buttons.append(
            ft.Container(
                width=30,
                height=30,
                border_radius=30,
                bgcolor=color,
                border=ft.border.all(1, ft.Colors.BLACK12),
                on_click=color_changed,
            )
        )

    def pan_start(e: ft.DragStartEvent):
        state.x = e.local_x
        state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        cp.shapes.append(
            cv.Line(
                state.x,
                state.y,
                e.local_x,
                e.local_y,
                paint=ft.Paint(
                    stroke_width=5,
                    color=state.color,
                    stroke_cap=ft.StrokeCap.ROUND,
                    stroke_join=ft.StrokeJoin.ROUND,
                ),
            )
        )
        cp.update()
        state.x = e.local_x
        state.y = e.local_y

    cp = cv.Canvas(
        [
            cv.Fill(ft.Paint(color=ft.Colors.WHITE)),
        ],
        content=ft.Container(
            ft.GestureDetector(
                on_pan_start=pan_start,
                on_pan_update=pan_update,
                drag_interval=10,
            ),
            border_radius=5,
            border=ft.border.all(2, ft.Colors.BLACK38),
        ),
        expand=False,
    )

    return ft.SafeArea(
        ft.Column(
            controls=[
                ft.Row(
                    controls=color_buttons, alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Container(
                    cp,
                    border_radius=5,
                    expand=True,
                ),
            ],
        ),
        expand=True,
    )


def main(page: ft.Page):
    page.title = "Free-hand drawing tool"
    page.window_width = 390
    page.window_height = 844
    page.add(example(page))


if __name__ == "__main__":
    ft.run(main)
