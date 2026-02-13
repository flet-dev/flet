import flet as ft


def main(page: ft.Page):
    page.padding = 0

    page.add(
        ft.PageView(
            expand=True,
            viewport_fraction=0.9,
            on_change=lambda e: print(f"Currently viewing page {int(e.data)}"),
            selected_index=1,
            horizontal=True,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.INDIGO_400,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text("Welcome", size=40, weight=ft.FontWeight.BOLD),
                            ft.Text("Swipe to see what PageView can do."),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.PINK_300,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.ANIMATION, size=72),
                            ft.Text(
                                "Viewport fraction lets you peek at the next slide."
                            ),
                        ],
                    ),
                ),
                ft.Container(
                    bgcolor=ft.Colors.TEAL_300,
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.TOUCH_APP, size=72),
                            ft.Text("Use on_change to respond to page swipes."),
                        ],
                    ),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
