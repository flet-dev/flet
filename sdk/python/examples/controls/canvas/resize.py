import flet as ft
import flet.canvas as cv


def main(page: ft.Page):
    def paint_resize(e: cv.CanvasResizeEvent):
        print("On resize:", e.width, e.height)
        canvas.shapes[0].x2 = e.width
        canvas.shapes[0].y2 = e.height
        canvas.shapes[1].y1 = e.height
        canvas.shapes[1].x2 = e.width
        canvas.update()

    page.add(
        ft.Container(
            width=float("inf"),
            expand=True,
            content=(
                canvas := cv.Canvas(
                    resize_interval=10,
                    on_resize=paint_resize,
                    shapes=[
                        cv.Line(x1=0, y1=0, x2=100, y2=100),
                        cv.Line(x1=0, y1=100, x2=100, y2=0),
                    ],
                )
            ),
        )
    )


ft.run(main)
