import flet as ft

name = "Basic switches"


def example():
    def button_clicked(e):
        t.value = f"Switch values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}."
        t.update()

    t = ft.Text()
    c1 = ft.Switch(label="Unchecked switch", value=False)
    c2 = ft.Switch(label="Checked switch", value=True)
    c3 = ft.Switch(label="Disabled switch", disabled=True)
    c4 = ft.Switch(
        label="Switch with rendered label_position='left'",
        label_position=ft.LabelPosition.LEFT,
    )
    b = ft.Button(content="Submit", on_click=button_clicked)

    return ft.Column(controls=[c1, c2, c3, c4, b, t])
