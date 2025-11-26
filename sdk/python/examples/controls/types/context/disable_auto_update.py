import flet as ft


def main(page: ft.Page):
    def button_click():
        ft.context.disable_auto_update()
        b.content = "Button clicked!"
        # update just the button
        b.update()

        page.controls.append(ft.Text("This won't appear"))
        # no page.update() will be called here

    page.controls.append(b := ft.Button("Action!", on_click=button_click))
    # page.update() - auto-update is enabled by default


if __name__ == "__main__":
    ft.run(main)
