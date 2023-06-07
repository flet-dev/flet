import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.AnimatedSwitcher()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["animatedswitcher"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_switch_in_curve_enum():
    r = ft.AnimatedSwitcher()
    assert r.switch_in_curve == ft.AnimationCurve.LINEAR
    assert r._get_attr("switchInCurve") is None

    r = ft.AnimatedSwitcher(switch_in_curve=ft.AnimationCurve.BOUNCE_IN)
    assert isinstance(r.switch_in_curve, ft.AnimationCurve)
    assert isinstance(r._get_attr("switchInCurve"), str)
    assert r.switch_in_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr('switchInCurve') == ft.AnimationCurve.BOUNCE_IN.value
    assert r._get_attr("switchInCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(switch_in_curve="easeIn")
    assert isinstance(r.switch_in_curve, ft.AnimationCurve)
    assert isinstance(r._get_attr("switchInCurve"), str)
    assert r.switch_in_curve == ft.AnimationCurve.EASE_IN
    assert r._get_attr('switchInCurve') == ft.AnimationCurve.EASE_IN.value
    assert r._get_attr("switchInCurve") == "easeIn"


def test_switch_out_curve_enum():
    r = ft.AnimatedSwitcher()
    assert r.switch_out_curve == ft.AnimationCurve.LINEAR
    assert r._get_attr("switchOutCurve") is None

    r = ft.AnimatedSwitcher(switch_out_curve=ft.AnimationCurve.BOUNCE_IN)
    assert isinstance(r.switch_out_curve, ft.AnimationCurve)
    assert isinstance(r._get_attr("switchOutCurve"), str)
    assert r.switch_out_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr('switchOutCurve') == ft.AnimationCurve.BOUNCE_IN.value
    assert r._get_attr("switchOutCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(switch_out_curve="easeIn")
    assert isinstance(r.switch_out_curve, ft.AnimationCurve)
    assert isinstance(r._get_attr("switchOutCurve"), str)
    assert r.switch_out_curve == ft.AnimationCurve.EASE_IN
    assert r._get_attr('switchOutCurve') == ft.AnimationCurve.EASE_IN.value
    assert r._get_attr("switchOutCurve") == "easeIn"


def test_transition_enum():
    r = ft.AnimatedSwitcher()
    assert r.transition == ft.AnimatedSwitcherTransition.FADE
    assert r._get_attr("transition") is None

    r = ft.AnimatedSwitcher(transition=ft.AnimatedSwitcherTransition.ROTATION)
    assert isinstance(r.transition, ft.AnimatedSwitcherTransition)
    assert isinstance(r._get_attr("transition"), str)
    assert r.transition == ft.AnimatedSwitcherTransition.ROTATION
    assert r._get_attr('transition') == ft.AnimatedSwitcherTransition.ROTATION.value
    assert r._get_attr("transition") == "rotation"

    r = ft.AnimatedSwitcher(transition="scale")
    assert isinstance(r.transition, ft.AnimatedSwitcherTransition)
    assert isinstance(r._get_attr("transition"), str)
    assert r.transition == ft.AnimatedSwitcherTransition.SCALE
    assert r._get_attr('transition') == ft.AnimatedSwitcherTransition.SCALE.value
    assert r._get_attr("transition") == "scale"

