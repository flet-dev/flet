import flet as ft


def main(page: ft.Page):
    page.title = "Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    txt_number = ft.TextField(
        value="0",
        text_align=ft.TextAlign.RIGHT,
        width=100,
        label="Counter value",
    )

    def toggle_semantics_debugger(e):
        page.show_semantics_debugger = not page.show_semantics_debugger
        page.update()

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        txt_number.label = f"Counter value, {txt_number.value}"
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        txt_number.label = f"Counter value, {txt_number.value}"
        page.update()

    page.on_keyboard_event = toggle_semantics_debugger
    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Semantics(
                        label=(
                            "Press plus button to increase counter, "
                            "or minus button to decrease counter."
                        ),
                        hint_text=(
                            "Press CONTROL plus ALT plus S to show semantics debugger"
                        ),
                        button=True,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE,
                                    tooltip="Decrease number",
                                    on_click=minus_click,
                                ),
                                txt_number,
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    tooltip="Increase number",
                                    on_click=plus_click,
                                ),
                            ],
                        ),
                    ),
                    ft.Text(
                        value=(
                            "Press CONTROL plus ALT plus S to show semantics debugger"
                        ),
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
