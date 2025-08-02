import flet as ft

name = "Change container theme colors"


def example():
    def change_primary_color(e):
        container.theme = ft.Theme(
            color_scheme=ft.ColorScheme(primary=primary_color.value)
        )
        primary_color.value = ""
        container.update()
        primary_color.update()

    container = ft.Container(
        width=200,
        height=200,
        border=ft.Border.all(1, ft.Colors.BLACK),
        content=ft.FilledButton("Primary color"),
    )

    primary_color = ft.TextField(label="Primary color value", width=500)
    return ft.Column(
        controls=[
            container,
            ft.Row(
                controls=[
                    primary_color,
                    ft.FilledButton(
                        "Change Primary color in Container",
                        on_click=change_primary_color,
                    ),
                ]
            ),
        ]
    )
