import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Text("Plain text with default style"),
        ft.Text("Selectable plain text with default style", selectable=True),
        ft.Text(
            value="Some text",
            selectable=True,
            size=30,
            spans=[
                ft.TextSpan(
                    text="here goes italic",
                    style=ft.TextStyle(italic=True, size=20, color=ft.Colors.GREEN),
                    spans=[
                        ft.TextSpan(
                            text="bold and italic",
                            style=ft.TextStyle(weight=ft.FontWeight.BOLD),
                        ),
                        ft.TextSpan(
                            text="just italic",
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
                    text="underlined and clickable",
                    style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    on_click=lambda e: print(f"Clicked span: {e.control}"),
                    on_enter=lambda e: print(f"Entered span: {e.control}"),
                    on_exit=lambda e: print(f"Exited span: {e.control}"),
                ),
                ft.TextSpan(text=" "),
                ft.TextSpan(
                    text="underlined red wavy",
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.UNDERLINE,
                        decoration_color=ft.Colors.RED,
                        decoration_style=ft.TextDecorationStyle.WAVY,
                    ),
                    on_enter=lambda e: print(f"Entered span: {e.control}"),
                    on_exit=lambda e: print(f"Exited span: {e.control}"),
                ),
                ft.TextSpan(text=" "),
                ft.TextSpan(
                    text="overlined blue",
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.OVERLINE, decoration_color="blue"
                    ),
                ),
                ft.TextSpan(text=" "),
                ft.TextSpan(
                    text="overlined and underlined",
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.OVERLINE
                        | ft.TextDecoration.UNDERLINE
                    ),
                ),
                ft.TextSpan(text=" "),
                ft.TextSpan(
                    text="line through thick",
                    style=ft.TextStyle(
                        decoration=ft.TextDecoration.LINE_THROUGH,
                        decoration_thickness=3,
                    ),
                ),
            ],
        ),
    )

    def handle_link_highlight(e: ft.Event[ft.TextSpan]):
        e.control.style.color = ft.Colors.BLUE
        e.control.update()

    def handle_link_unhighlight(e: ft.Event[ft.TextSpan]):
        e.control.style.color = None
        e.control.update()

    page.add(
        ft.Text(
            disabled=False,
            spans=[
                ft.TextSpan(
                    text="Go to Google",
                    style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE),
                    url="https://google.com",
                    on_enter=handle_link_highlight,
                    on_exit=handle_link_unhighlight,
                )
            ],
        ),
    )


ft.run(main)
