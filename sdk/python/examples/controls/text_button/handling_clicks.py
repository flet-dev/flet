import flet as ft


def main(page: ft.Page):
    page.title = "TextButton with 'click' event"

    def button_clicked(e):
        button.data += 1
        message_text.value = f"Button clicked {button.data} time(s)"
        page.update()

    message_text = ft.Text()
    page.add(
        button := ft.TextButton(
            key="TextButton",
            content="Button with 'click' event",
            data=0,
            on_click=button_clicked,
        ),
        message := ft.Container(content=message_text, padding=ft.Padding(left=12)),
    )


if __name__ == "__main__":
    ft.run(main)
