import flet as ft


async def main(page: ft.Page):
    page.padding = 50

    tf = ft.TextField(
        key="styled_textfield",
        text_size=30,
        cursor_color=ft.Colors.RED,
        selection_color=ft.Colors.YELLOW,
        color=ft.Colors.PINK,
        bgcolor=ft.Colors.BLACK_26,
        filled=True,
        focused_color=ft.Colors.GREEN,
        focused_bgcolor=ft.Colors.CYAN_200,
        border={
            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                border_radius=30,
                side=ft.BorderSide(color=ft.Colors.GREEN_800),
            ),
            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                border_radius=30,
                side=ft.BorderSide(width=2, color=ft.Colors.GREEN_ACCENT_400),
            ),
        },
        max_length=20,
        capitalization=ft.TextCapitalization.CHARACTERS,
    )

    page.add(
        ft.SafeArea(
            content=tf,
        )
    )


if __name__ == "__main__":
    ft.run(main)
