import flet as ft


def test_semantics_identifier_defaults_to_none():
    semantics = ft.Semantics(content=ft.Text("Save"))
    assert semantics.identifier is None


def test_semantics_identifier_is_settable():
    semantics = ft.Semantics(
        identifier="save_btn",
        label="Submit",
        content=ft.Text("Save"),
    )
    assert semantics.identifier == "save_btn"
    assert semantics.label == "Submit"
