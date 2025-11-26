import flet as ft

name = "CupertinoRadio example"


def example():
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        t.update()

    t = ft.Text()
    b = ft.Button(content="Submit", on_click=button_clicked)
    cg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.CupertinoRadio(
                    value="red",
                    label="Red - Cupertino Radio",
                    active_color=ft.Colors.RED,
                    inactive_color=ft.Colors.RED,
                ),
                ft.Radio(
                    value="green",
                    label="Green - Material Radio",
                    fill_color=ft.Colors.GREEN,
                ),
                ft.Radio(
                    value="blue",
                    label="Blue - Adaptive Radio",
                    adaptive=True,
                    active_color=ft.Colors.BLUE,
                    tooltip=ft.Tooltip(
                        message="Adaptive Radio shows as CupertinoRadio on macOS and "
                        "iOS and as Radio on other platforms"
                    ),
                ),
            ]
        )
    )

    return ft.Column([ft.Text("Select your favorite color:"), cg, b, t])
