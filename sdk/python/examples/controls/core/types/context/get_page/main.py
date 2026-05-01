import flet as ft


def main(page: ft.Page):
    def button_click(e):
        print("Page width:", ft.context.page.width)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[ft.Button("Get page width", on_click=button_click)]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
