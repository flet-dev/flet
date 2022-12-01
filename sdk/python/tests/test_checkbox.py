import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Checkbox()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["checkbox"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_label_position_enum():
    r = ft.Checkbox(label_position=ft.LabelPosition.LEFT)
    assert isinstance(r.label_position, ft.LabelPosition)
    assert isinstance(r._get_attr("labelPosition"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["labelposition"] == "left"


def test_label_position_str():
    r = ft.Checkbox(label_position="left")
    assert isinstance(r.label_position, str)
    assert isinstance(r._get_attr("labelPosition"), str)
    cmd = r._build_add_commands()
    assert cmd[0].attrs["labelposition"] == "left"


def test_label_position_wrong_str_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Checkbox(label_position="center1")


def test_label_position_wrong_type_raises_beartype():
    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Checkbox(label_position=1)
