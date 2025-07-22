import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.ElevatedButton]):
        message.value = f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
        page.update()

    page.add(
        c1 := ft.Checkbox(label="Unchecked by default checkbox", value=False),
        c2 := ft.Checkbox(
            label="Undefined by default tristate checkbox", tristate=True
        ),
        c3 := ft.Checkbox(label="Checked by default checkbox", value=True),
        c4 := ft.Checkbox(label="Disabled checkbox", disabled=True),
        c5 := ft.Checkbox(
            label="Checkbox with LEFT label_position",
            label_position=ft.LabelPosition.LEFT,
        ),
        ft.ElevatedButton(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
