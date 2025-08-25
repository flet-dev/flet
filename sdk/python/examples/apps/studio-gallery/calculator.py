import flet as ft
from flet import (
    Button,
    Colors,
    Column,
    Container,
    Row,
    Text,
    border_radius,
)


class CalculatorApp(Container):
    def build(self):
        self.reset()
        self.result = Text(value="0", color=Colors.WHITE, size=20)

        # application's root control (i.e. "view") containing all other controls
        self.content = Container(
            # width=300,
            bgcolor=Colors.BLACK,
            border_radius=border_radius.all(20),
            padding=20,
            content=Column(
                controls=[
                    Row(controls=[self.result], alignment=ft.MainAxisAlignment.END),
                    Row(
                        controls=[
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="AC",
                                bgcolor=Colors.BLUE_GREY_100,
                                color=Colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="AC",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="+/-",
                                bgcolor=Colors.BLUE_GREY_100,
                                color=Colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="+/-",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="%",
                                bgcolor=Colors.BLUE_GREY_100,
                                color=Colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="%",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="/",
                                bgcolor=Colors.ORANGE,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="/",
                            ),
                        ],
                    ),
                    Row(
                        controls=[
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="7",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="7",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="8",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="8",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="9",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="9",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="*",
                                bgcolor=Colors.ORANGE,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="*",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="4",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="4",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="5",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="5",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="6",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="6",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="-",
                                bgcolor=Colors.ORANGE,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="-",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="1",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="1",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="2",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="2",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="3",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="3",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="+",
                                bgcolor=Colors.ORANGE,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="+",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="0",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=2,
                                on_click=self.button_clicked,
                                data="0",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content=".",
                                bgcolor=Colors.WHITE24,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data=".",
                            ),
                            Button(
                                style=ft.ButtonStyle(padding=0),
                                content="=",
                                bgcolor=Colors.ORANGE,
                                color=Colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="=",
                            ),
                        ]
                    ),
                ],
            ),
        )

    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):
        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def example(page):
    calc = CalculatorApp()

    return calc


def main(page: ft.Page):
    page.title = "Flet calculator example"
    page.window_width = 390
    page.window_height = 844
    page.add(example(page))


if __name__ == "__main__":
    ft.run(main)
