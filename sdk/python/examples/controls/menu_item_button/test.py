import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    mib1 = ft.MenuItemButton(
        content=ft.Text("Yes"),
        on_click=lambda e: print("yes"),
    )
    mib2 = ft.MenuItemButton(
        content=ft.Text("No"),
        on_click=lambda e: print("no"),
    )
    mib3 = ft.MenuItemButton(
        content=ft.Text("Maybe"),
        on_click=lambda e: print("maybe"),
    )

    page.add(ft.Row(controls=[mib1, mib2, mib3]))


ft.run(main)
