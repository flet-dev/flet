import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.ElevatedButton]):
        message.value = f"Textboxes values are:  '{tb1.value}', '{tb2.value}', '{tb3.value}', '{tb4.value}', '{tb5.value}'."
        page.update()

    page.add(
        tb1 := ft.TextField(label="Standard"),
        tb2 := ft.TextField(label="Disabled", disabled=True, value="First name"),
        tb3 := ft.TextField(label="Read-only", read_only=True, value="Last name"),
        tb4 := ft.TextField(
            label="With placeholder", hint_text="Please enter text here"
        ),
        tb5 := ft.TextField(label="With an icon", icon=ft.Icons.EMOJI_EMOTIONS),
        ft.ElevatedButton(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
