import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.GestureDetector(
                    on_tap=lambda _: print("TAP!"),
                    multi_tap_touches=3,
                    on_multi_tap=lambda e: print("MULTI TAP:", e.correct_touches),
                    on_multi_long_press=lambda _: print("Multi tap long press"),
                ),
                ft.TransparentPointer(
                    content=ft.Container(
                        content=ft.ElevatedButton("Test button"),
                        padding=50,
                    )
                ),
            ],
        )
    )


ft.run(main)
