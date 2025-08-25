import flet as ft


class Data:
    def __init__(self) -> None:
        self.counter = 0

    def increment(self):
        self.counter += 1

    def decrement(self):
        self.counter -= 1


data = Data()


def main(page: ft.Page):
    page.title = "SnackBar Example"

    snack_bar = ft.SnackBar(
        content=ft.Text("You did it!"),
        action="Undo it!",
        on_action=lambda e: data.decrement(),
    )

    def handle_button_click(e: ft.Event[ft.Button]):
        data.increment()
        snack_bar.content.value = f"You did it x {data.counter}"
        if not snack_bar.open:
            page.show_dialog(snack_bar)
        page.update()

    page.add(ft.Button("Open SnackBar", on_click=handle_button_click))


ft.run(main)
