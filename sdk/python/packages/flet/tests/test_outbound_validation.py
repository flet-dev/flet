import re
from typing import Annotated, Optional

import pytest

import flet as ft
from flet.controls._validation import V
from flet.controls.base_control import BaseControl, control
from flet.controls.control import Control as FletControl
from flet.controls.object_patch import ObjectPatch


def _assert_value_error(control: BaseControl, message: str) -> None:
    with pytest.raises(ValueError, match=re.escape(message)):
        control._before_update_safe()


def test_inherited_field_rule_validates_control_opacity():
    _assert_value_error(
        ft.Text("Hello", opacity=1.2),
        "opacity must be between 0.0 and 1.0 inclusive, got 1.2",
    )


def test_slider_class_rules_use_default_comparison_messages():
    _assert_value_error(
        ft.Slider(min=5, max=1),
        "min (5) must be less than or equal to max (1)",
    )

    _assert_value_error(
        ft.Slider(min=2, max=5, value=1),
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


def test_field_rule_auto_allows_none_for_optional_fields():
    @control("OptionalFieldRuleControl")
    class OptionalFieldRuleControl(BaseControl):
        value: Annotated[Optional[int], V.gt(0)] = None

    OptionalFieldRuleControl()._before_update_safe()


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


def test_control_rule_auto_allows_none_for_optional_fields():
    @control("AutoOptionalNoneControl")
    class AutoOptionalNoneControl(BaseControl):
        left: Optional[int] = None
        right: int = 10
        __outbound_rules__ = (V.fields_le("left", "right"),)

    # `left` is Optional, so None is auto-allowed by `fields_le`.
    AutoOptionalNoneControl()._before_update_safe()


def test_control_rule_none_is_rejected_for_non_optional_fields():
    @control("NonOptionalNoneControl")
    class NonOptionalNoneControl(BaseControl):
        left: int = 1
        right: int = 10
        __outbound_rules__ = (V.fields_le("left", "right"),)

    control_instance = NonOptionalNoneControl()
    control_instance.left = None
    _assert_value_error(
        control_instance,
        "left (None) must be less than or equal to right (10)",
    )


def test_visible_control_rule_uses_default_field_name_message():
    @control("VisibleControlMessageControl")
    class VisibleControlMessageControl(BaseControl):
        child: Annotated[FletControl, V.visible_control()]

    control_instance = VisibleControlMessageControl(child=ft.Text(visible=False))
    _assert_value_error(control_instance, "child must be visible")


def test_visible_control_rule_auto_allows_none_for_optional_field():
    @control("OptionalVisibleControlRuleControl")
    class OptionalVisibleControlRuleControl(BaseControl):
        child: Annotated[Optional[FletControl], V.visible_control()] = None

    OptionalVisibleControlRuleControl()._before_update_safe()


def test_str_or_visible_control_rule_defaults_and_optional_none():
    @control("StringOrVisibleControlRuleControl")
    class StringOrVisibleControlRuleControl(BaseControl):
        value: Annotated[FletControl, V.str_or_visible_control()]

    _assert_value_error(
        StringOrVisibleControlRuleControl(value=ft.Text(visible=False)),
        "value must be a string or a visible Control",
    )

    @control("OptionalStringOrVisibleControlRuleControl")
    class OptionalStringOrVisibleControlRuleControl(BaseControl):
        value: Annotated[Optional[FletControl], V.str_or_visible_control()] = None

    OptionalStringOrVisibleControlRuleControl()._before_update_safe()
