import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Placeholder(
            expand=True,
            color=ft.Colors.random(),
        )
    )


if __name__ == "__main__":
    ft.run(main)
