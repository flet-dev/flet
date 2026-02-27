import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.TextField(hint_text="Enter your name", expand=True),
                ft.Button("Join chat"),
            ]
        )
    )


ft.run(main)
