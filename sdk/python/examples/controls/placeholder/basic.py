import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Placeholder(
            expand=True,
            color=ft.Colors.GREEN_ACCENT,
            fallback_height=200,
            fallback_width=300,
            stroke_width=20,
        )
    )


if __name__ == "__main__":
    ft.run(main)
