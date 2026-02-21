"""
Internal outbound validation helpers for Flet controls.

This module provides small composable rule objects that can be attached to control
fields via `typing.Annotated` and to controls via `__outbound_rules__`.
The runtime calls `validate_outbound()` before patch serialization so invalid
state is rejected on the Python side before reaching Dart.
"""

import sys
from dataclasses import dataclass
from functools import cache
from typing import (
    Annotated,
    Any,
    Callable,
    Optional,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

__all__ = [
    "ControlRule",
    "FieldRule",
    "V",
    "validate_outbound",
]

FieldCheck = Callable[[Any, str, Any], None]
FieldMessage = Union[str, Callable[[Any, str, Any], str]]
ControlCheck = Callable[[Any], None]
ControlMessage = Union[str, Callable[[Any], str]]
ControlPredicate = Callable[[Any], bool]


@dataclass(frozen=True)
class FieldRule:
    """A single validation rule applied to one field value."""

    _check: FieldCheck

    def validate(self, control: Any, field_name: str, value: Any) -> None:
        """Validate one field value for a specific control instance."""
        self._check(control, field_name, value)


@dataclass(frozen=True)
class ControlRule:
    """A validation rule that can inspect multiple fields on a control."""

    _check: ControlCheck

    def validate(self, control: Any) -> None:
        """Validate a control instance."""
        self._check(control)


@dataclass(frozen=True)
class _ClassValidationSpec:
    """Compiled validation specification for a control class."""

    field_rules: tuple[tuple[str, FieldRule], ...]
    control_rules: tuple[ControlRule, ...]


def _resolve_field_message(
    message: FieldMessage, control: Any, field_name: str, value: Any
) -> str:
    """Render a field-level message that may be static text or a callable."""
    if callable(message):
        return message(control, field_name, value)
    return message


def _resolve_control_message(message: ControlMessage, control: Any) -> str:
    """Render a control-level message that may be static text or a callable."""
    if callable(message):
        return message(control)
    return message


def _format_expected_type(
    expected_type: Union[type[Any], tuple[type[Any], ...]],
) -> str:
    """Format expected type(s) into a readable sentence fragment."""
    if not isinstance(expected_type, tuple):
        return expected_type.__name__
    names = [t.__name__ for t in expected_type]
    if len(names) == 0:
        return "unknown"
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} or {names[1]}"
    return f"{', '.join(names[:-1])}, or {names[-1]}"


class V:
    """
    Validation rule builder namespace.

    Methods return `FieldRule` or `ControlRule` instances which are attached to
    control fields (`Annotated[...]`) or class-level `__outbound_rules__`.
    """

    @staticmethod
    def field(check: FieldCheck) -> FieldRule:
        """Wrap a custom field validator callback into a `FieldRule`."""
        return FieldRule(check)

    @staticmethod
    def control(check: ControlCheck) -> ControlRule:
        """Wrap a custom control validator callback into a `ControlRule`."""
        return ControlRule(check)

    @staticmethod
    def ensure(
        predicate: ControlPredicate,
        *,
        message: Optional[ControlMessage] = None,
    ) -> ControlRule:
        """
        Build a generic control-level predicate rule.

        When `message` is omitted, a generic fallback is used.
        """

        def _check(control: Any) -> None:
            if not predicate(control):
                if message is not None:
                    raise ValueError(_resolve_control_message(message, control))
                predicate_name = getattr(predicate, "__name__", None)
                if predicate_name and predicate_name != "<lambda>":
                    raise ValueError(f"Control validation failed: {predicate_name}")
                raise ValueError("Control validation failed.")

        return ControlRule(_check)

    @staticmethod
    def instance_of(
        expected_type: Union[type[Any], tuple[type[Any], ...]],
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate a field value type with an optional custom error message.

        Args:
            expected_type: Allowed runtime type(s).
            message: Optional custom error message/template.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if value is None and _resolve_allow_none_for_field(
                control.__class__, field_name
            ):
                return
            if not isinstance(value, expected_type):
                if message is None:
                    raise ValueError(
                        f"{field_name} must be of type "
                        f"{_format_expected_type(expected_type)}, got {type(value)}"
                    )
                raise ValueError(
                    _resolve_field_message(message, control, field_name, value)
                )

        return FieldRule(_check)

    @staticmethod
    def visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is visible, i.e. `Control.visible` is `True`.

        Args:
            message: Optional custom error text or formatter.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (f"{field_name} must be visible"),
            ):
                return
            if getattr(value, "visible", False):
                return
            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, control, field_name, value)
                )
            raise ValueError(f"{field_name} must be visible")

        return FieldRule(_check)

    @staticmethod
    def str_or_visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is either a string or a visible control.

        Args:
            message: Optional custom error text or formatter.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must be a string or a visible Control"
                ),
            ):
                return
            if isinstance(value, str) or getattr(value, "visible", False):
                return
            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, control, field_name, value)
                )
            raise ValueError(f"{field_name} must be a string or a visible Control")

        return FieldRule(_check)

    @staticmethod
    def gt(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value > bound`.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be strictly greater than {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value <= bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, control, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be strictly greater than {bound}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def ge(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value >= bound`.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be greater than or equal to {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value < bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, control, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be greater than or equal to {bound}, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def lt(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value < bound`.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be less than {bound}, got {current_value}"
                ),
            ):
                return
            if value >= bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, control, field_name, value)
                    )
                raise ValueError(f"{field_name} must be less than {bound}, got {value}")

        return FieldRule(_check)

    @staticmethod
    def le(
        bound: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value <= bound`.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be less than or equal to {bound}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value > bound:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, control, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be less than or equal to {bound}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def between(
        minimum: Any,
        maximum: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `minimum <= value <= maximum`.
        """

        def _check(control: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                control=control,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be between {minimum} and {maximum} inclusive, "
                    f"got {current_value}"
                ),
            ):
                return
            if not (minimum <= value <= maximum):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, control, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be between {minimum} and {maximum} inclusive, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def fields_gt(
        left_field: str,
        right_field: str,
        *,
        message: Optional[ControlMessage] = None,
    ) -> ControlRule:
        """
        Validate `left_field > right_field` on a control instance.

        Args:
            left_field: Name of the field on the left side of the comparison.
            right_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(control: Any) -> None:
            left_value, right_value, skip = _prepare_comparison_values(
                control=control,
                left_field=left_field,
                right_field=right_field,
                message=message,
                default_error=lambda left, right: (
                    f"{left_field} ({left}) must be strictly greater than "
                    f"{right_field} ({right})"
                ),
            )
            if skip:
                return
            if left_value <= right_value:
                if message is not None:
                    raise ValueError(_resolve_control_message(message, control))
                raise ValueError(
                    f"{left_field} ({left_value}) must be strictly greater than "
                    f"{right_field} ({right_value})"
                )

        return ControlRule(_check)

    @staticmethod
    def fields_ge(
        left_field: str,
        right_field: str,
        *,
        message: Optional[ControlMessage] = None,
    ) -> ControlRule:
        """
        Validate `left_field >= right_field` on a control instance.

        Args:
            left_field: Name of the field on the left side of the comparison.
            right_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(control: Any) -> None:
            left_value, right_value, skip = _prepare_comparison_values(
                control=control,
                left_field=left_field,
                right_field=right_field,
                message=message,
                default_error=lambda left, right: (
                    f"{left_field} ({left}) must be greater than or equal to "
                    f"{right_field} ({right})"
                ),
            )
            if skip:
                return
            if left_value < right_value:
                if message is not None:
                    raise ValueError(_resolve_control_message(message, control))
                raise ValueError(
                    f"{left_field} ({left_value}) must be greater than or equal to "
                    f"{right_field} ({right_value})"
                )

        return ControlRule(_check)

    @staticmethod
    def fields_lt(
        left_field: str,
        right_field: str,
        *,
        message: Optional[ControlMessage] = None,
    ) -> ControlRule:
        """
        Validate `left_field < right_field` on a control instance.

        Args:
            left_field: Name of the field on the left side of the comparison.
            right_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(control: Any) -> None:
            left_value, right_value, skip = _prepare_comparison_values(
                control=control,
                left_field=left_field,
                right_field=right_field,
                message=message,
                default_error=lambda left, right: (
                    f"{left_field} ({left}) must be strictly less than "
                    f"{right_field} ({right})"
                ),
            )
            if skip:
                return
            if left_value >= right_value:
                if message is not None:
                    raise ValueError(_resolve_control_message(message, control))
                raise ValueError(
                    f"{left_field} ({left_value}) must be strictly less than "
                    f"{right_field} ({right_value})"
                )

        return ControlRule(_check)

    @staticmethod
    def fields_le(
        left_field: str,
        right_field: str,
        *,
        message: Optional[ControlMessage] = None,
    ) -> ControlRule:
        """
        Validate `left_field <= right_field` on a control instance.

        Args:
            left_field: Name of the field on the left side of the comparison.
            right_field: Name of the field on the right side of the comparison.
            message: Optional custom error text or formatter.
        """

        def _check(control: Any) -> None:
            left_value, right_value, skip = _prepare_comparison_values(
                control=control,
                left_field=left_field,
                right_field=right_field,
                message=message,
                default_error=lambda left, right: (
                    f"{left_field} ({left}) must be less than or equal to "
                    f"{right_field} ({right})"
                ),
            )
            if skip:
                return
            if left_value > right_value:
                if message is not None:
                    raise ValueError(_resolve_control_message(message, control))
                raise ValueError(
                    f"{left_field} ({left_value}) must be less than or equal to "
                    f"{right_field} ({right_value})"
                )

        return ControlRule(_check)


def _get_declared_type_hints(cls: type[Any]) -> dict[str, Any]:
    """
    Resolve declared annotations for one class with best-effort extras support.

    Only annotations declared directly on `cls` are returned. This allows MRO-based
    merging in `_compile_class_spec()` without duplicating inherited members.
    """

    annotations = getattr(cls, "__annotations__", {})
    if not annotations:
        return {}

    module = sys.modules.get(cls.__module__)
    globalns = module.__dict__ if module else None
    try:
        type_hints = get_type_hints(cls, globalns=globalns, include_extras=True)
    except TypeError:
        type_hints = get_type_hints(cls, globalns=globalns)
    except Exception:
        type_hints = annotations

    return {name: type_hints.get(name, hint) for name, hint in annotations.items()}


@cache
def _get_effective_type_hints(cls: type[Any]) -> dict[str, Any]:
    """
    Resolve effective annotations for `cls`, including inherited fields.

    The result is used for Optional/None inference in cross-field control rules.
    """

    module = sys.modules.get(cls.__module__)
    globalns = module.__dict__ if module else None
    try:
        return get_type_hints(cls, globalns=globalns, include_extras=True)
    except TypeError:
        return get_type_hints(cls, globalns=globalns)
    except Exception:
        hints: dict[str, Any] = {}
        for base in reversed(cls.__mro__):
            hints.update(getattr(base, "__annotations__", {}))
        return hints


def _strip_annotated(annotation: Any) -> Any:
    """
    Remove `Annotated[...]` wrapper(s), returning the core annotation type.
    """

    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


def _annotation_allows_none(annotation: Any) -> bool:
    """
    Return `True` if annotation contains `None` (for example `Optional[T]`).
    """

    annotation = _strip_annotated(annotation)
    origin = get_origin(annotation)
    if origin is Union:
        return any(arg is type(None) for arg in get_args(annotation))
    return False


def _resolve_allow_none_for_field(control_cls: type[Any], field_name: str) -> bool:
    """
    Resolve `None` allowance for a field from its annotation.
    """
    annotation = _get_effective_type_hints(control_cls).get(field_name)
    if annotation is None:
        return False
    return _annotation_allows_none(annotation)


def _prepare_field_value(
    control: Any,
    field_name: str,
    value: Any,
    message: Optional[FieldMessage],
    default_error: Callable[[Any], str],
) -> bool:
    """
    Normalize `None` handling for field-level validators.

    Returns:
        `True` when validation should be skipped because `None` is allowed.
    """

    none_allowed = _resolve_allow_none_for_field(control.__class__, field_name)
    if value is None and none_allowed:
        return True

    if value is None:
        if message is not None:
            raise ValueError(
                _resolve_field_message(message, control, field_name, value)
            )
        raise ValueError(default_error(value))

    return False


def _prepare_comparison_values(
    control: Any,
    left_field: str,
    right_field: str,
    message: Optional[ControlMessage],
    default_error: Callable[[Any, Any], str],
) -> tuple[Any, Any, bool]:
    """
    Load and normalize values for a cross-field comparison.

    Returns:
        `(left_value, right_value, skip_validation)`.
    """

    left_value = getattr(control, left_field)
    right_value = getattr(control, right_field)
    left_none_allowed = _resolve_allow_none_for_field(control.__class__, left_field)
    right_none_allowed = _resolve_allow_none_for_field(control.__class__, right_field)

    if left_value is None and left_none_allowed:
        return left_value, right_value, True
    if right_value is None and right_none_allowed:
        return left_value, right_value, True

    if left_value is None or right_value is None:
        if message is not None:
            raise ValueError(_resolve_control_message(message, control))
        raise ValueError(default_error(left_value, right_value))

    return left_value, right_value, False


@cache
def _compile_class_spec(control_cls: type[Any]) -> _ClassValidationSpec:
    """
    Compile and cache effective validation rules for a control class.

    Rules are merged in MRO order (base to derived) so subclasses can extend
    validation behavior deterministically.
    """

    field_rules: list[tuple[str, FieldRule]] = []
    control_rules: list[ControlRule] = []

    for cls in reversed(control_cls.__mro__):
        if cls is object:
            continue

        # Collect field-level rules from Annotated metadata.
        for field_name, hint in _get_declared_type_hints(cls).items():
            if get_origin(hint) is Annotated:
                for metadata in get_args(hint)[1:]:
                    if isinstance(metadata, FieldRule):
                        field_rules.append((field_name, metadata))

        # Collect class-level cross-field rules.
        rules = cls.__dict__.get("__outbound_rules__", ())
        if rules:
            for rule in rules:
                if isinstance(rule, ControlRule):
                    control_rules.append(rule)

    return _ClassValidationSpec(tuple(field_rules), tuple(control_rules))


def validate_outbound(control: Any) -> None:
    """
    Run all compiled outbound validators for a control instance.

    Field rules are evaluated first, then class-level control rules.
    Validation stops at the first raised exception.
    """

    spec = _compile_class_spec(control.__class__)
    for field_name, rule in spec.field_rules:
        rule.validate(control, field_name, getattr(control, field_name))
    for rule in spec.control_rules:
        rule.validate(control)
