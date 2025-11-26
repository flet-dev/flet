import flet as ft


def main(page: ft.Page):
    gradient1 = ft.LinearGradient(
        begin=ft.Alignment.TOP_CENTER,
        end=ft.Alignment.BOTTOM_CENTER,
        colors=[ft.Colors.GREEN, ft.Colors.BLUE],
        stops=[0.5, 1.0],
    )
    gradient2 = ft.RadialGradient(
        center=ft.Alignment.TOP_LEFT,
        radius=1.0,
        colors=[ft.Colors.YELLOW, ft.Colors.DEEP_ORANGE_900],
        tile_mode=ft.GradientTileMode.CLAMP,
    )

    message = ft.Text("Animate me!")

    def animate_container(e: ft.Event[ft.Button]):
        message.value = (
            "Animate me back!" if message.value == "Animate me!" else "Animate me!"
        )
        container.width = 150 if container.width == 250 else 250
        container.height = 150 if container.height == 250 else 250
        container.gradient = gradient2 if container.gradient == gradient1 else gradient1
        if container.alignment == ft.Alignment.TOP_LEFT:
            container.alignment = ft.Alignment.BOTTOM_RIGHT
        else:
            container.alignment = ft.Alignment.TOP_LEFT
        container.border_radius = 30 if container.border_radius == 10 else 10
        container.border = (
            ft.Border.all(width=2, color=ft.Colors.BLACK)
            if container.border == ft.Border.all(width=2, color=ft.Colors.BLUE)
            else ft.Border.all(width=2, color=ft.Colors.BLUE)
        )
        container.update()

    page.add(
        container := ft.Container(
            content=message,
            width=250,
            height=250,
            gradient=gradient2,
            alignment=ft.Alignment.TOP_LEFT,
            animate=ft.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_OUT),
            border=ft.Border.all(width=2, color=ft.Colors.BLUE),
            border_radius=10,
            padding=10,
        ),
        ft.Button("Animate container", on_click=animate_container),
    )


if __name__ == "__main__":
    ft.run(main)
