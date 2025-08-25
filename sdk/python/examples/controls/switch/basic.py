import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.Button]):
        message.value = (
            f"Switch values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}."
        )
        page.update()

    page.add(
        c1 := ft.Switch(label="Unchecked switch", value=False),
        c2 := ft.Switch(label="Checked switch", value=True),
        c3 := ft.Switch(label="Disabled switch", disabled=True),
        c4 := ft.Switch(
            label="Switch with rendered label_position='left'",
            label_position=ft.LabelPosition.LEFT,
        ),
        ft.Button(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
