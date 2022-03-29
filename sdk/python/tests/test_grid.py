import flet
import pytest
from beartype.roar import BeartypeCallHintPepParamException
from flet import Grid, Column
from flet.protocol import Command


class Contact:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


expected_result = [
    Command(
        indent=0,
        name=None,
        values=["grid"],
        attrs={"compact": "true", "headervisible": "true", "selection": "multiple", "shimmerlines": "1"},
        lines=[],
        commands=[],
    ),
    Command(indent=2, name=None, values=["columns"], attrs={}, lines=[], commands=[]),
    Command(
        indent=4,
        name=None,
        values=["column"],
        attrs={
            "fieldname": "first_name",
            "icon": "mail",
            "icononly": "true",
            "maxwidth": "200",
            "minwidth": "100",
            "name": "First name",
            "resizable": "false",
            "sortable": "string",
            "sorted": "false",
            "sortfield": "sort field name",
        },
        lines=[],
        commands=[],
    ),
    Command(
        indent=4,
        name=None,
        values=["column"],
        attrs={"fieldname": "last_name", "name": "Last name"},
        lines=[],
        commands=[],
    ),
    Command(indent=2, name=None, values=["items"], attrs={}, lines=[], commands=[]),
    Command(
        indent=4,
        name=None,
        values=["item"],
        attrs={"first_name": "Inesa", "last_name": "Fitsner"},
        lines=[],
        commands=[],
    ),
    Command(
        indent=4,
        name=None,
        values=["item"],
        attrs={"first_name": "Fiodar", "last_name": "Fitsner"},
        lines=[],
        commands=[],
    ),
]


def test_grid_add__with_class():
    g = Grid(
        selection_mode="multiple",
        compact=True,
        header_visible=True,
        shimmer_lines=1,
        columns=[
            Column(
                field_name="first_name",
                name="First name",
                icon="mail",
                icon_only=True,
                sortable="string",
                sort_field="sort field name",
                sorted=False,
                resizable=False,
                min_width=100,
                max_width=200,
            ),
            Column(field_name="last_name", name="Last name"),
        ],
        items=[
            Contact(first_name="Inesa", last_name="Fitsner"),
            Contact(first_name="Fiodar", last_name="Fitsner"),
        ],
    )

    assert isinstance(g, flet.Control)
    assert isinstance(g, flet.Grid)
    assert g.get_cmd_str() == expected_result, "Test failed"


def test_grid_add__with_dict():
    g = Grid(
        selection_mode="multiple",
        compact=True,
        header_visible=True,
        shimmer_lines=1,
        columns=[
            Column(
                field_name="first_name",
                name="First name",
                icon="mail",
                icon_only=True,
                sortable="string",
                sort_field="sort field name",
                sorted=False,
                resizable=False,
                min_width=100,
                max_width=200,
            ),
            Column(field_name="last_name", name="Last name"),
        ],
        items=[
            {"first_name": "Inesa", "last_name": "Fitsner"},
            {"first_name": "Fiodar", "last_name": "Fitsner"},
        ],
    )

    assert isinstance(g, flet.Control)
    assert isinstance(g, flet.Grid)
    assert g.get_cmd_str() == expected_result, "Test failed"


def test_property_value_check():
    with pytest.raises(BeartypeCallHintPepParamException):
        Column(icon_only="foo")
