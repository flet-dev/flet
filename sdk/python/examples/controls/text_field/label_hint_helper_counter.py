import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    def handle_field_change(e: ft.Event[ft.TextField]):
        message.value = e.control.value
        page.update()

    page.add(
        ft.TextField(
            on_change=handle_field_change,
            text_style=ft.TextStyle(
                size=15,
                italic=True,
                color=ft.Colors.DEEP_ORANGE_600,
                bgcolor=ft.Colors.LIME_ACCENT_200,
            ),
            label="Label",
            label_style=ft.TextStyle(
                size=17,
                weight=ft.FontWeight.BOLD,
                italic=True,
                color=ft.Colors.BLUE,
                bgcolor=ft.Colors.RED_700,
            ),
            hint_text="Hint",
            hint_style=ft.TextStyle(
                size=15,
                weight=ft.FontWeight.BOLD,
                italic=True,
                color=ft.Colors.PINK_ACCENT,
                bgcolor=ft.Colors.BROWN_400,
            ),
            helper="Helper",
            helper_style=ft.TextStyle(
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.DEEP_PURPLE,
                bgcolor=ft.Colors.BLUE_50,
            ),
            counter="Counter",
            counter_style=ft.TextStyle(
                size=14,
                italic=True,
                color=ft.Colors.YELLOW,
                bgcolor=ft.Colors.GREEN_500,
            ),
        ),
        message := ft.Text(),
    )


ft.run(main)
