import flet as ft

name = "ElevatedButton with url"


def example():
    b = ft.ElevatedButton("Button with Google url", url="https://google.com")
    t = ft.Text()

    return ft.Column(controls=[b, t])
