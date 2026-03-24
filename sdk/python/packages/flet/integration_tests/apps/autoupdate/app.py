import flet as ft


def main(page: ft.Page):
    page.title = "Autoupdate test"

    def auto_update_global_enabled_click(e):
        assert ft.context.page
        page.controls.append(ft.Text("Global auto update"))

    def disable_autoupdate_no_update_click(e):
        ft.context.disable_auto_update()
        page.controls.append(ft.Text("Auto update no update"))

    def disable_autoupdate_with_update_click(e):
        ft.context.disable_auto_update()
        page.controls.append(ft.Text("Auto update with update"))
        page.update()

    def skip_autoupdate_after_update_called_click(e):
        page.controls.append(ft.Text("This text should not appear"))
        skip_button.content = "Button content updated"
        skip_button.update()

    assert ft.context.page
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
        skip_button := ft.Button(
            "skip_autoupdate_after_update_called",
            on_click=skip_autoupdate_after_update_called_click,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
