import flet as ft


def main(page: ft.Page):
    page.title = "TextButton with 'click' event"

    def button_clicked(e):
        button.data += 1
        message.value = f"Button clicked {button.data} time(s)"
        page.update()

    page.add(
        button := ft.TextButton(
            content="Button with 'click' event",
            data=0,
            on_click=button_clicked,
        ),
        message := ft.Text(),
    )


ft.run(main)
