import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.AlertDialog()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["alertdialog"],
            attrs={"modal": "false", "open": "false"},
            commands=[],
        )
    ], "Test failed"


def test_alignment_enum():
    r = ft.AlertDialog(actions_alignment=ft.MainAxisAlignment.SPACE_AROUND)
    assert isinstance(r.actions_alignment, ft.MainAxisAlignment)
    assert isinstance(r._get_attr("actionsAlignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["actionsalignment"] == "spaceAround"


def test_alignment_str():
    r = ft.AlertDialog(actions_alignment="center")
    assert isinstance(r.actions_alignment, str)
    assert isinstance(r._get_attr("actionsalignment"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["actionsalignment"] == "center"
