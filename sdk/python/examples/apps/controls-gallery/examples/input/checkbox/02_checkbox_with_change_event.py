import flet as ft

name = "Checkbox with `change` event"


def example():
    def checkbox_changed(e):
        t.value = f"Checkbox value changed to {c.value}"
        t.update()

    c = ft.Checkbox(label="Checkbox with 'change' event", on_change=checkbox_changed)
    t = ft.Text()

    return ft.Column(controls=[c, t])
