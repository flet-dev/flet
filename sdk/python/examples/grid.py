import flet
from flet import (
    Button,
    Checkbox,
    Column,
    Dropdown,
    Grid,
    Stack,
    Text,
    Textbox,
    Toolbar,
    dropdown,
    toolbar,
)


class Person:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        age: int = None,
        employee: bool = False,
        color: str = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.employee = employee
        self.color = color


def main(page):
    page.title = "Grid example"
    page.update()

    # Basic grid
    page.add(
        Text("Basic grid", size="large"),
        Stack(
            width="50%",
            controls=[
                Grid(
                    columns=[
                        Column(name="First name", field_name="first_name"),
                        Column(name="Last name", field_name="last_name"),
                        Column(name="Age", field_name="age"),
                    ],
                    items=[
                        Person(first_name="John", last_name="Smith", age=30),
                        Person(first_name="Samantha", last_name="Fox", age=43),
                        Person(first_name="Alice", last_name="Brown", age=25),
                    ],
                )
            ],
        ),
    )

    # Sortable grid
    page.add(
        Text("Sortable grid with resizable columns and selectable rows", size="large"),
        Grid(
            selection_mode="single",
            preserve_selection=True,
            columns=[
                Column(
                    resizable=True,
                    sortable="string",
                    name="First name",
                    field_name="first_name",
                ),
                Column(
                    resizable=True,
                    sortable="string",
                    sorted="asc",
                    name="Last name",
                    field_name="last_name",
                ),
                Column(resizable=True, sortable="number", name="Age", field_name="age"),
            ],
            items=[
                Person(first_name="John", last_name="Smith", age=30),
                Person(first_name="Samantha", last_name="Fox", age=43),
                Person(first_name="Alice", last_name="Brown", age=25),
            ],
        ),
    )

    # Compact grid
    page.add(
        Text("Compact grid with no header and multiple selection", size="large"),
        Grid(
            compact=True,
            header_visible=False,
            selection_mode="multiple",
            preserve_selection=True,
            columns=[
                Column(max_width=100, field_name="first_name"),
                Column(max_width=100, field_name="last_name"),
                Column(max_width=100, field_name="age"),
            ],
            items=[
                Person(first_name="John", last_name="Smith", age=30),
                Person(first_name="Samantha", last_name="Fox", age=43),
                Person(first_name="Alice", last_name="Brown", age=25),
            ],
        ),
    )

    # Dynamic grid
    grid = None

    def delete_records(e):
        for r in grid.selected_items:
            grid.items.remove(r)
        page.update()

    delete_records = toolbar.Item(
        text="Delete records", icon="Delete", disabled=True, on_click=delete_records
    )
    grid_toolbar = Toolbar(items=[delete_records])

    def grid_items_selected(e):
        delete_records.disabled = len(e.control.selected_items) == 0
        delete_records.update()

    grid = Grid(
        selection_mode="multiple",
        compact=True,
        header_visible=True,
        columns=[
            Column(
                name="First name", template_controls=[Textbox(value="{first_name}")]
            ),
            Column(name="Last name", template_controls=[Textbox(value="{last_name}")]),
            Column(name="Age", template_controls=[Text(value="{age}")]),
            Column(
                name="Favorite color",
                template_controls=[
                    Dropdown(
                        value="{color}",
                        options=[
                            dropdown.Option("red", "Red"),
                            dropdown.Option("green", "Green"),
                            dropdown.Option("blue", "Blue"),
                        ],
                    )
                ],
            ),
            Column(
                name="Is employee", template_controls=[Checkbox(value_field="employee")]
            ),
        ],
        items=[
            Person(
                first_name="John",
                last_name="Smith",
                age=30,
                employee=False,
                color="blue",
            ),
            Person(
                first_name="Jack",
                last_name="Brown",
                age=43,
                employee=True,
                color="green",
            ),
            Person(first_name="Alice", last_name="Fox", age=25, employee=False),
        ],
        margin=0,
        on_select=grid_items_selected,
    )

    first_name = Textbox("First name")
    last_name = Textbox("Last name")
    age = Textbox("Age")

    def add_record(e):
        grid.items.append(
            Person(
                first_name=first_name.value,
                last_name=last_name.value,
                age=age.value,
                employee=True,
            )
        )
        first_name.value = ""
        last_name.value = ""
        age.value = ""
        page.update()

    page.add(
        Text("Dynamic grid with template columns", size="large"),
        grid_toolbar,
        grid,
        Text("Add new employee record", size="medium"),
        Stack(horizontal=True, controls=[first_name, last_name, age]),
        Button("Add record", on_click=add_record),
    )


flet.app("python-grid", target=main, web=False)
