import flet as ft

name = "Button with url"


def example():
    b = ft.Button("Button with Google url", url="https://google.com")
    t = ft.Text()

    return ft.Column(controls=[b, t])
