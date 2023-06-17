import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.NavigationBar()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["navigationbar"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_extension_set_enum():
    r = ft.NavigationBar()
    assert isinstance(r.label_behavior, ft.NavigationBarLabelBehavior)
    assert r.extension_set == ft.NavigationBarLabelBehavior.ALWAYS_SHOW
    assert r._get_attr("labelType") is None

    r = ft.NavigationBar(label_behavior=ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED)
    assert isinstance(r.label_behavior, ft.NavigationBarLabelBehavior)
    assert isinstance(r._get_attr("labelType"), str)
    assert r.label_behavior == ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED
    assert r._get_attr("labelType") == ft.NavigationBarLabelBehavior.ONLY_SHOW_SELECTED.value
    assert r._get_attr("labelType") == "onlyShowSelected"

    r = ft.NavigationBar(label_behavior="alwaysHide")
    assert isinstance(r.label_behavior, ft.NavigationBarLabelBehavior)
    assert isinstance(r._get_attr("labelType"), str)
    assert r.label_behavior == ft.NavigationBarLabelBehavior.ALWAYS_HIDE
    assert r._get_attr("labelType") == ft.NavigationBarLabelBehavior.ALWAYS_HIDE.value
    assert r._get_attr("labelType") == "alwaysHide"
