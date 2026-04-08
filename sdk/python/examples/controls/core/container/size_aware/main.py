import flet as ft


def main(page: ft.Page):
    def handle_size_change(e: ft.LayoutSizeChangeEvent[ft.Container]):
        e.control.content.value = f"{int(e.width)} x {int(e.height)}"

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.BLUE_ACCENT,
                size_change_interval=100,
                on_size_change=handle_size_change,
                content=ft.Text(color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
