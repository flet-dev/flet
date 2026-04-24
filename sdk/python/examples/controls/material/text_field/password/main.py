import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.TextField(
                key="password_textfield",
                label="Password with reveal button",
                password=True,
                can_reveal_password=True,
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
