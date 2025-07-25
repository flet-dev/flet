import flet as ft

name = "Password with reveal button"


def example():
    return ft.TextField(
        label="Password with reveal button", password=True, can_reveal_password=True
    )
