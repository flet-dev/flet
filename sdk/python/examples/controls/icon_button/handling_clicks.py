import flet as ft


def main(page: ft.Page):
    page.title = "IconButton Example"

    def button_clicked(e: ft.Event[ft.IconButton]):
        button.data += 1
        message.value = f"Button clicked {button.data} time(s)"
        page.update()

    page.add(
        button := ft.IconButton(
            icon=ft.Icons.PLAY_CIRCLE_FILL_OUTLINED,
            data=0,
            on_click=button_clicked,
        ),
        message := ft.Text(),
    )


if __name__ == "__main__":
    ft.run(main)
