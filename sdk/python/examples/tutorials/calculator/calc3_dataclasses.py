from dataclasses import dataclass

import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)

    @dataclass
    class CalcButton(ft.Button):
        def init(self):
            if self.expand is None:
                self.expand = 1

    @dataclass
    class DigitButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.WHITE_24
        color: ft.Colors = ft.Colors.WHITE

    @dataclass
    class ActionButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.ORANGE
        color: ft.Colors = ft.Colors.WHITE

    @dataclass
    class ExtraActionButton(CalcButton):
        bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
        color: ft.Colors = ft.Colors.BLACK

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.Colors.BLACK,
            border_radius=ft.BorderRadius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment=ft.MainAxisAlignment.END),
                    ft.Row(
                        controls=[
                            ExtraActionButton(content="AC"),
                            ExtraActionButton(content="+/-"),
                            ExtraActionButton(content="%"),
                            ActionButton(content="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="7"),
                            DigitButton(content="8"),
                            DigitButton(content="9"),
                            ActionButton(content="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="4"),
                            DigitButton(content="5"),
                            DigitButton(content="6"),
                            ActionButton(content="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="1"),
                            DigitButton(content="2"),
                            DigitButton(content="3"),
                            ActionButton(content="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(content="0", expand=2),
                            DigitButton(content="."),
                            ActionButton(content="="),
                        ],
                    ),
                ]
            ),
        )
    )


ft.run(main)
