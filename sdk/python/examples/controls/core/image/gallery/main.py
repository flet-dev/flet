import flet as ft


def main(page: ft.Page):
    page.title = "Image Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50

    gallery = ft.Row(expand=True, wrap=False, scroll=ft.ScrollMode.ALWAYS)

    for i in range(0, 30):
        gallery.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.BoxFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.BorderRadius.all(10),
            )
        )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Image(
                        src="assets/app_icon_512.png",
                        width=100,
                        height=100,
                        fit=ft.BoxFit.CONTAIN,
                    ),
                    gallery,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
