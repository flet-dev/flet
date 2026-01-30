import flet as ft


def main(page: ft.Page):
    def handle_layout(e: ft.LayoutEvent[ft.Container]):
        e.control.content.value = f"{int(e.width)} x {int(e.height)}"

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.BLUE_ACCENT,
            content=ft.Text(color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            layout_interval=100,
            on_layout=handle_layout,
        )
    )


ft.run(main)
