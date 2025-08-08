import flet as ft


def main(page: ft.Page):
    def animate_container(e: ft.Event[ft.ElevatedButton]):
        c1.top = 20
        c1.left = 200
        c2.top = 100
        c2.left = 40
        c3.top = 180
        c3.left = 100
        page.update()

    page.add(
        ft.Stack(
            height=400,
            controls=[
                c1 := ft.Container(
                    width=50, height=50, bgcolor="red", animate_position=1000
                ),
                c2 := ft.Container(
                    width=50,
                    height=50,
                    bgcolor="green",
                    top=60,
                    left=0,
                    animate_position=500,
                ),
                c3 := ft.Container(
                    width=50,
                    height=50,
                    bgcolor="blue",
                    top=120,
                    left=0,
                    animate_position=1000,
                ),
            ],
        ),
        ft.ElevatedButton("Animate!", on_click=animate_container),
    )


ft.run(main)
