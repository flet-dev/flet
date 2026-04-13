import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Dropdown(
                        key="styled_dropdown_1",
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
                            ft.DropdownOption("a", "Style 1A"),
                            ft.DropdownOption("b", "Style 1B"),
                            ft.DropdownOption("c", "Style 1C"),
                        ],
                    ),
                    ft.Dropdown(
                        key="styled_dropdown_2",
                        border_radius=30,
                        filled=True,
                        fill_color=ft.Colors.RED_400,
                        border_color=ft.Colors.TRANSPARENT,
                        bgcolor=ft.Colors.RED_200,
                        color=ft.Colors.CYAN_400,
                        focused_border_color=ft.Colors.PINK_300,
                        focused_border_width=20,
                        options=[
                            ft.DropdownOption("a", "Style 2A"),
                            ft.DropdownOption("b", "Style 2B"),
                            ft.DropdownOption("c", "Style 2C"),
                        ],
                    ),
                    ft.Dropdown(
                        key="styled_dropdown_3",
                        border_color=ft.Colors.PINK_ACCENT,
                        focused_border_color=ft.Colors.GREEN_ACCENT_400,
                        focused_border_width=25,
                        border_radius=30,
                        width=150,
                        border_width=5,
                        options=[
                            ft.DropdownOption("a", "Style 3A"),
                            ft.DropdownOption("b", "Style 3B"),
                            ft.DropdownOption("c", "Style 3C"),
                        ],
                    ),
                    ft.Container(
                        padding=ft.Padding.only(bottom=20),
                        content=ft.Dropdown(
                            key="styled_dropdown_4",
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
                                ft.dropdown.Option("a", "Style 4A"),
                                ft.dropdown.Option("b", "Style 4B"),
                                ft.dropdown.Option("c", "Style 4C"),
                            ],
                        ),
                    ),
                    ft.Dropdown(
                        key="styled_dropdown_5",
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
                                text="Style 5A",
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
                                text="Style 5B",
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
                                text="Style 5C",
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
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
