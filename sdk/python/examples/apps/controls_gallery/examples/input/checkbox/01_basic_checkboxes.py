import flet as ft

name = "Basic checkboxes"


def example():
    def button_clicked(e):
        t.value = f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, "
        f"{c4.value}, {c5.value}."
        t.update()

    t = ft.Text()
    c1 = ft.Checkbox(label="Unchecked by default checkbox", value=False)
    c2 = ft.Checkbox(label="Undefined by default tristate checkbox", tristate=True)
    c3 = ft.Checkbox(label="Checked by default checkbox", value=True)
    c4 = ft.Checkbox(label="Disabled checkbox", disabled=True)
    c5 = ft.Checkbox(
        label="Checkbox with rendered label_position='left'",
        label_position=ft.LabelPosition.LEFT,
    )
    b = ft.Button(content="Submit", on_click=button_clicked)

    return ft.Column(controls=[c1, c2, c3, c4, c5, b, t])
