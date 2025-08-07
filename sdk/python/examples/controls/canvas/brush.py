import flet as ft
import flet.canvas as cv


class State:
    x: float
    y: float


state = State()


def main(page: ft.Page):
    page.title = "Canvas Example"

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

    canvas = cv.Canvas(
        expand=False,
        shapes=[
            cv.Fill(
                ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        begin=(0, 0),
                        end=(600, 600),
                        colors=[ft.Colors.CYAN_50, ft.Colors.GREY],
                    )
                )
            ),
        ],
        content=ft.GestureDetector(
            on_pan_start=handle_pan_start,
            on_pan_update=handle_pan_update,
            drag_interval=10,
        ),
    )

    page.add(
        ft.Container(
            content=canvas,
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )


ft.run(main)
