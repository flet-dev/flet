import flet as ft


async def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.SafeArea(
            content=ft.CupertinoTextField(
                label="Textfield Label",
                label_style=ft.TextStyle(italic=True, weight=ft.FontWeight.BOLD),
                bgcolor=ft.Colors.BLUE_GREY,
                image=ft.DecorationImage(src="https://picsum.photos/1000/260"),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
