import flet as ft

name = "Animate container"


def example():
    c = ft.Container(
        width=200,
        height=200,
        bgcolor="red",
        animate=ft.Animation(1000, "bounceOut"),
    )

    def animate_container(e):
        c.width = 100 if c.width == 200 else 200
        c.height = 100 if c.height == 200 else 200
        c.bgcolor = "blue" if c.bgcolor == "red" else "red"
        c.update()

    return ft.Column(
        controls=[c, ft.ElevatedButton("Animate container", on_click=animate_container)]
    )
