import flet as ft


def main(page: ft.Page):
    page.title = "Button Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    def button_clicked(e: ft.Event[ft.Button]):
        button.data += 1
        message.value = f"Button clicked {button.data} time(s)"
        page.update()

    page.add(
        button := ft.Button(
            content="Button with 'click' event",
            data=0,
            on_click=button_clicked,
        ),
        message := ft.Text(),
    )


ft.run(main)
