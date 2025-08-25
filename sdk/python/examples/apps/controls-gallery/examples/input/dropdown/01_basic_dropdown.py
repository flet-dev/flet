import flet as ft

name = "Basic dropdown"


def example():
    def button_clicked(e):
        t.value = f"Dropdown value is:  {dd.value}"
        t.update()

    t = ft.Text()
    b = ft.Button(content="Submit", on_click=button_clicked)
    dd = ft.Dropdown(
        width=100,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
    )

    return ft.Column(controls=[dd, b, t])
