import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_switch_change(e: ft.Event[ft.Switch]):
        sheet.fullscreen = e.control.value

    sheet = ft.BottomSheet(
        fullscreen=True,
        show_drag_handle=True,
        content=ft.Container(
            padding=ft.Padding.all(10),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("This is bottom sheet's content!"),
                    ft.Button("Close bottom sheet", on_click=lambda: page.pop_dialog()),
                ],
            ),
        ),
    )

    page.add(
        ft.Button(
            content="Display bottom sheet",
            on_click=lambda e: page.show_dialog(sheet),
        ),
        ft.Switch(value=True, label="Fullscreen", on_change=handle_switch_change),
    )


if __name__ == "__main__":
    ft.run(main)
