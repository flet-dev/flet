import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            width=480,
            padding=10,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
            border_radius=10,
            content=ft.Row(
                controls=[
                    ft.TextField(hint_text="Enter your name", expand=True),
                    ft.Button("Join chat"),
                ]
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
