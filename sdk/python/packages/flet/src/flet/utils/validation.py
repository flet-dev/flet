"""
Validation helpers for dataclass-style models, including Flet controls.

This module provides composable rule objects that are attached to annotated
fields (`typing.Annotated`) and to class-level cross-field declarations
(`__validation_rules__`).

Primary use cases:
1. Generic dataclass/domain model validation via direct `validate(instance)` calls.
2. Flet outbound validation, where `BaseControl` invokes `validate(self)`
   before patch serialization so the invalid state fails on Python side first.

The public entry points are:
- `V`, the rule-builder namespace used in `Annotated[...]` metadata and
  `__validation_rules__`.
- `validate()`, which evaluates the compiled field and class rules for one
  instance.
- `FieldRule` and `ClassRule`, lightweight wrappers used by the runtime and
  by advanced callers defining custom validation callbacks.
"""

import sys
from collections.abc import Iterable
from dataclasses import dataclass
from functools import cache
from typing import (
    Annotated,
    Any,
    Callable,
    ClassVar,
    Optional,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from flet.utils.deprecated import deprecated_warning

__all__ = [
    "ClassRule",
    "FieldRule",
    "V",
    "ValidationDeclarationError",
    "ValidationRules",
    "validate",
]

FieldCheck = Callable[[Any, str, Any], None]
"""Signature for a field-level validator callback."""

FieldMessage = Union[str, Callable[[Any, str, Any], str]]
"""Static text or callable used to format a field-level error message."""

ClassCheck = Callable[[Any], None]
"""Signature for a class-level validator callback."""

ClassMessage = Union[str, Callable[[Any], str]]
"""Static text or callable used to format a class-level error message."""

ClassPredicate = Callable[[Any], bool]
"""Boolean predicate used by [`V.ensure()`][(m).V.ensure]."""


class ValidationDeclarationError(RuntimeError):
    """
    Raised when a validation rule declaration is invalid.

    This exception is for authoring mistakes in the validation declaration
    itself, such as invalid builder arguments or malformed rule composition.
    Runtime validation failures for instance values raise `ValueError`
    instead.
    """


@dataclass(frozen=True)
class FieldRule:
    """
    A single validation rule applied to one annotated field value.

    Instances of this dataclass are usually created via `V.*` helpers and
    stored in `Annotated[...]` metadata.
    """

    _check: FieldCheck

    def validate(self, instance: Any, field_name: str, value: Any) -> None:
        """
        Validate one field value for a specific instance.

        Args:
            instance: Model or control instance currently being validated.
            field_name: Name of the field associated with this rule.
            value: Current runtime value read from `instance.<field_name>`.

        Raises:
            ValueError: If the wrapped field check rejects `value`.
        """
        self._check(instance, field_name, value)


@dataclass(frozen=True)
class ClassRule:
    """
    A cross-field validation rule evaluated against one class instance.

    Instances of this dataclass are usually created via `V.ensure()` or
    declared directly in `__validation_rules__`.
    """

    _check: ClassCheck

    def validate(self, instance: Any) -> None:
        """
        Validate one instance against a class-level rule.

        Args:
            instance: Model or control instance currently being validated.

        Raises:
            ValueError: If the wrapped class check rejects `instance`.
        """
        self._check(instance)


ValidationRules = ClassVar[tuple[ClassRule, ...]]
"""Alias for class-level `__validation_rules__` tuples."""


@dataclass(frozen=True)
class _ClassValidationSpec:
    """
    Compiled validation specification for one class.

    Attributes:
        field_rules: Ordered `(field_name, rule)` pairs extracted from
            `Annotated[...]` metadata across the class MRO.
        class_rules: Ordered class-level rules extracted from
            `__validation_rules__` across the class MRO.
    """

    field_rules: tuple[tuple[str, FieldRule], ...]
    class_rules: tuple[ClassRule, ...]


_DEPRECATED_WARNINGS_KEY = "__deprecated_validation_warnings"
_REPORTED_VALIDATION_ERRORS_KEY = "__reported_validation_errors"


def _get_warned_deprecated_fields(instance: Any) -> Optional[set[str]]:
    """
    Return a mutable set of already-emitted deprecation warning keys.

    Warnings are tracked on a private runtime attribute so they do not leak into
    serialized control data.

    Args:
        instance: Model or control instance used to store the warning cache.

    Returns:
        A mutable set attached to `instance`, or `None` when the instance does
        not allow attaching the private cache attribute.
    """

    warned = getattr(instance, _DEPRECATED_WARNINGS_KEY, None)
    if warned is not None:
        return warned

    warned = set()
    try:
        setattr(instance, _DEPRECATED_WARNINGS_KEY, warned)
    except Exception:
        return None
    return warned


def _get_reported_validation_errors(
    instance: Any,
) -> Optional[set[tuple[str, str]]]:
    """
    Return a mutable set of already-reported validation error signatures.

    Signatures are stored on the instance to suppress repeated identical
    `ValueError` failures during control auto-update cycles.

    Args:
        instance: Model or control instance used to store the error cache.

    Returns:
        A mutable set of `(exception_type_name, message)` tuples, or `None`
        when the instance does not allow attaching the private cache attribute.
    """

    reported = getattr(instance, _REPORTED_VALIDATION_ERRORS_KEY, None)
    if reported is not None:
        return reported

    reported = set()
    try:
        setattr(instance, _REPORTED_VALIDATION_ERRORS_KEY, reported)
    except Exception:
        return None
    return reported


def _resolve_field_message(
    message: FieldMessage, instance: Any, field_name: str, value: Any
) -> str:
    """
    Render a field-level message that may be static text or a callable.

    Args:
        message: Static message text or formatter callable.
        instance: Model or control instance being validated.
        field_name: Field name associated with the error.
        value: Runtime field value being validated.

    Returns:
        The resolved error message string.
    """
    if callable(message):
        return message(instance, field_name, value)
    return message


def _resolve_class_message(message: ClassMessage, instance: Any) -> str:
    """
    Render a class-level message that may be static text or a callable.

    Args:
        message: Static message text or formatter callable.
        instance: Model or control instance being validated.

    Returns:
        The resolved error message string.
    """
    if callable(message):
        return message(instance)
    return message


def _format_expected_type(
    expected_type: Union[type[Any], tuple[type[Any], ...]],
) -> str:
    """
    Format expected type names into a readable sentence fragment.

    Args:
        expected_type: Single type or tuple of allowed runtime types.

    Returns:
        A human-readable type list such as `int` or `int, str, or float`.
    """
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


def _format_allowed_values(values: tuple[Any, ...]) -> str:
    """
    Format allowed values into a readable sentence fragment.

    Args:
        values: Allowed values already materialized as a tuple.

    Returns:
        A human-readable value list such as `'a'`, `'a' or 'b'`, or
        `'a', 'b', or 'c'`.
    """
    value_names = [repr(value) for value in values]
    if len(value_names) == 1:
        return value_names[0]
    if len(value_names) == 2:
        return f"{value_names[0]} or {value_names[1]}"
    return f"{', '.join(value_names[:-1])}, or {value_names[-1]}"


class V:
    """
    Validation rule builder namespace.

    Methods return `FieldRule` or `ClassRule` instances which are attached to
    class fields (`Annotated[...]`) or class-level `__validation_rules__`.

    Most field-level helpers automatically allow `None` when the field
    annotation is optional, and otherwise raise `ValueError` when a runtime
    value violates the declared rule.
    """

    @staticmethod
    def field(check: FieldCheck) -> FieldRule:
        """
        Wrap a custom field validator callback into a `FieldRule`.

        Args:
            check: Callback receiving `(instance, field_name, value)`. It should
                raise `ValueError` when the field is invalid.

        Returns:
            A field rule that delegates validation to `check`.
        """
        return FieldRule(check)

    @staticmethod
    def deprecated(
        replacement: Optional[str] = None,
        *,
        reason: Optional[str] = None,
        docs_reason: Optional[str] = None,
        version: str,
        delete_version: Optional[str] = None,
    ) -> FieldRule:
        """
        Emit a one-time deprecation warning when a field value is set.

        This rule is intended for soft-deprecating dataclass/control properties
        without changing value flow. It does not mutate field values.

        The warning is emitted once per instance and only when the field value
        is not `None`.

        Args:
            replacement: Preferred property name used in default message.
            reason: Full deprecation reason. When omitted, a
                replacement-based message is generated.
            docs_reason: Docs-only reason. This value is ignored at
                runtime and is consumed by docs tooling when available.
            version: Version where deprecation starts.
            delete_version: Version where removal is planned.

        Returns:
            A field rule that emits a deprecation warning at validation time.
        """

        default_reason = (
            f"Use `{replacement}` instead."
            if replacement is not None
            else "This property is deprecated."
        )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if value is None:
                return

            warning_key = f"{instance.__class__.__name__}.{field_name}"
            warned = _get_warned_deprecated_fields(instance)
            if warned is not None and warning_key in warned:
                return

            deprecated_warning(
                name=warning_key,
                reason=reason or default_reason,
                version=version,
                delete_version=delete_version,
                type="property",
            )
            if warned is not None:
                warned.add(warning_key)

        return FieldRule(_check)

    @staticmethod
    def ensure(
        predicate: ClassPredicate,
        *,
        message: Optional[ClassMessage] = None,
    ) -> ClassRule:
        """
        Build a generic cross-field predicate rule.

        When `message` is omitted, a generic fallback is used.

        Args:
            predicate: Boolean predicate receiving the instance. It should
                return `True` when the instance is valid.
            message: Optional static text or formatter used when the predicate
                returns `False`.

        Returns:
            A class rule that evaluates `predicate` against the instance.
        """

        def _check(instance: Any) -> None:
            if not predicate(instance):
                if message is not None:
                    raise ValueError(_resolve_class_message(message, instance))
                predicate_name = getattr(predicate, "__name__", None)
                if predicate_name and predicate_name != "<lambda>":
                    raise ValueError(f"Validation failed: {predicate_name}")
                raise ValueError("Validation failed.")

        return ClassRule(_check)

    @staticmethod
    def instance_of(
        expected_type: Union[type[Any], tuple[type[Any], ...]],
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate a field value type with an optional custom error message.

        Property docstring Raises wording:
        `If it is not of type ...`.

        Args:
            expected_type: Allowed runtime type(s).
            message: Custom error message/template.

        Returns:
            A field rule that checks `isinstance(value, expected_type)`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if value is None and _resolve_allow_none_for_field(
                instance.__class__, field_name
            ):
                return
            if not isinstance(value, expected_type):
                if message is None:
                    raise ValueError(
                        f"{field_name} must be of type "
                        f"{_format_expected_type(expected_type)}, got {type(value)}"
                    )
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )

        return FieldRule(_check)

    @staticmethod
    def visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is visible, i.e. `Control.visible` is `True`.

        Property docstring Raises wording: `If it is not visible.`

        Args:
            message: Custom error text or formatter.

        Returns:
            A field rule that accepts only visible controls.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: f"{field_name} must be visible",
            ):
                return
            if getattr(value, "visible", False):
                return
            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )
            raise ValueError(f"{field_name} must be visible")

        return FieldRule(_check)

    @staticmethod
    def visible_controls(
        *,
        min_count: int,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field contains at least `min_count` visible controls.

        Property docstring Raises wording:
        - `If it does not contain at least one visible Control.`
        - `If it does not contain at least n visible Controls.`

        The field value is expected to be an iterable of controls exposing a
        `visible` boolean attribute.

        Args:
            min_count: Minimum number of visible controls required.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `min_count` is not greater than or
                equal to `1`.

        Returns:
            A field rule that counts visible items in the iterable value.
        """
        if min_count < 1:
            raise ValidationDeclarationError(
                f"min_count must be greater than or equal to 1, got {min_count}"
            )

        def _default_error(field_name: str, visible_count: int) -> str:
            if min_count == 1:
                return (
                    f"{field_name} must contain at least one visible Control, "
                    f"got {visible_count}"
                )
            return (
                f"{field_name} must contain at least {min_count} visible Controls, "
                f"got {visible_count}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: _default_error(field_name, 0),
            ):
                return

            try:
                visible_count = sum(
                    1 for item in value if getattr(item, "visible", False)
                )
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(_default_error(field_name, 0)) from err

            if visible_count < min_count:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(_default_error(field_name, visible_count))

        return FieldRule(_check)

    @staticmethod
    def str_or_visible_control(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is either a string or a visible instance.

        Property docstring Raises wording:
        `If it is neither a string nor a visible Control.`

        Args:
            message: Custom error text or formatter.

        Returns:
            A field rule that accepts either strings or visible controls.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                    _resolve_field_message(message, instance, field_name, value)
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

        Property docstring Raises wording:
        `If it is not strictly greater than ...`.

        Args:
            bound: Exclusive lower bound.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces a strict lower bound.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                        _resolve_field_message(message, instance, field_name, value)
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

        Property docstring Raises wording:
        `If it is not greater than or equal to ...`.

        Args:
            bound: Inclusive lower bound.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces an inclusive lower bound.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                        _resolve_field_message(message, instance, field_name, value)
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

        Property docstring Raises wording:
        `If it is not strictly less than ...`.

        Args:
            bound: Exclusive upper bound.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces a strict upper bound.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                        _resolve_field_message(message, instance, field_name, value)
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

        Property docstring Raises wording:
        `If it is not less than or equal to ...`.

        Args:
            bound: Inclusive upper bound.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces an inclusive upper bound.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                        _resolve_field_message(message, instance, field_name, value)
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

        Property docstring Raises wording:
        `If it is not between ... and ..., inclusive.`

        Args:
            minimum: Inclusive lower bound.
            maximum: Inclusive upper bound.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces both inclusive bounds.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
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
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be between {minimum} and {maximum} inclusive, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def factor_of(
        base: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is an integer factor of `base`.

        Property docstring Raises wording:
        `If it is not a factor of ...`.

        This rule is sign-neutral. To enforce direction, compose with:
        - `V.gt(0)` for positive factors, or
        - `V.lt(0)` for negative factors.

        Args:
            base: The integer that validated values must evenly divide.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `base` is zero or not an integer.

        Returns:
            A field rule that accepts only integer factors of `base`.
        """
        if not isinstance(base, int) or isinstance(base, bool) or base == 0:
            raise ValidationDeclarationError(
                f"base must be a non-zero integer, got {base!r}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be a factor of {base}, got {current_value}"
                ),
            ):
                return
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value == 0
                or base % value != 0
            ):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be a factor of {base}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def multiple_of(
        divisor: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a field value is an integer multiple of `divisor`.

        Property docstring Raises wording:
        `If it is not a multiple of ...`.

        This rule is sign-neutral. To enforce direction, compose with:
        - `V.gt(0)` for positive multiples, or
        - `V.lt(0)` for negative multiples.

        Args:
            divisor: Divisor used for the divisibility check.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `divisor` is zero or not an integer.

        Returns:
            A field rule that accepts only integer multiples of `divisor`.
        """
        if not isinstance(divisor, int) or isinstance(divisor, bool) or divisor == 0:
            raise ValidationDeclarationError(
                f"divisor must be a non-zero integer, got {divisor!r}"
            )
        normalized_divisor = abs(divisor)

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be a multiple of {normalized_divisor}, "
                    f"got {current_value}"
                ),
            ):
                return
            if (
                not isinstance(value, int)
                or isinstance(value, bool)
                or value % normalized_divisor != 0
            ):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be a multiple of {normalized_divisor}, "
                    f"got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def eq(
        expected: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value == expected`.

        Property docstring Raises wording:
        `If it is not equal to ...`.

        Args:
            expected: Required value.
            message: Custom error text or formatter.

        Returns:
            A field rule that enforces equality with `expected`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be equal to {expected}, got {current_value}"
                ),
            ):
                return
            if value != expected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be equal to {expected}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def ne(
        unexpected: Any,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `value != unexpected`.

        Property docstring Raises wording:
        `If it is equal to ...`.

        Args:
            unexpected: Disallowed value.
            message: Custom error text or formatter.

        Returns:
            A field rule that rejects equality with `unexpected`.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must not be equal to {unexpected}, "
                    f"got {current_value}"
                ),
            ):
                return
            if value == unexpected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must not be equal to {unexpected}, got {value}"
                )

        return FieldRule(_check)

    @staticmethod
    def one_of(
        allowed_values: Iterable[Any],
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that `value` belongs to a fixed set of allowed values.

        Property docstring Raises wording:
        `If it is not one of ...`.

        Args:
            allowed_values: Allowed values collection. The iterable is consumed
                once and stored as a tuple.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `allowed_values` is empty.

        Returns:
            A field rule that accepts only values present in `allowed_values`.
        """
        allowed_values_tuple = tuple(allowed_values)
        if len(allowed_values_tuple) == 0:
            raise ValidationDeclarationError(
                "allowed_values must contain at least one value"
            )

        allowed_values_text = _format_allowed_values(allowed_values_tuple)

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda current_value: (
                    f"{field_name} must be one of {allowed_values_text}, "
                    f"got {current_value!r}"
                ),
            ):
                return
            if value not in allowed_values_tuple:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must be one of {allowed_values_text}, got {value!r}"
                )

        return FieldRule(_check)

    @staticmethod
    def or_(
        *rules: FieldRule,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that at least one field rule passes.

        Args:
            rules: Field rules evaluated in declaration order.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If no rules are provided.
            ValidationDeclarationError: If any provided object is not a `FieldRule`.

        Returns:
            A field rule that succeeds when any one of `rules` succeeds.
        """
        if len(rules) == 0:
            raise ValidationDeclarationError("or_ requires at least one field rule")
        for rule in rules:
            if not isinstance(rule, FieldRule):
                raise ValidationDeclarationError("or_ expects only FieldRule instances")

        def _check(instance: Any, field_name: str, value: Any) -> None:
            # Fast path: try each rule without catching exceptions first.
            # Only fall back to exception collection when all rules fail.
            errors: Optional[list[str]] = None
            for rule in rules:
                try:
                    rule.validate(instance, field_name, value)
                    return  # first passing rule is enough
                except ValueError as err:
                    if errors is None:
                        errors = []
                    errors.append(str(err))

            if message is not None:
                raise ValueError(
                    _resolve_field_message(message, instance, field_name, value)
                )

            if errors is not None and len(errors) == 1:
                raise ValueError(errors[0])

            joined_errors = "; or ".join(errors or ())
            raise ValueError(
                f"{field_name} must satisfy at least one of the allowed "
                f"conditions: {joined_errors}"
            )

        return FieldRule(_check)

    @staticmethod
    def non_empty(
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field value is non-empty (`len(value) > 0`).

        Property docstring Raises wording:
        `If it is empty.`

        Args:
            message: Custom error text or formatter.

        Returns:
            A field rule that requires a sized, non-empty value.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must be a non-empty sized value, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a non-empty sized value, got {type(value)}"
                ) from err

            if length == 0:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(f"{field_name} must be non-empty")

        return FieldRule(_check)

    @staticmethod
    def length_ge(
        minimum: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field has length greater than or equal to `minimum`.

        Property docstring Raises wording:
        `If its length is less than ...`.

        Args:
            minimum: Inclusive minimum allowed length.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `minimum` is negative.

        Returns:
            A field rule that enforces a minimum length.
        """
        if minimum < 0:
            raise ValidationDeclarationError(
                f"minimum must be greater than or equal to 0, got {minimum}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length greater than or equal to "
                    f"{minimum}, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length greater than "
                    f"or equal to {minimum}, got {type(value)}"
                ) from err

            if length < minimum:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length greater than or equal to "
                    f"{minimum}, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def length_eq(
        expected: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field has length equal to `expected`.

        Property docstring Raises wording:
        `If its length is not equal to ...`.

        Args:
            expected: Required length.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `expected` is negative.

        Returns:
            A field rule that enforces an exact length.
        """
        if expected < 0:
            raise ValidationDeclarationError(
                f"expected must be greater than or equal to 0, got {expected}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length equal to {expected}, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length equal to "
                    f"{expected}, got {type(value)}"
                ) from err

            if length != expected:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length equal to {expected}, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def length_between(
        minimum: int,
        maximum: int,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate that a sized field length is between bounds, inclusive.

        Property docstring Raises wording:
        `If its length is not between ... and ..., inclusive.`

        Args:
            minimum: Inclusive minimum allowed length.
            maximum: Inclusive maximum allowed length.
            message: Custom error text or formatter.

        Raises:
            ValidationDeclarationError: If `minimum` is negative.
            ValidationDeclarationError: If `maximum` is less than `minimum`.

        Returns:
            A field rule that enforces an inclusive length range.
        """
        if minimum < 0:
            raise ValidationDeclarationError(
                f"minimum must be greater than or equal to 0, got {minimum}"
            )
        if maximum < minimum:
            raise ValidationDeclarationError(
                f"maximum must be greater than or equal to minimum ({minimum}), "
                f"got {maximum}"
            )

        def _check(instance: Any, field_name: str, value: Any) -> None:
            if _prepare_field_value(
                instance=instance,
                field_name=field_name,
                value=value,
                message=message,
                default_error=lambda _current_value: (
                    f"{field_name} must have length between {minimum} and {maximum} "
                    f"inclusive, got None"
                ),
            ):
                return

            try:
                length = len(value)
            except TypeError as err:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    ) from err
                raise ValueError(
                    f"{field_name} must be a sized value with length between "
                    f"{minimum} and {maximum} inclusive, got {type(value)}"
                ) from err

            if not (minimum <= length <= maximum):
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} must have length between {minimum} and {maximum} "
                    f"inclusive, got {length}"
                )

        return FieldRule(_check)

    @staticmethod
    def gt_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name > other_field` on an instance.

        Property docstring Raises wording:
        `If it is not strictly greater than [`other_field`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field in the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Custom error text or formatter.

        Returns:
            A field rule that compares one field against another field value on
            the same instance.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be strictly greater than "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value <= other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be strictly greater than "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def ge_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name >= other_field` on an instance.

        Property docstring Raises wording:
        `If it is not greater than or equal to [`other_field`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field in the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Custom error text or formatter.

        Returns:
            A field rule that compares one field against another field value on
            the same instance.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be greater than or equal to "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value < other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be greater than or equal to "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def lt_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name < other_field` on an instance.

        Property docstring Raises wording:
        `If it is not strictly less than [`other_field`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field in the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Custom error text or formatter.

        Returns:
            A field rule that compares one field against another field value on
            the same instance.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be strictly less than "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value >= other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be strictly less than "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)

    @staticmethod
    def le_field(
        other_field: str,
        *,
        message: Optional[FieldMessage] = None,
    ) -> FieldRule:
        """
        Validate `field_name <= other_field` on an instance.

        Property docstring Raises wording:
        `If it is not less than or equal to [`other_field`][(c).].`

        This rule is attached to one field via `Annotated[...]` and compares that
        field value against another field in the same instance.

        Args:
            other_field: Name of the field on the right side of the comparison.
            message: Custom error text or formatter.

        Returns:
            A field rule that compares one field against another field value on
            the same instance.
        """

        def _check(instance: Any, field_name: str, value: Any) -> None:
            other_value, skip = _prepare_field_comparison_values(
                instance=instance,
                field_name=field_name,
                value=value,
                other_field=other_field,
                message=message,
                default_error=lambda left, right: (
                    f"{field_name} ({left}) must be less than or equal to "
                    f"{other_field} ({right})"
                ),
            )
            if skip:
                return
            if value > other_value:
                if message is not None:
                    raise ValueError(
                        _resolve_field_message(message, instance, field_name, value)
                    )
                raise ValueError(
                    f"{field_name} ({value}) must be less than or equal to "
                    f"{other_field} ({other_value})"
                )

        return FieldRule(_check)


def _get_declared_type_hints(cls: type[Any]) -> dict[str, Any]:
    """
    Resolve declared annotations for one class with best-effort extras support.

    Only annotations declared directly on `cls` are returned. This allows MRO-based
    merging in `_compile_class_spec()` without duplicating inherited members.

    Args:
        cls: Class whose locally declared annotations should be resolved.

    Returns:
        A mapping of field names to resolved type hints for annotations declared
        directly on `cls`.
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

    The result is used for Optional/None inference in field-level rules.

    Args:
        cls: Class whose effective annotations should be resolved.

    Returns:
        A mapping of field names to resolved type hints after MRO merging.
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

    Args:
        annotation: Annotation that may contain one or more `Annotated` layers.

    Returns:
        The unwrapped base annotation.
    """

    while get_origin(annotation) is Annotated:
        annotation = get_args(annotation)[0]
    return annotation


def _annotation_allows_none(annotation: Any) -> bool:
    """
    Return `True` if annotation contains `None` (for example `Optional[T]`).

    Args:
        annotation: Annotation to inspect.

    Returns:
        `True` when the normalized annotation is a `Union[...]` containing
        `NoneType`.
    """

    annotation = _strip_annotated(annotation)
    origin = get_origin(annotation)
    if origin is Union:
        return any(arg is type(None) for arg in get_args(annotation))
    return False


@cache
def _resolve_allow_none_for_field(model_cls: type[Any], field_name: str) -> bool:
    """
    Resolve `None` allowance for an annotated field on a class.

    Args:
        model_cls: Class declaring the field.
        field_name: Field name whose effective annotation should be inspected.

    Returns:
        `True` when the effective field annotation allows `None`.
    """
    annotation = _get_effective_type_hints(model_cls).get(field_name)
    if annotation is None:
        return False
    return _annotation_allows_none(annotation)


def _prepare_field_value(
    instance: Any,
    field_name: str,
    value: Any,
    message: Optional[FieldMessage],
    default_error: Callable[[Any], str],
) -> bool:
    """
    Normalize `None` handling for field-level validators.

    Args:
        instance: Model or control instance being validated.
        field_name: Name of the field currently being validated.
        value: Current runtime field value.
        message: Optional custom error message or formatter.
        default_error: Fallback formatter used when `value` is invalid and no
            custom message is provided.

    Returns:
        `True` when validation should be skipped because `None` is allowed.

    Raises:
        ValueError: If `value` is `None`, the field is not optional, and the
            rule should fail immediately.
    """

    if value is not None:
        return False

    if _resolve_allow_none_for_field(instance.__class__, field_name):
        return True

    if message is not None:
        raise ValueError(_resolve_field_message(message, instance, field_name, value))
    raise ValueError(default_error(value))


def _prepare_field_comparison_values(
    instance: Any,
    field_name: str,
    value: Any,
    other_field: str,
    message: Optional[FieldMessage],
    default_error: Callable[[Any, Any], str],
) -> tuple[Any, bool]:
    """
    Load and normalize values for a field-vs-field comparison rule.

    Args:
        instance: Model or control instance being validated.
        field_name: Name of the left-hand field.
        value: Current runtime value of the left-hand field.
        other_field: Name of the right-hand field.
        message: Optional custom error message or formatter.
        default_error: Fallback formatter used when either side is invalid and
            no custom message is provided.

    Returns:
        A tuple of `(other_value, skip_validation)`. Validation is skipped when
        either side is `None` and that side is optional.

    Raises:
        ValueError: If comparison cannot proceed because a required side is `None`.
    """

    other_value = getattr(instance, other_field)

    if value is not None and other_value is not None:
        return other_value, False

    cls = instance.__class__
    if value is None and _resolve_allow_none_for_field(cls, field_name):
        return other_value, True
    if other_value is None and _resolve_allow_none_for_field(cls, other_field):
        return other_value, True

    if message is not None:
        raise ValueError(_resolve_field_message(message, instance, field_name, value))
    raise ValueError(default_error(value, other_value))


@cache
def _compile_class_spec(model_cls: type[Any]) -> _ClassValidationSpec:
    """
    Compile and cache effective validation rules for one class.

    Rules are merged in MRO order (base to derived) so subclasses can extend
    validation behavior deterministically.

    Args:
        model_cls: Class whose field and class validation rules should be
            compiled.

    Returns:
        The cached validation specification for `model_cls`.
    """

    field_rules: list[tuple[str, FieldRule]] = []
    class_rules: list[ClassRule] = []

    for cls in reversed(model_cls.__mro__):
        if cls is object:
            continue

        # Collect field-level rules from Annotated metadata.
        for field_name, hint in _get_declared_type_hints(cls).items():
            if get_origin(hint) is Annotated:
                for metadata in get_args(hint)[1:]:
                    if isinstance(metadata, FieldRule):
                        field_rules.append((field_name, metadata))

        # Collect class-level cross-field rules.
        rules = cls.__dict__.get("__validation_rules__", ())
        if rules:
            for rule in rules:
                if isinstance(rule, ClassRule):
                    class_rules.append(rule)

    return _ClassValidationSpec(tuple(field_rules), tuple(class_rules))


def validate(instance: Any, *, suppress_repeated_errors: bool = False) -> None:
    """
    Run all compiled validators for one instance.

    Field rules are evaluated first, then class-level rules.
    Validation stops at the first raised exception.

    Args:
        instance: Instance to validate.
        suppress_repeated_errors: When `True`, repeated identical `ValueError`
            messages for the same instance are suppressed after the first report.

    Raises:
        ValueError: If any field or class rule fails and the failure is not
            suppressed as a repeated identical error for the same instance.
    """

    spec = _compile_class_spec(instance.__class__)
    reported = (
        _get_reported_validation_errors(instance) if suppress_repeated_errors else None
    )

    try:
        for field_name, rule in spec.field_rules:
            rule.validate(instance, field_name, getattr(instance, field_name))
        for rule in spec.class_rules:
            rule.validate(instance)
    except ValueError as ex:
        if reported is None:
            raise

        # Dedup key is `(exception type, message)` so distinct failures for the
        # same control instance are still surfaced once.
        signature = (ex.__class__.__name__, str(ex))
        if signature in reported:
            return
        reported.add(signature)
        raise
    else:
        if reported:
            # Reset once the control validates successfully again.
            reported.clear()
