from flet.core.protocol import Command

import flet as ft


def test_datatable_instance_no_attrs_set():
    r = ft.DataTable(columns=[ft.DataColumn(label=ft.Text("Header"))])
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(indent=0, name=None, values=["datatable"], attrs={}, commands=[]),
        Command(indent=2, name=None, values=["datacolumn"], attrs={}, commands=[]),
        Command(
            indent=4,
            name=None,
            values=["text"],
            attrs={"n": "label", "value": "Header"},
            commands=[],
        ),
    ], "Test failed"


def test_datarow_instance_no_attrs_set():
    r = ft.DataRow(cells=[ft.DataCell(content=ft.Text("Cell"))])
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(indent=0, name=None, values=["datarow"], attrs={}, commands=[]),
        Command(indent=2, name=None, values=["datacell"], attrs={}, commands=[]),
        Command(
            indent=4, name=None, values=["text"], attrs={"value": "Cell"}, commands=[]
        ),
    ], "Test failed"


def test_datarow_color_literal_material_state_as_string():
    r = ft.DataRow(cells=[ft.DataCell(content=ft.Text("Cell"))], color="yellow")
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["datarow"],
            attrs={"color": '{"default":"yellow"}'},
            commands=[],
        ),
        Command(indent=2, name=None, values=["datacell"], attrs={}, commands=[]),
        Command(
            indent=4, name=None, values=["text"], attrs={"value": "Cell"}, commands=[]
        ),
    ], "Test failed"


def test_datarow_color_multiple_material_states_as_strings():
    r = ft.DataRow(
        cells=[ft.DataCell(content=ft.Text("Cell"))],
        color={
            ft.ControlState.SELECTED: "red",
            ft.ControlState.HOVERED: "blue",
            ft.ControlState.DEFAULT: "yellow",
        },
    )
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["datarow"],
            attrs={"color": '{"selected":"red","hovered":"blue","default":"yellow"}'},
            commands=[],
        ),
        Command(indent=2, name=None, values=["datacell"], attrs={}, commands=[]),
        Command(
            indent=4, name=None, values=["text"], attrs={"value": "Cell"}, commands=[]
        ),
    ], "Test failed"


def test_datarow_color_multiple_material_states():
    r = ft.DataRow(
        cells=[ft.DataCell(content=ft.Text("Cell"))],
        color={
            ft.ControlState.SELECTED: "red",
            ft.ControlState.HOVERED: "blue",
            ft.ControlState.DEFAULT: "yellow",
        },
    )
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["datarow"],
            attrs={"color": '{"selected":"red","hovered":"blue","default":"yellow"}'},
            commands=[],
        ),
        Command(indent=2, name=None, values=["datacell"], attrs={}, commands=[]),
        Command(
            indent=4, name=None, values=["text"], attrs={"value": "Cell"}, commands=[]
        ),
    ], "Test failed"
