::: flet.DropdownM2

## Examples

[Live example](https://flet-controls-gallery.fly.dev/input/dropdown)

### Basic dropdown



```python
import flet as ft

def main(page: ft.Page):
    def button_clicked(e):
        t.value = f"Dropdown value is:  {dd.value}"
        page.update()

    t = ft.Text()
    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    dd = ft.DropdownM2(
        width=100,
        options=[
            ft.dropdownm2.Option("Red"),
            ft.dropdownm2.Option("Green"),
            ft.dropdownm2.Option("Blue"),
        ],
    )
    page.add(dd, b, t)

ft.run(main)
```


<img src="/img/docs/controls/dropdown/basic-dropdown.gif" className="screenshot-30"/>

### Dropdown with label and hint



```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.DropdownM2(
            label="Color",
            hint_text="Choose your favourite color?",
            options=[
                ft.dropdownm2.Option("Red"),
                ft.dropdownm2.Option("Green"),
                ft.dropdownm2.Option("Blue"),
            ],
            autofocus=True,
        )
    )

ft.run(main)
```


<img src="/img/docs/controls/dropdown/dropdown-with-custom-content.gif" className="screenshot-30"/>

### Dropdown with `on_change` event



```python
import flet as ft

def main(page: ft.Page):
    def dropdown_changed(e):
        t.value = f"Dropdown changed to {dd.value}"
        page.update()

    t = ft.Text()
    dd = ft.DropdownM2(
        on_change=dropdown_changed,
        options=[
            ft.dropdownm2.Option("Red"),
            ft.dropdownm2.Option("Green"),
            ft.dropdownm2.Option("Blue"),
        ],
        width=200,
    )
    page.add(dd, t)

ft.run(main)
```


<img src="/img/docs/controls/dropdown/dropdown-with-change-event.gif" className="screenshot-30" />

### Change items in dropdown options



```python
import flet as ft

def main(page: ft.Page):
    def find_option(option_name):
        for option in d.options:
            if option_name == option.key:
                return option
        return None

    def add_clicked(e):
        d.options.append(ft.dropdown.Option(option_textbox.value))
        d.value = option_textbox.value
        option_textbox.value = ""
        page.update()

    def delete_clicked(e):
        option = find_option(d.value)
        if option != None:
            d.options.remove(option)
            # d.value = None
            page.update()

    d = ft.DropdownM2()
    option_textbox = ft.TextField(hint_text="Enter item name")
    add = ft.ElevatedButton("Add", on_click=add_clicked)
    delete = ft.OutlinedButton("Delete selected", on_click=delete_clicked)
    page.add(d, ft.Row(controls=[option_textbox, add, delete]))

ft.run(main)
```


<img src="/img/docs/controls/dropdown/dropdown-with-add-and-delete.gif" className="screenshot-40"/>
