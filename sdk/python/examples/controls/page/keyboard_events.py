import flet as ft


class ButtonControl(ft.Container):
    def __init__(self, text):
        super().__init__()
        self.content: ft.Text = ft.Text(text)
        self.border = ft.Border.all(1, ft.Colors.BLACK54)
        self.border_radius = 3
        self.bgcolor = "0x09000000"
        self.padding = 10
        self.visible = False


def main(page: ft.Page):
    page.spacing = 50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_keyboard(e: ft.KeyboardEvent):
        key.content.value = e.key
        key.visible = True
        shift.visible = e.shift
        ctrl.visible = e.ctrl
        alt.visible = e.alt
        meta.visible = e.meta
        page.update()

    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Text(
            "Press any key with a combination of CTRL, ALT, SHIFT and META keys..."
        ),
        ft.Row(
            controls=[
                key := ButtonControl(""),
                shift := ButtonControl("Shift"),
                ctrl := ButtonControl("Control"),
                alt := ButtonControl("Alt"),
                meta := ButtonControl("Meta"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )


ft.run(main)
