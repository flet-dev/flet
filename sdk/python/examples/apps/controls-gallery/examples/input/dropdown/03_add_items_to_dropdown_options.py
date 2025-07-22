import flet as ft

name = "Add items to dropdown options"


def example():
    def add_clicked(e):
        d.options.append(ft.dropdown.Option(option_textbox.value))
        d.value = option_textbox.value
        option_textbox.value = ""
        option_textbox.update()
        d.update()

    d = ft.Dropdown()
    option_textbox = ft.TextField(hint_text="Enter item name")
    add = ft.ElevatedButton("Add", on_click=add_clicked)

    return ft.Column(controls=[d, ft.Row(controls=[option_textbox, add])])
