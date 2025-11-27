import flet as ft


def main(page: ft.Page):
    def animate(e: ft.Event[ft.Button]):
        e.control.rotate = 0.1 if e.data else 0
        page.update()

    page.add(
        ft.Button(
            content="Hover over me, I'm animated!",
            rotate=0,
            animate_rotation=100,
            on_hover=animate,
            on_click=lambda e: page.add(ft.Text("Clicked! Try a long press!")),
            on_long_press=lambda e: page.add(ft.Text("I knew you could do it!")),
        )
    )


if __name__ == "__main__":
    ft.run(main)
