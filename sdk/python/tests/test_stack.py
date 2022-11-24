import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Stack()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["stack"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_clip_behavior_enum():
    r = ft.Stack()
    assert r.clip_behavior is None
    assert r._get_attr("clipBehavior") is None

    r = ft.Stack(clip_behavior=ft.ClipBehavior.ANTI_ALIAS)
    assert isinstance(r.clip_behavior, ft.ClipBehavior)
    assert r.clip_behavior == ft.ClipBehavior.ANTI_ALIAS
    assert r._get_attr("clipBehavior") == "antiAlias"

    r = ft.Stack(clip_behavior="none")
    assert isinstance(r.clip_behavior, str)
    assert r._get_attr("clipBehavior") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Stack(clip_behavior="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Stack(clip_behavior=1)
