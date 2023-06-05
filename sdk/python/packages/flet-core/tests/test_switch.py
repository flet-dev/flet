import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Switch()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=['switch'],
            attrs={},
            commands=[],
        )
    ], 'Test failed'


def test_label_position_enum():
    r = ft.Switch(label_position=ft.LabelPosition.LEFT)
    assert isinstance(r.label_position, ft.LabelPosition)
    assert isinstance(r._get_attr('labelPosition'), str)
    assert r.label_position == ft.LabelPosition.LEFT
    assert r._get_attr('labelPosition') == ft.LabelPosition.LEFT.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['labelposition'] == 'left'


def test_label_position_str():
    r = ft.Switch(label_position='left')
    assert isinstance(r.label_position, ft.LabelPosition)
    assert isinstance(r._get_attr('labelPosition'), str)
    assert r.label_position == ft.LabelPosition.LEFT
    assert r._get_attr('labelPosition') == ft.LabelPosition.LEFT.value
    cmd = r._build_add_commands()
    assert cmd[0].attrs['labelposition'] == 'left'
