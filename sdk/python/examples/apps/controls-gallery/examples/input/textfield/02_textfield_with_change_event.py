import flet as ft

name = "TextField with `change` event"


def example():
    def textbox_changed(e):
        t.value = e.control.value
        t.update()

    t = ft.Text()
    tb = ft.TextField(
        label="TextField with 'change' event:",
        on_change=textbox_changed,
    )

    return ft.Column(controls=[tb, t])
