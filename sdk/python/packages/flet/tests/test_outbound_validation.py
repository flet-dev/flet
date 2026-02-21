import re
from typing import Annotated

import pytest

import flet as ft
from flet.controls._validation import V
from flet.controls.base_control import BaseControl, control
from flet.controls.object_patch import ObjectPatch


def _assert_value_error(control: BaseControl, message: str) -> None:
    with pytest.raises(ValueError, match=re.escape(message)):
        control._before_update_safe()


def test_inherited_field_rule_validates_control_opacity():
    text = ft.Text("Hello", opacity=1.2)

    _assert_value_error(
        text,
        "opacity must be between 0.0 and 1.0 inclusive, got 1.2",
    )


def test_slider_class_rules_use_default_comparison_messages():
    slider_min_gt_max = ft.Slider(min=2, max=1)
    _assert_value_error(
        slider_min_gt_max,
        "min (2) must be less than or equal to max (1)",
    )

    slider_value_lt_min = ft.Slider(min=2, max=5, value=1)
    _assert_value_error(
        slider_value_lt_min,
        "value (1) must be greater than or equal to min (2)",
    )


def test_range_slider_rules_run_via_base_control_safe_hook():
    slider = ft.RangeSlider(start_value=0, end_value=2, max=1)

    # `before_update()` alone should not run outbound validators.
    slider.before_update()
    _assert_value_error(slider, "end_value (2) must be less than or equal to max (1)")


def test_safe_area_content_visibility_rule_keeps_message():
    safe_area = ft.SafeArea(content=ft.Text("content", visible=False))

    _assert_value_error(safe_area, "content must be visible")


def test_textfield_validation_and_normalization_both_work():
    valid_textfield = ft.TextField(min_lines=1, max_lines=3, bgcolor=ft.Colors.RED)
    assert valid_textfield.filled is None
    valid_textfield._before_update_safe()
    assert valid_textfield.filled is True

    invalid_textfield = ft.TextField(max_length=0)
    _assert_value_error(
        invalid_textfield,
        "max_length must be either equal to -1 or greater than 0",
    )

    invalid_min_lines = ft.TextField(min_lines=0)
    _assert_value_error(
        invalid_min_lines,
        "min_lines must be strictly greater than 0, got 0",
    )


def test_valid_controls_still_serialize_through_object_patch():
    slider = ft.Slider(min=0, max=10, value=5)
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        None, slider, control_cls=BaseControl
    )

    assert len(patch.patch) > 0
    assert slider in added_controls
    assert removed_controls == []


def test_default_field_message_is_used_when_message_is_omitted():
    @control("DefaultFieldMessageControl")
    class DefaultFieldMessageControl(BaseControl):
        value: Annotated[int, V.gt(0)] = 0

    control_instance = DefaultFieldMessageControl()
    _assert_value_error(
        control_instance,
        "value must be strictly greater than 0, got 0",
    )


def test_default_control_message_is_used_when_message_is_omitted():
    @control("DefaultControlMessageControl")
    class DefaultControlMessageControl(BaseControl):
        start: int = 2
        end: int = 1
        __outbound_rules__ = (V.ensure(lambda control: control.start <= control.end),)

    control_instance = DefaultControlMessageControl()
    _assert_value_error(
        control_instance,
        "Control validation failed.",
    )
