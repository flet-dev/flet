import flet as ft


def main(page: ft.Page):
    page.title = "GridView Example"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 50

    page.add(
        ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
            controls=[
                ft.Image(
                    src=f"https://picsum.photos/150/150?{i}",
                    fit=ft.BoxFit.NONE,
                    repeat=ft.ImageRepeat.NO_REPEAT,
                    border_radius=ft.BorderRadius.all(10),
                )
                for i in range(0, 60)
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
