import flet as ft

FIELD_INPUT_FILTER = ft.InputFilter(
    regex_string=r"^-?[0-9]*\.?[0-9]*$",  # numeric input only with optional "-" and "."
    allow=True,
    replacement_string="",
)


def format_temperature(value: float) -> str:
    """Format a temperature value for display.

    Rounds to 2 decimal places. If the rounded value is an integer, returns
    the integer without a decimal point (e.g. 5). Otherwise trims trailing
    zeros and a trailing decimal point (e.g. 5.20 -> 5.2, 5.00 -> 5).
    """
    rounded = round(value, 2)
    if rounded.is_integer():
        return str(int(rounded))
    return f"{rounded:.2f}".rstrip("0").rstrip(".")


def celsius_to_fahrenheit(value: float) -> float:
    """Convert a temperature from Celsius to Fahrenheit."""
    return value * 9 / 5 + 32


def fahrenheit_to_celsius(value: float) -> float:
    """Convert a temperature from Fahrenheit to Celsius."""
    return (value - 32) * 5 / 9


def main(page: ft.Page):
    page.title = "7GUIs - Temperature Converter"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def sync_fields(source: ft.TextField, target: ft.TextField, convert):
        value = source.value.strip()
        if not value:
            target.value = ""
            target.update()
            return

        try:
            source_value = float(value)
        except ValueError:
            return
        target_value = convert(source_value)

        target.value = format_temperature(target_value)
        page.update()

    def handle_celsius_change(e: ft.Event[ft.TextField]):
        sync_fields(celsius, fahrenheit, celsius_to_fahrenheit)

    def handle_fahrenheit_change(e: ft.Event[ft.TextField]):
        sync_fields(fahrenheit, celsius, fahrenheit_to_celsius)

    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=460,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.AMBER_50,
                content=ft.Column(
                    tight=True,
                    spacing=18,
                    controls=[
                        ft.Text(
                            "Temperature Converter",
                            size=28,
                            weight=ft.FontWeight.W_700,
                        ),
                        ft.Text(
                            "Edit either field and the other one updates immediately.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                celsius := ft.TextField(
                                    label="Celsius",
                                    suffix="°C",
                                    expand=True,
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    input_filter=FIELD_INPUT_FILTER,
                                    on_change=handle_celsius_change,
                                ),
                                ft.Text("="),
                                fahrenheit := ft.TextField(
                                    label="Fahrenheit",
                                    suffix="°F",
                                    expand=True,
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    input_filter=FIELD_INPUT_FILTER,
                                    on_change=handle_fahrenheit_change,
                                ),
                            ],
                        ),
                    ],
                ),
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
