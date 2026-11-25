import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent EditableComboBox"

    def change_font(e: ft.Event[fluent.EditableComboBox]):
        sample.font_family = e.control.value

    def change_size(e: ft.Event[fluent.EditableComboBox]):
        size = int(e.control.value) if e.control.value.isdigit() else 0
        if 1 <= size <= 72:
            e.control.error_text = None
            sample.size = size
        else:
            e.control.error_text = "Enter 1 to 72"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            fluent.EditableComboBox(
                                key="font",
                                width=160,
                                value="Arial",
                                items=[
                                    fluent.ComboBoxItem(value=font)
                                    for font in ["Arial", "Courier New", "Georgia"]
                                ],
                                on_change=change_font,
                            ),
                            fluent.EditableComboBox(
                                key="size",
                                width=120,
                                value="14",
                                items=[
                                    fluent.ComboBoxItem(value=str(size))
                                    for size in [10, 12, 14, 18, 24, 36]
                                ],
                                on_change=change_size,
                            ),
                        ],
                    ),
                    sample := ft.Text(
                        "The quick brown fox", font_family="Arial", size=14
                    ),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
