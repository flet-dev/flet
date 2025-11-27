import flet as ft


def main(page: ft.Page):
    page.add(
        # 1
        ft.Dropdown(
            text_size=20,
            content_padding=10,
            color=ft.Colors.PURPLE_200,
            bgcolor=ft.Colors.BLUE_200,
            filled=True,
            border_radius=30,
            border_color=ft.Colors.GREEN_800,
            focused_border_color=ft.Colors.GREEN_ACCENT_400,
            focused_border_width=5,
            options=[
                ft.DropdownOption("a", "Item A"),
                ft.DropdownOption("b", "Item B"),
                ft.DropdownOption("c", "Item C"),
            ],
        ),
        # 2
        ft.Dropdown(
            border_radius=30,
            filled=True,
            fill_color=ft.Colors.RED_400,
            border_color=ft.Colors.TRANSPARENT,
            bgcolor=ft.Colors.RED_200,
            color=ft.Colors.CYAN_400,
            focused_border_color=ft.Colors.PINK_300,
            focused_border_width=20,
            options=[
                ft.DropdownOption("a", "Item A"),
                ft.DropdownOption("b", "Item B"),
                ft.DropdownOption("c", "Item C"),
            ],
        ),
        # 3
        ft.Dropdown(
            border_color=ft.Colors.PINK_ACCENT,
            focused_border_color=ft.Colors.GREEN_ACCENT_400,
            focused_border_width=25,
            border_radius=30,
            width=150,
            border_width=5,
            options=[
                ft.DropdownOption("a", "Item A"),
                ft.DropdownOption("b", "Item B"),
                ft.DropdownOption("c", "Item C"),
            ],
        ),
        # 4
        ft.Container(
            padding=ft.Padding.only(bottom=20),
            content=ft.Dropdown(
                text_size=30,
                color=ft.Colors.ORANGE_ACCENT,
                border_radius=20,
                filled=True,
                border_width=0,
                autofocus=True,
                focused_border_color=ft.Colors.GREEN_100,
                focused_border_width=10,
                width=200,
                height=50,
                options=[
                    ft.dropdown.Option("a", "Item A"),
                    ft.dropdown.Option("b", "Item B"),
                    ft.dropdown.Option("c", "Item C"),
                ],
            ),
        ),
        # 5
        ft.Dropdown(
            text_size=30,
            border_radius=20,
            filled=True,
            border_width=0,
            focused_border_color=ft.Colors.GREEN_100,
            focused_border_width=10,
            content_padding=20,
            width=200,
            options=[
                ft.DropdownOption(
                    key="a",
                    text="Item A",
                    style=ft.ButtonStyle(
                        shape=ft.BeveledRectangleBorder(radius=15),
                        color={
                            ft.ControlState.HOVERED: ft.Colors.WHITE,
                            ft.ControlState.FOCUSED: ft.Colors.BLUE,
                            ft.ControlState.DEFAULT: ft.Colors.BLACK,
                        },
                    ),
                ),
                ft.DropdownOption(
                    key="b",
                    text="Item B",
                    style=ft.ButtonStyle(
                        shape=ft.BeveledRectangleBorder(radius=15),
                        color={
                            ft.ControlState.HOVERED: ft.Colors.WHITE,
                            ft.ControlState.FOCUSED: ft.Colors.BLUE,
                            ft.ControlState.DEFAULT: ft.Colors.BLACK,
                        },
                    ),
                ),
                ft.DropdownOption(
                    key="c",
                    text="Item C",
                    style=ft.ButtonStyle(
                        shape=ft.BeveledRectangleBorder(radius=15),
                        color={
                            ft.ControlState.HOVERED: ft.Colors.WHITE,
                            ft.ControlState.FOCUSED: ft.Colors.BLUE,
                            ft.ControlState.DEFAULT: ft.Colors.BLACK,
                        },
                    ),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
