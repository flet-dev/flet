import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


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
    assert r.switch_in_curve == None
    assert r._get_attr("switchInCurve") is None

    r = ft.AnimatedSwitcher(switch_in_curve=ft.AnimationCurve.BOUNCE_IN)
    assert isinstance(r.switch_in_curve, ft.AnimationCurve)
    assert r.switch_in_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr("switchInCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(switch_in_curve="easeIn")
    assert isinstance(r.switch_in_curve, str)
    assert r._get_attr("switchInCurve") == "easeIn"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(switch_in_curve="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(switch_in_curve=1)


def test_switch_out_curve_enum():
    r = ft.AnimatedSwitcher()
    assert r.switch_out_curve == None
    assert r._get_attr("switchOutCurve") is None

    r = ft.AnimatedSwitcher(switch_out_curve=ft.AnimationCurve.BOUNCE_IN)
    assert isinstance(r.switch_out_curve, ft.AnimationCurve)
    assert r.switch_out_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr("switchOutCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(switch_out_curve="easeIn")
    assert isinstance(r.switch_out_curve, str)
    assert r._get_attr("switchOutCurve") == "easeIn"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(switch_out_curve="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(switch_out_curve=1)


def test_transition_enum():
    r = ft.AnimatedSwitcher()
    assert r.transition == None
    assert r._get_attr("transition") is None

    r = ft.AnimatedSwitcher(transition=ft.AnimatedSwitcherTransition.FADE)
    assert isinstance(r.transition, ft.AnimatedSwitcherTransition)
    assert r.transition == ft.AnimatedSwitcherTransition.FADE
    assert r._get_attr("transition") == "fade"

    r = ft.AnimatedSwitcher(transition="scale")
    assert isinstance(r.transition, str)
    assert r._get_attr("transition") == "scale"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(transition="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.AnimatedSwitcher(transition=1)
