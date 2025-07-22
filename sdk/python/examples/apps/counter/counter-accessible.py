import flet as ft


def main(page: ft.Page):
    page.title = "Flet counter example"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 50

    def on_keyboard(e: ft.KeyboardEvent):
        print(e)
        if e.key == "S" and e.ctrl:
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    page.on_keyboard_event = on_keyboard

    txt_number = ft.TextField(
        label="Number", value="0", text_align=ft.TextAlign.RIGHT, width=100
    )
    sem = ft.Semantics(txt_number, label="Current number: 0")

    def button_click(e):
        txt_number.value = str(
            int(txt_number.value) + (1 if e.control.data == "+" else -1)
        )
        sem.label = f"Current number: {txt_number.value}"
        page.update()

    page.add(
        ft.Row(
            [
                ft.IconButton(
                    ft.Icons.REMOVE,
                    tooltip="Decrement",
                    on_click=button_click,
                    data="-",
                ),
                sem,
                ft.IconButton(
                    ft.Icons.ADD, tooltip="Increment", on_click=button_click, data="+"
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Text("Press CTRL+S to toggle semantics debugger"),
    )


ft.app(target=main)
