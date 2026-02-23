import re
from dataclasses import dataclass, field
from typing import Annotated, Optional

import pytest

from flet.utils.validation import (
    ClassRule,
    V,
    ValidationDeclarationError,
    ValidationRules,
    validate,
)


@dataclass
class _Visible:
    visible: bool = True


def test_field_wrapper_and_class_rule_delegate_callbacks():
    """Verify `V.field()` and `ClassRule(...)` execute provided callbacks."""
    called: dict[str, object] = {}

    def check_field(ctrl, field_name, value):
        called["field"] = (field_name, value, ctrl.marker)

    def check_control(ctrl):
        called["control"] = ctrl.marker

    @dataclass
    class Sample:
        marker: str = "ok"
        value: Annotated[int, V.field(check_field)] = 7
        __validation_rules__: ValidationRules = (ClassRule(check_control),)

    validate(Sample())

    assert called["field"] == ("value", 7, "ok")
    assert called["control"] == "ok"


def test_ensure_default_messages_for_named_and_lambda_predicates():
    """Check fallback `V.ensure()` error messages for named and lambda predicates."""

    def always_false(_ctrl):
        return False

    @dataclass
    class NamedPredicateControl:
        __validation_rules__: ValidationRules = (V.ensure(always_false),)

    with pytest.raises(ValueError, match="Validation failed: always_false"):
        validate(NamedPredicateControl())

    @dataclass
    class LambdaPredicateControl:
        __validation_rules__: ValidationRules = (V.ensure(lambda _ctrl: False),)

    with pytest.raises(ValueError, match="Validation failed."):
        validate(LambdaPredicateControl())


def test_ensure_uses_custom_message_and_allows_pass():
    """
    Confirm `V.ensure()` accepts passing values and emits callable custom messages.
    """

    @dataclass
    class Sample:
        ok: bool = True
        name: str = "alpha"
        __validation_rules__: ValidationRules = (
            V.ensure(lambda ctrl: ctrl.ok, message=lambda ctrl: f"{ctrl.name} failed"),
        )

    validate(Sample(ok=True))

    with pytest.raises(ValueError, match="alpha failed"):
        validate(Sample(ok=False))


def test_instance_of_supports_optional_none_and_expected_types():
    """
    Ensure `V.instance_of()` allows `None` when the field annotation is `Optional`.
    """

    @dataclass
    class Sample:
        value: Annotated[Optional[int], V.instance_of(int)] = None

    validate(Sample(value=None))
    validate(Sample(value=5))


def test_instance_of_reports_default_type_errors():
    """Validate default type error formatting for `V.instance_of()` tuples."""

    @dataclass
    class Sample:
        value: Annotated[int, V.instance_of((int, str, float))] = 0

    with pytest.raises(
        ValueError,
        match="value must be of type int, str, or float, got <class 'list'>",
    ):
        validate(Sample(value=[]))  # type: ignore[arg-type]


def test_instance_of_uses_custom_message_callable():
    """Verify `V.instance_of()` uses a callable custom error message."""

    @dataclass
    class Sample:
        value: Annotated[int, V.instance_of(int, message=lambda *_: "wrong type")] = 0  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="wrong type"):
        validate(Sample(value="x"))  # type: ignore[arg-type]


def test_visible_control_accepts_visible_and_optional_none():
    """Check `V.visible_control()` accepts visible controls and optional `None`."""

    @dataclass
    class OptionalSample:
        child: Annotated[Optional[_Visible], V.visible_control()] = None

    validate(OptionalSample(child=None))
    validate(OptionalSample(child=_Visible(visible=True)))


def test_visible_control_fails_for_hidden_or_none_with_custom_message():
    """
    Ensure `V.visible_control()` rejects hidden/required-None values with custom text.
    """

    @dataclass
    class RequiredSample:
        child: Annotated[_Visible, V.visible_control(message="child invalid")] = field(
            default_factory=_Visible
        )

    with pytest.raises(ValueError, match="child invalid"):
        validate(RequiredSample(child=_Visible(visible=False)))

    with pytest.raises(ValueError, match="child invalid"):
        validate(RequiredSample(child=None))  # type: ignore[arg-type]


def test_visible_controls_validates_min_count_and_default_messages():
    """
    Cover `V.visible_controls()` min-count validation and default failure messages.
    """
    with pytest.raises(
        ValidationDeclarationError,
        match="min_count must be greater than or equal to 1, got 0",
    ):
        V.visible_controls(min_count=0)

    @dataclass
    class OneRequired:
        children: Annotated[list[_Visible], V.visible_controls(min_count=1)] = field(
            default_factory=list
        )

    @dataclass
    class TwoRequired:
        children: Annotated[list[_Visible], V.visible_controls(min_count=2)] = field(
            default_factory=list
        )

    with pytest.raises(
        ValueError,
        match="children must contain at least one visible Control, got 0",
    ):
        validate(OneRequired(children=[]))

    with pytest.raises(
        ValueError,
        match="children must contain at least 2 visible Controls, got 1",
    ):
        validate(
            TwoRequired(children=[_Visible(visible=True), _Visible(visible=False)])
        )

    with pytest.raises(
        ValueError,
        match="children must contain at least one visible Control, got 0",
    ):
        validate(OneRequired(children=123))  # type: ignore[arg-type]


def test_visible_controls_uses_custom_message_on_type_error_and_count_mismatch():
    """Ensure `V.visible_controls()` applies custom messages for all failure modes."""

    @dataclass
    class Sample:
        children: Annotated[
            list[_Visible], V.visible_controls(min_count=2, message="bad children")
        ] = field(default_factory=list)

    with pytest.raises(ValueError, match="bad children"):
        validate(Sample(children=42))  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="bad children"):
        validate(Sample(children=[_Visible(True), _Visible(False)]))


def test_str_or_visible_control_allows_string_or_visible_control():
    """
    Verify `V.str_or_visible_control()` accepts only string or visible control values.
    """

    @dataclass
    class Sample:
        label: Annotated[object, V.str_or_visible_control()]

    validate(Sample(label="text"))
    validate(Sample(label=_Visible(visible=True)))

    with pytest.raises(ValueError, match="label must be a string or a visible Control"):
        validate(Sample(label=_Visible(visible=False)))


@pytest.mark.parametrize(
    ("rule", "valid_value", "invalid_value", "error_message"),
    [
        (V.gt(5), 6, 5, "value must be strictly greater than 5, got 5"),
        (V.ge(5), 5, 4, "value must be greater than or equal to 5, got 4"),
        (V.lt(5), 4, 5, "value must be less than 5, got 5"),
        (V.le(5), 5, 6, "value must be less than or equal to 5, got 6"),
        (
            V.between(2, 4),
            3,
            5,
            "value must be between 2 and 4 inclusive, got 5",
        ),
    ],
)
def test_numeric_rules(rule, valid_value, invalid_value, error_message):
    """Parametrically validate scalar comparison rules and their default messages."""

    @dataclass
    class Sample:
        value: Annotated[int, rule] = valid_value

    validate(Sample(value=valid_value))
    with pytest.raises(ValueError, match=error_message):
        validate(Sample(value=invalid_value))


def test_numeric_rules_handle_optional_none_and_custom_message_for_required_none():
    """
    Verify scalar rules skip optional `None` and fail required `None` with custom text.
    """

    @dataclass
    class OptionalSample:
        value: Annotated[Optional[int], V.gt(0)] = None

    validate(OptionalSample(value=None))

    @dataclass
    class RequiredSample:
        value: Annotated[int, V.gt(0, message="missing number")] = 1

    with pytest.raises(ValueError, match="missing number"):
        validate(RequiredSample(value=None))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("rule", "valid_value", "invalid_value", "error_message"),
    [
        (
            V.factor_of(60),
            -15,
            7,
            "value must be a factor of 60, got 7",
        ),
        (
            V.multiple_of(-5),
            -15,
            14,
            "value must be a multiple of 5, got 14",
        ),
    ],
)
def test_divisibility_rules(rule, valid_value, invalid_value, error_message):
    """Validate factor/multiple helpers and their default error messages."""

    @dataclass
    class Sample:
        value: Annotated[int, rule]

    validate(Sample(value=valid_value))
    with pytest.raises(ValueError, match=re.escape(error_message)):
        validate(Sample(value=invalid_value))


def test_divisibility_rules_support_optional_none_and_custom_message():
    """Ensure divisibility rules honor optional-None inference and custom text."""

    @dataclass
    class OptionalSample:
        value: Annotated[Optional[int], V.factor_of(60)] = None

    @dataclass
    class RequiredSample:
        value: Annotated[int, V.multiple_of(5, message="bad multiple")]

    validate(OptionalSample(value=None))

    with pytest.raises(ValueError, match="bad multiple"):
        validate(RequiredSample(value=6))


def test_divisibility_rules_validate_builder_arguments():
    """Verify declaration-time validation for divisor/base arguments."""

    with pytest.raises(
        ValidationDeclarationError, match="base must be a non-zero integer"
    ):
        V.factor_of(0)

    with pytest.raises(
        ValidationDeclarationError, match="divisor must be a non-zero integer"
    ):
        V.multiple_of(0)


@pytest.mark.parametrize(
    ("rule", "valid_value", "invalid_value", "error_message"),
    [
        (V.eq(5), 5, 4, "value must be equal to 5, got 4"),
        (V.ne(5), 4, 5, "value must not be equal to 5, got 5"),
        (
            V.one_of(("small", "medium", "large")),
            "medium",
            "x-large",
            "value must be one of 'small', 'medium', or 'large', got 'x-large'",
        ),
    ],
)
def test_equality_and_membership_rules(rule, valid_value, invalid_value, error_message):
    """Validate equality/membership rules and their default error messages."""

    @dataclass
    class Sample:
        value: Annotated[object, rule]

    validate(Sample(value=valid_value))
    with pytest.raises(ValueError, match=re.escape(error_message)):
        validate(Sample(value=invalid_value))


def test_one_of_requires_non_empty_allowed_values():
    """Ensure `V.one_of()` rejects empty allowed-value collections."""
    with pytest.raises(
        ValidationDeclarationError,
        match="allowed_values must contain at least one value",
    ):
        V.one_of(())


def test_or_rule_accepts_when_any_rule_passes_and_composes_default_error():
    """
    Verify `V.or_()` accepts if any nested rule passes and combines failures by default.
    """

    @dataclass
    class Sample:
        value: Annotated[int, V.or_(V.eq(-1), V.gt(0))]

    validate(Sample(value=-1))
    validate(Sample(value=2))

    with pytest.raises(
        ValueError,
        match=re.escape(
            "value must satisfy at least one of the allowed conditions: "
            "value must be equal to -1, got 0; or "
            "value must be strictly greater than 0, got 0"
        ),
    ):
        validate(Sample(value=0))


def test_or_rule_uses_custom_message_and_validates_arguments():
    """Ensure `V.or_()` supports custom messages and validates builder input."""

    @dataclass
    class Sample:
        value: Annotated[int, V.or_(V.eq(1), V.eq(2), message="invalid choice")]

    with pytest.raises(ValueError, match="invalid choice"):
        validate(Sample(value=3))

    with pytest.raises(
        ValidationDeclarationError, match="or_ requires at least one field rule"
    ):
        V.or_()

    with pytest.raises(
        ValidationDeclarationError, match="or_ expects only FieldRule instances"
    ):
        V.or_(V.eq(1), "bad")  # type: ignore[arg-type]


def test_non_empty_rule_default_messages_and_optional_none_inference():
    """
    Validate `V.non_empty()` behavior for empty values, type errors,
    and optional `None`.
    """

    @dataclass
    class RequiredSample:
        value: Annotated[list[int], V.non_empty()] = field(default_factory=list)

    @dataclass
    class OptionalSample:
        value: Annotated[Optional[list[int]], V.non_empty()] = None

    with pytest.raises(ValueError, match="value must be non-empty"):
        validate(RequiredSample(value=[]))

    with pytest.raises(
        ValueError,
        match=re.escape("value must be a non-empty sized value, got <class 'int'>"),
    ):
        validate(RequiredSample(value=123))  # type: ignore[arg-type]

    validate(OptionalSample(value=None))


def test_length_rules_default_messages_builder_checks_and_custom_message():
    """Cover length-rule defaults and builder constraints."""

    with pytest.raises(
        ValidationDeclarationError,
        match="minimum must be greater than or equal to 0, got -1",
    ):
        V.length_ge(-1)

    with pytest.raises(
        ValidationDeclarationError,
        match="expected must be greater than or equal to 0, got -1",
    ):
        V.length_eq(-1)

    with pytest.raises(
        ValidationDeclarationError,
        match=re.escape("maximum must be greater than or equal to minimum (2), got 1"),
    ):
        V.length_between(2, 1)

    @dataclass
    class MinLength:
        value: Annotated[str, V.length_ge(2)]

    @dataclass
    class BetweenLength:
        value: Annotated[list[int], V.length_between(1, 2, message="length invalid")]

    @dataclass
    class EqLength:
        value: Annotated[str, V.length_eq(3)]

    validate(MinLength(value="ok"))
    with pytest.raises(
        ValueError,
        match="value must have length greater than or equal to 2, got 1",
    ):
        validate(MinLength(value="x"))

    validate(EqLength(value="abc"))
    with pytest.raises(
        ValueError,
        match="value must have length equal to 3, got 2",
    ):
        validate(EqLength(value="ab"))

    with pytest.raises(ValueError, match="length invalid"):
        validate(BetweenLength(value=[]))

    with pytest.raises(ValueError, match="length invalid"):
        validate(BetweenLength(value=123))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("rule", "valid_pair", "invalid_pair", "error_message"),
    [
        (
            V.gt_field("other"),
            (3, 2),
            (2, 2),
            "current (2) must be strictly greater than other (2)",
        ),
        (
            V.ge_field("other"),
            (2, 2),
            (1, 2),
            "current (1) must be greater than or equal to other (2)",
        ),
        (
            V.lt_field("other"),
            (1, 2),
            (2, 2),
            "current (2) must be strictly less than other (2)",
        ),
        (
            V.le_field("other"),
            (2, 2),
            (3, 2),
            "current (3) must be less than or equal to other (2)",
        ),
    ],
)
def test_field_comparison_rules(rule, valid_pair, invalid_pair, error_message):
    """Parametrically validate field-to-field comparison rules and default messages."""

    @dataclass
    class Sample:
        current: Annotated[int, rule] = valid_pair[0]
        other: int = valid_pair[1]

    validate(Sample(current=valid_pair[0], other=valid_pair[1]))
    with pytest.raises(ValueError, match=re.escape(error_message)):
        validate(Sample(current=invalid_pair[0], other=invalid_pair[1]))


def test_field_comparison_rules_skip_when_optional_side_is_none():
    """
    Ensure field comparison rules skip when either annotated optional side is `None`.
    """

    @dataclass
    class CurrentOptional:
        current: Annotated[Optional[int], V.gt_field("other")]
        other: int

    @dataclass
    class OtherOptional:
        current: Annotated[int, V.gt_field("other")]
        other: Optional[int] = None

    validate(CurrentOptional(current=None, other=3))
    validate(OtherOptional(current=5, other=None))


def test_field_comparison_rules_use_custom_message_for_required_none():
    """
    Confirm field comparison rules use custom messages when required values are `None`.
    """

    @dataclass
    class Sample:
        current: Annotated[int, V.gt_field("other", message="comparison failed")]
        other: int

    with pytest.raises(ValueError, match="comparison failed"):
        validate(Sample(current=None, other=1))  # type: ignore[arg-type]


def test_validate_runs_field_rules_before_class_rules():
    """Verify field-level validation runs before class-level validation."""
    events: list[str] = []

    def fail_field(_ctrl, _field_name, _value):
        events.append("field")
        raise ValueError("field failed")

    def run_control(_ctrl):
        events.append("control")

    @dataclass
    class Sample:
        value: Annotated[int, V.field(fail_field)] = 1
        __validation_rules__: ValidationRules = (ClassRule(run_control),)

    with pytest.raises(ValueError, match="field failed"):
        validate(Sample())

    assert events == ["field"]


def test_validate_merges_mro_rules_in_base_to_child_order():
    """Ensure compiled validation rules follow MRO base-to-child ordering semantics."""

    def field_rule(tag: str):
        return V.field(lambda ctrl, _field_name, _value: ctrl.events.append(tag))

    def control_rule(tag: str):
        return ClassRule(lambda ctrl: ctrl.events.append(tag))

    @dataclass
    class Base:
        events: list[str] = field(default_factory=list)
        value: Annotated[int, field_rule("base_field")] = 1
        __validation_rules__: ValidationRules = (control_rule("base_control"),)

    @dataclass
    class Child(Base):
        value: Annotated[int, field_rule("child_field")] = 2
        __validation_rules__ = (
            control_rule("child_control"),
            "not-a-rule",
        )

    child = Child()
    validate(child)

    assert child.events == [
        "base_field",
        "child_field",
        "base_control",
        "child_control",
    ]
