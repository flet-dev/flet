import flet as ft

name = "Rich text basics"


def example():
    return ft.Column(
        controls=[
            ft.Text("Plain text with default style"),
            ft.Text(
                "Some text",
                size=30,
                spans=[
                    ft.TextSpan(
                        "here goes italic",
                        ft.TextStyle(italic=True, size=20, color=ft.Colors.GREEN),
                        spans=[
                            ft.TextSpan(
                                "bold and italic",
                                ft.TextStyle(weight=ft.FontWeight.BOLD),
                            ),
                            ft.TextSpan(
                                "just italic",
                                spans=[
                                    ft.TextSpan("smaller italic", ft.TextStyle(size=15))
                                ],
                            ),
                        ],
                    )
                ],
            ),
            ft.Text(
                disabled=False,
                spans=[
                    ft.TextSpan(
                        "underlined and clickable",
                        ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                        on_click=lambda e: print("Clicked span"),
                        on_enter=lambda e: print("Entered span"),
                        on_exit=lambda e: print("Exited span"),
                    ),
                    ft.TextSpan(" "),
                    ft.TextSpan(
                        "underlined red wavy",
                        ft.TextStyle(
                            decoration=ft.TextDecoration.UNDERLINE,
                            decoration_color=ft.Colors.RED,
                            decoration_style=ft.TextDecorationStyle.WAVY,
                        ),
                        on_enter=lambda e: print("Entered span"),
                        on_exit=lambda e: print("Exited span"),
                    ),
                    ft.TextSpan(" "),
                    ft.TextSpan(
                        "overlined blue",
                        ft.TextStyle(
                            decoration=ft.TextDecoration.OVERLINE,
                            decoration_color="blue",
                        ),
                    ),
                    ft.TextSpan(" "),
                    ft.TextSpan(
                        "overlined and underlined",
                        ft.TextStyle(
                            decoration=ft.TextDecoration.OVERLINE
                            | ft.TextDecoration.UNDERLINE
                        ),
                    ),
                    ft.TextSpan(" "),
                    ft.TextSpan(
                        "line through thick",
                        ft.TextStyle(
                            decoration=ft.TextDecoration.LINE_THROUGH,
                            decoration_thickness=3,
                        ),
                    ),
                ],
            ),
        ]
    )
