import flet as ft

name = "Images Example"


def example():
    img = ft.Image(
        src="logo.svg",
        width=100,
        height=100,
        fit=ft.BoxFit.CONTAIN,
    )
    images = ft.Row(width=600, wrap=False, scroll="always")

    for i in range(0, 30):
        images.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.BoxFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.BorderRadius.all(10),
            )
        )

    return ft.Column(
        # width=400,
        # height=400,
        controls=[
            img,
            images,
        ]
    )
