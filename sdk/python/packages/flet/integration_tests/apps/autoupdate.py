import flet as ft


def main(page: ft.Page):
    page.title = "Autoupdate test"

    def auto_update_global_enabled_click(e):
        page.controls.append(ft.Text("Global auto update"))

    def disable_autoupdate_no_update_click(e):
        ft.context.disable_auto_update()
        page.controls.append(ft.Text("Auto update no update"))

    def disable_autoupdate_with_update_click(e):
        ft.context.disable_auto_update()
        page.controls.append(ft.Text("Auto update with update"))
        page.update()

    page.add(
        ft.Text(f"Auto update enabled: {ft.context.auto_update_enabled()}"),
        ft.Button(
            "auto_update_global_enabled", on_click=auto_update_global_enabled_click
        ),
        ft.Button(
            "disable_autoupdate_no_update",
            on_click=disable_autoupdate_no_update_click,
        ),
        ft.Button(
            "disable_autoupdate_with_update",
            on_click=disable_autoupdate_with_update_click,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
