import flet as ft


def main(page: ft.Page):
    def button_clicked(e):
        print("transparent pointer button clicked")

    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.GestureDetector(
                    on_tap=lambda _: print("TAP!"),
                    multi_tap_touches=3,
                    on_multi_tap=lambda e: print("MULTI TAP:", e.global_position),
                    on_multi_long_press=lambda _: print("Multi tap long press"),
                ),
                ft.TransparentPointer(
                    content=ft.Container(
                        content=ft.Button("Test button", on_click=button_clicked),
                        padding=50,
                    )
                ),
            ],
        )
    )


ft.run(main)
