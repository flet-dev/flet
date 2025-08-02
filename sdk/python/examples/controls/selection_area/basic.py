import flet as ft

TEXT_STYLE = ft.TextStyle(
    size=22,
    weight=ft.FontWeight.W_600,
    decoration=ft.TextDecoration(
        ft.TextDecoration.UNDERLINE | ft.TextDecoration.OVERLINE
    ),
    decoration_style=ft.TextDecorationStyle.WAVY,
)


def main(page: ft.Page):
    page.add(
        ft.SelectionArea(
            content=ft.Column(
                controls=[
                    ft.Text("Selectable text", color=ft.Colors.GREEN, style=TEXT_STYLE),
                    ft.Text("Also selectable", color=ft.Colors.GREEN, style=TEXT_STYLE),
                ]
            )
        )
    )

    page.add(ft.Text("Not selectable", color=ft.Colors.RED, style=TEXT_STYLE))


ft.run(main)
