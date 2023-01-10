import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.NavigationRail()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["navigationrail"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_extension_set_enum():
    r = ft.NavigationRail()
    assert r.label_type is None
    assert r._get_attr("labelType") is None

    r = ft.NavigationRail(label_type=ft.NavigationRailLabelType.SELECTED)
    assert isinstance(r.label_type, ft.NavigationRailLabelType)
    assert r.label_type == ft.NavigationRailLabelType.SELECTED
    assert r._get_attr("labelType") == "selected"

    r = ft.NavigationRail(label_type="none")
    assert isinstance(r.label_type, str)
    assert r._get_attr("labelType") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.NavigationRail(label_type="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.NavigationRail(label_type=1)
