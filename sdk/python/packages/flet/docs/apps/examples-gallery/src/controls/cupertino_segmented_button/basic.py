import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.CupertinoSegmentedButton(
            selected_index=1,
            selected_color=ft.Colors.RED_400,
            on_change=lambda e: print(f"selected_index: {e.data}"),
            padding=ft.Padding.symmetric(vertical=20, horizontal=50),
            controls=[
                ft.Text("One"),
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=10, horizontal=30),
                    content=ft.Text("Two"),
                ),
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=5, horizontal=10),
                    content=ft.Text("Three"),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
