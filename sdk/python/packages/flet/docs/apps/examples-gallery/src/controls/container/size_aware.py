import flet as ft
import flet.canvas as cv


class SizeAwareContainer(cv.Canvas):
    def __init__(self, color, expand):
        super().__init__(expand=expand)
        self.size = ft.Text()
        self.content = ft.Container(
            content=self.size,
            alignment=ft.Alignment.CENTER,
            bgcolor=color,
        )
        self.resize_interval = 100
        self.on_resize = self.canvas_resize

    def canvas_resize(self, e):
        self.size.value = f"{int(e.width)} x {int(e.height)}"
        self.update()


def main(page: ft.Page):
    page.add(
        ft.Row(
            expand=2,
            controls=[
                SizeAwareContainer(ft.Colors.RED, expand=2),
                SizeAwareContainer(ft.Colors.GREEN, expand=4),
            ],
        ),
        ft.Row(
            expand=3,
            controls=[
                SizeAwareContainer(ft.Colors.YELLOW, expand=2),
                SizeAwareContainer(ft.Colors.BLUE, expand=4),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
