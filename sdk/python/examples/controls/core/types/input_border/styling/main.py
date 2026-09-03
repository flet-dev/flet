import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Custom outline",
                        border=ft.OutlineInputBorder(
                            border_radius=12,
                            gap_padding=8,
                            side=ft.BorderSide(width=2, color=ft.Colors.TEAL),
                        ),
                    ),
                    ft.TextField(
                        label="Custom underline",
                        border=ft.UnderlineInputBorder(
                            border_radius=ft.BorderRadius.only(
                                top_left=12, top_right=12
                            ),
                            side=ft.BorderSide(width=3, color=ft.Colors.DEEP_ORANGE),
                        ),
                        filled=True,
                    ),
                    ft.TextField(
                        label="Per-state borders",
                        hint_text="Focus me",
                        border={
                            ft.ControlState.DEFAULT: ft.OutlineInputBorder(
                                border_radius=20,
                                side=ft.BorderSide(color=ft.Colors.BLUE_GREY_400),
                            ),
                            ft.ControlState.FOCUSED: ft.OutlineInputBorder(
                                border_radius=20,
                                side=ft.BorderSide(width=3, color=ft.Colors.INDIGO),
                            ),
                        },
                    ),
                    ft.TextField(
                        label="Error border",
                        error="This value is required",
                        border={
                            ft.ControlState.DEFAULT: ft.OutlineInputBorder(),
                            ft.ControlState.ERROR: ft.UnderlineInputBorder(
                                side=ft.BorderSide(width=3, color=ft.Colors.PINK),
                            ),
                        },
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
