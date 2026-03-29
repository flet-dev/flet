import flet as ft


@ft.component
def App():
    return ft.SafeArea(content=ft.Text("Hello, world!"))


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
