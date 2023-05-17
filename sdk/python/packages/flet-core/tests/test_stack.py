import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Stack()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=['stack'],
            attrs={'clipbehavior': 'hardEdge'},
            commands=[],
        )
    ], 'Test failed'


def test_clip_behavior_enum():
    r = ft.Stack()
    assert r.clip_behavior == ft.ClipBehavior.HARD_EDGE
    assert r._get_attr('clipBehavior') == ft.ClipBehavior.HARD_EDGE.value

    r = ft.Stack(clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert isinstance(r._get_attr("clipBehavior"), str)
    assert r.clip_behavior == ft.ClipBehavior.ANTI_ALIAS
    assert r._get_attr("clipBehavior") == "antiAlias"

    r = ft.Stack(clip_behavior='none')
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert isinstance(r._get_attr("clipBehavior"), str)
    assert r.clip_behavior == ft.ClipBehavior.NONE
    assert r._get_attr('clipBehavior') == 'none'
