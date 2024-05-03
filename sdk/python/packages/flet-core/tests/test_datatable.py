import flet_core as ft
from flet_core.protocol import Command


def test_datatable_instance_no_attrs_set():
    r = ft.DataTable(columns=[])
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["datatable"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_datarow_instance_no_attrs_set():
    r = ft.DataRow(cells=[])
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["r"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_datarow_color_literal_material_state_as_string():
    r = ft.DataRow(cells=[], color="yellow")
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["r"],
            attrs={"color": '"yellow"'},
            commands=[],
        )
    ], "Test failed"


def test_datarow_color_multiple_material_states_as_strings():
    r = ft.DataRow(cells=[], color={"selected": "red", "hovered": "blue", "": "yellow"})
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["r"],
            attrs={"color": '{"selected":"red","hovered":"blue","":"yellow"}'},
            commands=[],
        )
    ], "Test failed"


def test_datarow_color_multiple_material_states():
    r = ft.DataRow(
        cells=[],
        color={
            ft.MaterialState.SELECTED: "red",
            ft.MaterialState.HOVERED: "blue",
            ft.MaterialState.DEFAULT: "yellow",
        },
    )
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["r"],
            attrs={"color": '{"selected":"red","hovered":"blue","":"yellow"}'},
            commands=[],
        )
    ], "Test failed"
