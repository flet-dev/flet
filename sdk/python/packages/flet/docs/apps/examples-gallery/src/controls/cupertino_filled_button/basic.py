import flet as ft


def main(page: ft.Page):
    page.add(
        ft.CupertinoFilledButton(
            content=ft.Text("CupertinoFilledButton"),
            opacity_on_click=0.3,
            on_click=lambda e: print("CupertinoFilledButton clicked!"),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
