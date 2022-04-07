import flet
from flet import ComboBox, combobox

page = flet.page("combobox-test")
page.horizontal_align = "stretch"
page.add(
    ComboBox(
        label="Your favorite color",
        value="c",
        on_focus=lambda e: print("on_focus!"),
        on_blur=lambda e: print("on_blur!"),
        on_change=lambda e: print("on_change!"),
        options=[
            combobox.Option("RGB", item_type="header"),
            combobox.Option("red"),
            combobox.Option("green"),
            combobox.Option("blue"),
            combobox.Option("div1", item_type="divider"),
            combobox.Option("CMYK", item_type="header"),
            combobox.Option("c", "Cyan"),
            combobox.Option("m", "Magenta"),
            combobox.Option("y", "Yellow"),
            combobox.Option("k", "Black"),
        ],
    ),
    ComboBox(
        label="Your favorite car makers",
        multi_select=True,
        value=["BMW, Volkswagen"],
        width="50%",
        on_change=lambda e: print("selected cars:", e.control.value),
        options=[
            combobox.Option("Select all", item_type="select_all"),
            combobox.Option("div1", item_type="divider"),
            combobox.Option("BMW"),
            combobox.Option("Toyota"),
            combobox.Option("Volkswagen"),
            combobox.Option("Mercedes-Benz", disabled=True),
        ],
    ),
    ComboBox(
        label="Allows free form",
        multi_select=False,
        width="50%",
        allow_free_form=True,
        on_focus=lambda e: print("on_focus!"),
        on_blur=lambda e: print("on_blur!"),
        options=[
            combobox.Option("One"),
            combobox.Option("Two"),
            combobox.Option("Five"),
        ],
    ),
    ComboBox(
        label="Allows free form with multi-select and error message",
        multi_select=True,
        width="50%",
        allow_free_form=True,
        error_message="This field cannot be left blank!",
        options=[
            combobox.Option("Red"),
            combobox.Option("Green"),
            combobox.Option("Blue"),
        ],
    ),
)

input()
