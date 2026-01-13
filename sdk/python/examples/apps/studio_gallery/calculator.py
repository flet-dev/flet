import flet as ft


@ft.component
def App():
    display, set_display = ft.use_state("0")
    operand1, set_operand1 = ft.use_state(0.0)
    operator, set_operator = ft.use_state("+")
    new_operand, set_new_operand = ft.use_state(True)

    def format_number(num: float):
        if num % 1 == 0:
            return int(num)
        return num

    def calculate(op1: float, op2: float, op: str):
        try:
            if op == "+":
                return format_number(op1 + op2)
            if op == "-":
                return format_number(op1 - op2)
            if op == "*":
                return format_number(op1 * op2)
            if op == "/":
                if op2 == 0:
                    return "Error"
                return format_number(op1 / op2)
        except Exception:
            return "Error"

    def parse_float(v, fallback=0.0):
        try:
            return float(v)
        except Exception:
            try:
                return float(fallback)
            except Exception:
                return 0.0

    def on_button(data: str):
        nonlocal display, operand1, operator, new_operand
        # update via setters so UI re-renders
        if display == "Error" or data == "AC":
            set_display("0")
            set_operand1(0.0)
            set_operator("+")
            set_new_operand(True)
            return

        if data in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."):
            if display == "0" or new_operand:
                set_display(data)
                set_new_operand(False)
            else:
                set_display(str(display) + data)
            return

        if data in ("+", "-", "*", "/"):
            val = calculate(operand1, parse_float(display), operator)
            # set result and operator
            set_display(str(val))
            set_operator(data)
            if val == "Error":
                set_operand1(0.0)
            else:
                set_operand1(parse_float(val))
            set_new_operand(True)
            return

        if data == "=":
            val = calculate(operand1, parse_float(display), operator)
            set_display(str(val))
            # reset for next input
            set_operand1(0.0)
            set_operator("+")
            set_new_operand(True)
            return

        if data == "%":
            set_display(str(parse_float(display) / 100))
            set_operand1(0.0)
            set_operator("+")
            set_new_operand(True)
            return

        if data == "+/-":
            v = parse_float(display)
            if v > 0:
                set_display("-" + str(display))
            elif v < 0:
                set_display(str(format_number(abs(v))))
            return

    def make_btn(label: str, bgcolor=None, color=None, expand: int = 1):
        return ft.Button(
            label,
            expand=expand,
            bgcolor=bgcolor,
            color=color,
            on_click=lambda e, d=label: on_button(d),
        )

    # build rows like the original layout
    return ft.Container(
        width=350,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.BorderRadius.all(20),
        padding=20,
        content=ft.Column(
            controls=[
                ft.Row(
                    [ft.Text(value=str(display), color=ft.Colors.WHITE, size=20)],
                    alignment=ft.MainAxisAlignment.END,
                ),
                ft.Row(
                    controls=[
                        make_btn(
                            "AC", bgcolor=ft.Colors.BLUE_GREY_100, color=ft.Colors.BLACK
                        ),
                        make_btn(
                            "+/-",
                            bgcolor=ft.Colors.BLUE_GREY_100,
                            color=ft.Colors.BLACK,
                        ),
                        make_btn(
                            "%", bgcolor=ft.Colors.BLUE_GREY_100, color=ft.Colors.BLACK
                        ),
                        make_btn("/", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]
                ),
                ft.Row(
                    controls=[
                        make_btn(
                            "7", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "8", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "9", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn("*", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]
                ),
                ft.Row(
                    controls=[
                        make_btn(
                            "4", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "5", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "6", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn("-", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]
                ),
                ft.Row(
                    controls=[
                        make_btn(
                            "1", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "2", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn(
                            "3", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn("+", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]
                ),
                ft.Row(
                    controls=[
                        make_btn(
                            "0",
                            bgcolor=ft.Colors.WHITE_24,
                            color=ft.Colors.WHITE,
                            expand=2,
                        ),
                        make_btn(
                            ".", bgcolor=ft.Colors.WHITE_24, color=ft.Colors.WHITE
                        ),
                        make_btn("=", bgcolor=ft.Colors.ORANGE, color=ft.Colors.WHITE),
                    ]
                ),
            ]
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
