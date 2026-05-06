import flet as ft


@ft.component
def App():
    return ft.SafeArea(content=ft.Text("Hello, world!"))


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
