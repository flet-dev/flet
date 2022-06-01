import flet
from flet import (
    Column,
    Container,
    Dropdown,
    ElevatedButton,
    OutlinedButton,
    Page,
    Row,
    TextField,
    dropdown,
)


def main(page: Page):
    def find_option(option_name):
        for option in d.options:
            if option_name == option.key:
                return option
        return None

    def add_clicked(e):
        d.options.append(dropdown.Option(option_textbox.value))
        d.value = option_textbox.value
        option_textbox.value = ""
        page.update()

    def delete_clicked(e):
        option = find_option(d.value)
        if option != None:
            d.options.remove(option)
            # d.value = None
            page.update()

    d = Dropdown()
    option_textbox = TextField(hint_text="Enter item name")
    add = ElevatedButton("Add", on_click=add_clicked)
    delete = OutlinedButton("Delete selected", on_click=delete_clicked)
    page.add(d, Row(controls=[option_textbox, add, delete]))


flet.app(port=8550, target=main, view=flet.WEB_BROWSER)
