import flet as ft


def main(page: ft.Page):
    page.add(
        ft.CupertinoButton(
            bgcolor=ft.CupertinoColors.LIGHT_BACKGROUND_GRAY,
            opacity_on_click=0.3,
            on_click=lambda e: print("Normal CupertinoButton clicked!"),
            content=ft.Text(
                value="Normal CupertinoButton",
                color=ft.CupertinoColors.DESTRUCTIVE_RED,
            ),
        ),
        ft.CupertinoButton(
            bgcolor=ft.Colors.PRIMARY,
            alignment=ft.Alignment.TOP_LEFT,
            border_radius=ft.border_radius.all(15),
            opacity_on_click=0.5,
            on_click=lambda e: print("Filled CupertinoButton clicked!"),
            content=ft.Text("Filled CupertinoButton", color=ft.Colors.YELLOW),
        ),
        ft.CupertinoButton(
            bgcolor=ft.Colors.PRIMARY,
            disabled=True,
            alignment=ft.Alignment.TOP_LEFT,
            opacity_on_click=0.5,
            content=ft.Text("Disabled CupertinoButton"),
        ),
        ft.ElevatedButton(
            adaptive=True,  # a CupertinoButton will be rendered when running on apple-platform
            bgcolor=ft.CupertinoColors.SYSTEM_TEAL,
            content=ft.Row(
                tight=True,
                controls=[
                    ft.Icon(name=ft.Icons.FAVORITE, color="pink"),
                    ft.Text("ElevatedButton+adaptive"),
                ],
            ),
        ),
    )


ft.run(main)
