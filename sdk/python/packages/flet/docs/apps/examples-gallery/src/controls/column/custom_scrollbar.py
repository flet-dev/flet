import flet as ft


def main(page: ft.Page):
    page.theme = ft.Theme(
        scrollbar_theme=ft.ScrollbarTheme(
            track_color={
                ft.ControlState.HOVERED: ft.Colors.AMBER,
                ft.ControlState.DEFAULT: ft.Colors.TRANSPARENT,
            },
            track_visibility=True,
            track_border_color=ft.Colors.BLUE,
            thumb_visibility=True,
            thumb_color={
                ft.ControlState.HOVERED: ft.Colors.RED,
                ft.ControlState.DEFAULT: ft.Colors.GREY_300,
            },
            thickness=30,
            radius=15,
            main_axis_margin=5,
            cross_axis_margin=10,
        )
    )

    fake_messages = [
        ft.Container(
            ft.Text(f"Message {i}", size=16, weight=ft.FontWeight.W_500),
            bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.BLUE_200),
            border_radius=8,
            padding=10,
        )
        for i in range(1, 31)
    ]

    page.add(
        ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        controls=fake_messages,
                        spacing=10,
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                    ),
                    width=320,
                    height=420,
                    bgcolor=ft.Colors.with_opacity(0.15, ft.Colors.AMBER_200),
                    padding=15,
                    border_radius=12,
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.run(main)
