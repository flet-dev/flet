import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.CupertinoFilledButton(
                opacity_on_click=0.3,
                on_click=lambda _: print("CupertinoFilledButton clicked!"),
                content=ft.Text("CupertinoFilledButton"),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
