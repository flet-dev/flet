import flet as ft
from flet.core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"))
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["animatedswitcher"],
            attrs={},
            commands=[],
        ),
        Command(
            indent=2,
            name=None,
            values=["text"],
            attrs={"n": "content", "value": "Hello!"},
            commands=[],
        ),
    ], "Test failed"


def test_switch_in_curve_enum():
    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"))
    assert r.switch_in_curve is None
    assert r._get_attr("switchInCurve") is None

    r = ft.AnimatedSwitcher(
        content=ft.Text("Hello!"), switch_in_curve=ft.AnimationCurve.BOUNCE_IN
    )
    assert isinstance(r.switch_in_curve, ft.AnimationCurve)
    assert r.switch_in_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr("switchInCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"), switch_in_curve="easeIn")
    assert isinstance(r.switch_in_curve, str)
    assert r._get_attr("switchInCurve") == "easeIn"


def test_switch_out_curve_enum():
    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"))
    assert r.switch_out_curve is None
    assert r._get_attr("switchOutCurve") is None

    r = ft.AnimatedSwitcher(
        content=ft.Text("Hello!"), switch_out_curve=ft.AnimationCurve.BOUNCE_IN
    )
    assert isinstance(r.switch_out_curve, ft.AnimationCurve)
    assert r.switch_out_curve == ft.AnimationCurve.BOUNCE_IN
    assert r._get_attr("switchOutCurve") == "bounceIn"

    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"), switch_out_curve="easeIn")
    assert isinstance(r.switch_out_curve, str)
    assert r._get_attr("switchOutCurve") == "easeIn"


def test_transition_enum():
    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"))
    assert r.transition is None
    assert r._get_attr("transition") is None

    r = ft.AnimatedSwitcher(
        content=ft.Text("Hello!"), transition=ft.AnimatedSwitcherTransition.FADE
    )
    assert isinstance(r.transition, ft.AnimatedSwitcherTransition)
    assert r.transition == ft.AnimatedSwitcherTransition.FADE
    assert r._get_attr("transition") == "fade"

    r = ft.AnimatedSwitcher(content=ft.Text("Hello!"), transition="scale")
    assert isinstance(r.transition, str)
    assert r._get_attr("transition") == "scale"
