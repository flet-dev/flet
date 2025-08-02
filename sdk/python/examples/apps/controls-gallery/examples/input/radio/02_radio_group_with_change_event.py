import flet as ft

name = "RadioGroup with `change` event"


def example():
    def radiogroup_changed(e):
        t.value = f"Your favorite color is:  {e.control.value}"
        t.update()

    t = ft.Text()
    cg = ft.RadioGroup(
        content=ft.Column(
            [
                ft.Radio(value="red", label="Red"),
                ft.Radio(value="green", label="Green"),
                ft.Radio(value="blue", label="Blue"),
            ]
        ),
        on_change=radiogroup_changed,
    )

    return ft.Column([ft.Text("Select your favorite color:"), cg, t])
