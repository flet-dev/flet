import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key == "S":
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    page.on_keyboard_event = on_keyboard

    def button_click(e: ft.Event[ft.Button]):
        counter.value = str(int(counter.value) + 1)
        page.update()

    page.add(
        counter := ft.Text("0", size=40),
        ft.Text("Press Shift+S to toggle semantics debugger"),
        ft.Button(
            content="Increment number",
            icon=ft.Icons.ADD,
            on_click=button_click,
        ),
    )


ft.run(main)
