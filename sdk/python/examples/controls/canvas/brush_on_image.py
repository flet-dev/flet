import flet as ft
import flet.canvas as cv


class State:
    x: float
    y: float


state = State()


def main(page: ft.Page):
    page.title = "Flet Brush"

    def handle_pan_start(e: ft.DragStartEvent):
        state.x = e.local_position.x
        state.y = e.local_position.y

    def handle_pan_update(e: ft.DragUpdateEvent):
        canvas.shapes.append(
            cv.Line(
                x1=state.x,
                y1=state.y,
                x2=e.local_position.x,
                y2=e.local_position.y,
                paint=ft.Paint(stroke_width=3),
            )
        )
        canvas.update()
        state.x = e.local_position.x
        state.y = e.local_position.y

    page.add(
        ft.Container(
            border_radius=5,
            expand=True,
            content=ft.Stack(
                expand=True,
                controls=[
                    ft.Image(
                        src="https://picsum.photos/200/300",
                        fit=ft.BoxFit.FILL,
                        width=float("inf"),
                    ),
                    canvas := cv.Canvas(
                        expand=False,
                        content=ft.GestureDetector(
                            on_pan_start=handle_pan_start,
                            on_pan_update=handle_pan_update,
                            drag_interval=10,
                        ),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
