import flet as ft


def build_card(index: int, color: ft.Colors) -> ft.Container:
    return ft.Container(
        bgcolor=color,
        border_radius=8,
        padding=16,
        content=ft.Column(
            spacing=10,
            controls=[
                ft.Text(f"Card {index}", size=22, weight=ft.FontWeight.BOLD),
                ft.Text("Line 1"),
                ft.Text("Line 2"),
                ft.Text("Line 3"),
                ft.Text("Line 4"),
                ft.Text("Line 5"),
            ],
        ),
    )


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=12,
                controls=[
                    ft.Text(
                        "Resize the window height. The header stays visible while "
                        "the responsive content scrolls."
                    ),
                    ft.ResponsiveRow(
                        expand=True,
                        scroll=ft.ScrollMode.AUTO,
                        spacing=16,
                        run_spacing=16,
                        controls=[
                            ft.Container(
                                col={
                                    ft.ResponsiveRowBreakpoint.XS: 12,
                                    ft.ResponsiveRowBreakpoint.MD: 6,
                                    ft.ResponsiveRowBreakpoint.LG: 4,
                                },
                                content=build_card(
                                    i,
                                    [
                                        ft.Colors.BLUE_50,
                                        ft.Colors.GREEN_50,
                                        ft.Colors.AMBER_50,
                                    ][i % 3],
                                ),
                            )
                            for i in range(1, 10)
                        ],
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
