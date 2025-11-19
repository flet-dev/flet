import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.Colors.WHITE, size=20)

    class CalcButton(ft.Button):
        def __init__(self, content, expand=1):
            super().__init__()
            self.content = content
            self.expand = expand

    class DigitButton(CalcButton):
        def __init__(self, content, expand=1):
            CalcButton.__init__(self, content, expand)
            self.bgcolor = ft.Colors.WHITE_24
            self.color = ft.Colors.WHITE

    class ActionButton(CalcButton):
        def __init__(self, content):
            CalcButton.__init__(self, content)
            self.bgcolor = ft.Colors.ORANGE
            self.color = ft.Colors.WHITE

    class ExtraActionButton(CalcButton):
        def __init__(self, content):
            CalcButton.__init__(self, content)
            self.bgcolor = ft.Colors.BLUE_GREY_100
            self.color = ft.Colors.BLACK

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
                            ExtraActionButton("AC"),
                            ExtraActionButton("+/-"),
                            ExtraActionButton("%"),
                            ActionButton("/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("7"),
                            DigitButton("8"),
                            DigitButton("9"),
                            ActionButton("*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("4"),
                            DigitButton("5"),
                            DigitButton("6"),
                            ActionButton("-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("1"),
                            DigitButton("2"),
                            DigitButton("3"),
                            ActionButton("+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton("0", expand=2),
                            DigitButton("."),
                            ActionButton("="),
                        ]
                    ),
                ]
            ),
        )
    )


ft.run(main)
