import flet as ft


class Item(ft.Row):
    def __init__(self, first_name, last_name):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name

        self.first_name_field = ft.TextField(first_name)
        self.last_name_field = ft.TextField(last_name)
        self.text = ft.Text(f"{first_name} {last_name}")
        self.edit_text = ft.Row(
            [
                self.first_name_field,
                self.last_name_field,
            ],
            visible=False,
        )
        self.edit_button = ft.Button("Edit", on_click=self.edit_item)
        self.delete_button = ft.Button("Delete", on_click=self.delete_item)
        self.save_button = ft.Button("Save", on_click=self.save_item, visible=False)
        self.cancel_button = ft.Button(
            "Cancel", on_click=self.cancel_item, visible=False
        )
        self.controls = [
            self.text,
            self.edit_text,
            self.edit_button,
            self.delete_button,
            self.save_button,
            self.cancel_button,
        ]

    def delete_item(self, e):
        self.page.controls.remove(self)

    def edit_item(self, e):
        self.first_name_field.value = self.first_name
        self.last_name_field.value = self.last_name
        self.text.visible = False
        self.edit_button.visible = False
        self.delete_button.visible = False
        self.save_button.visible = True
        self.cancel_button.visible = True
        self.edit_text.visible = True

    def save_item(self, e):
        self.first_name = self.first_name_field.value
        self.last_name = self.last_name_field.value
        self.text.value = f"{self.first_name} {self.last_name}"
        self.text.visible = True
        self.edit_button.visible = True
        self.delete_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.edit_text.visible = False

    def cancel_item(self, e):
        self.text.visible = True
        self.edit_button.visible = True
        self.delete_button.visible = True
        self.save_button.visible = False
        self.cancel_button.visible = False
        self.edit_text.visible = False


def main(page: ft.Page):
    page.title = "CRUD Imperative Example"

    def add_item(e):
        item = Item(first_name.value, last_name=last_name.value)
        first_name.value = ""
        last_name.value = ""
        page.add(item)

    first_name = ft.TextField(label="First Name", width=200)
    last_name = ft.TextField(label="Last Name", width=200)

    page.add(
        ft.Row(
            [
                first_name,
                last_name,
                ft.Button("Add", on_click=add_item),
            ]
        )
    )


if __name__ == "__main__":
    ft.run(main)
