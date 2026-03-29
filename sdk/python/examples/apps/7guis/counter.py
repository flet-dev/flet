import flet as ft


def main(page: ft.Page):
    page.title = "7GUIs - Counter"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    count = 0

    def increment(e: ft.Event[ft.Button]):
        nonlocal count
        count += 1
        field.value = str(count)
        field.update()

    page.add(
        ft.SafeArea(
            ft.Container(
                width=420,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.BLUE_GREY_50,
                content=ft.Column(
                    tight=True,
                    spacing=20,
                    controls=[
                        ft.Text(
                            "Counter",
                            size=28,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "A minimal counter with a read-only value and one action.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                field := ft.TextField(
                                    value=str(count),
                                    read_only=True,
                                    width=120,
                                    text_align=ft.TextAlign.RIGHT,
                                    bgcolor=ft.Colors.SURFACE,
                                    border_radius=14,
                                ),
                                ft.FilledButton(
                                    "Increment",
                                    icon=ft.Icons.ADD,
                                    on_click=increment,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
