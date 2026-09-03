import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.DropdownM2(
                        label="Matching field and menu",
                        value="a",
                        border=ft.OutlineInputBorder(
                            border_radius=20,
                            side=ft.BorderSide(width=2, color=ft.Colors.TEAL),
                        ),
                        menu_border_radius=20,
                        options=[
                            ft.dropdownm2.Option("a", "Alice"),
                            ft.dropdownm2.Option("b", "Bob"),
                            ft.dropdownm2.Option("c", "Carol"),
                        ],
                    ),
                    ft.DropdownM2(
                        label="Underlined field, rounded menu",
                        value="a",
                        border=ft.UnderlineInputBorder(),
                        menu_border_radius=ft.BorderRadius.only(
                            bottom_left=16, bottom_right=16
                        ),
                        options=[
                            ft.dropdownm2.Option("a", "Alice"),
                            ft.dropdownm2.Option("b", "Bob"),
                            ft.dropdownm2.Option("c", "Carol"),
                        ],
                    ),
                ],
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
