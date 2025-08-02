import flet as ft


def main(page: ft.Page):
    def handle_page_resize(e: ft.PageResizeEvent):
        pw.value = f"{page.width} px"
        pw.update()

    page.on_resize = handle_page_resize

    pw = ft.Text(text_align=ft.TextAlign.END, style=ft.TextTheme.display_small)
    # page.overlay.append(pw)

    page.add(
        ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Text("Column 1"),
                    padding=5,
                    bgcolor=ft.Colors.YELLOW,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=ft.Text("Column 2"),
                    padding=5,
                    bgcolor=ft.Colors.GREEN,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=ft.Text("Column 3"),
                    padding=5,
                    bgcolor=ft.Colors.BLUE,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
                ft.Container(
                    content=ft.Text("Column 4"),
                    padding=5,
                    bgcolor=ft.Colors.PINK_300,
                    col={"xs": 12, "md": 6, "lg": 3},
                ),
            ],
        ),
        ft.ResponsiveRow(
            run_spacing={"xs": 10},
            controls=[
                ft.TextField(label="TextField 1", col={"md": 4}),
                ft.TextField(label="TextField 2", col={"md": 4}),
                ft.TextField(label="TextField 3", col={"md": 4}),
            ],
        ),
        pw,
    )
    handle_page_resize(None)


ft.run(main)
