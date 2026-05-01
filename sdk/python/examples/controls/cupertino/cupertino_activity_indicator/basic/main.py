import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=ft.CupertinoActivityIndicator(
                animating=True,
                color=ft.Colors.RED,
                radius=50,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
