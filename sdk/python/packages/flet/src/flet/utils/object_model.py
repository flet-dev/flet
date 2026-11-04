import copy
import dataclasses
import datetime
import inspect
import logging
import sys
import types
from enum import Enum
from typing import Annotated, Any, Union, get_args, get_origin, get_type_hints

from flet.utils.from_dict import from_dict

logger = logging.getLogger("flet")

_SCALAR_TYPES = (
    bool,
    datetime.date,
    datetime.datetime,
    datetime.time,
    datetime.timedelta,
    float,
    int,
    str,
    type(None),
)
"""Types whose fields can't hold a `dict` or a `list`."""


def patch_dataclass(obj: Any, patch: dict):
    """
    Applies a partial update to a dataclass instance in place.

    The function resolves field type hints and updates matching fields from `patch`,
    including support for nested dataclasses, lists, enum values, and plain values. A
    key that isn't a field of `obj` is ignored, and so is a value that can't be
    converted to its field's type or a `dict` or `list` for a scalar field.

    A nested value object is replaced with a patched copy, because one object is often
    shared by many controls and sessions. A nested control is patched in place, limited
    to its `client_writable` fields. Private keys are ignored in nested objects.

    For `@control` / `@value` objects (those with `_values` and
    `_prop_defaults`), Prop fields are written directly into `_values` rather
    than going through `Prop.__set__`.  This avoids unnecessary dirty-tracking,
    frozen-checks, and `_notify` calls — none of which are needed when applying
    patches that originate *from* Dart rather than from Python code.

    Args:
        obj: Dataclass instance to patch.
        patch: Mapping of field names to new values.
    """
    cls = obj.__class__

    try:
        frame = inspect.currentframe().f_back
        globalns = sys.modules[cls.__module__].__dict__
        localns = frame.f_globals.copy()
        localns.update(frame.f_locals)
        hints = get_type_hints(cls, globalns=globalns, localns=localns)
    except Exception:
        hints = {f.name: f.type for f in dataclasses.fields(cls)}  # fallback
        # print("ERROR: ", cls.__name__, e)

    # For @control / @value objects write Prop fields directly into _values,
    # bypassing dirty-tracking and other Prop.__set__ side-effects.
    _values = getattr(obj, "_values", None)
    _prop_defaults = getattr(type(obj), "_prop_defaults", None)

    def _write(field_name: str, value: Any) -> None:
        if (
            _values is not None
            and _prop_defaults is not None
            and field_name in _prop_defaults
        ):
            prop_default = _prop_defaults[field_name]
            if value == prop_default:
                _values.pop(field_name, None)  # keep _values sparse
            else:
                _values[field_name] = value
        else:
            object.__setattr__(obj, field_name, value)

    field_names = {f.name for f in dataclasses.fields(cls)}

    for field_name, value in patch.items():
        if field_name not in hints or field_name not in field_names:
            continue

        field_type = hints[field_name]
        current_value = getattr(obj, field_name, None)
        actual_type = resolve_actual_type(field_type)
        is_optional = actual_type is not field_type

        try:
            # Nested dataclass patching
            if dataclasses.is_dataclass(actual_type):
                if isinstance(value, dict):
                    nested_patch = _public_keys(value)
                    if _is_control(current_value):
                        patch_dataclass(
                            current_value,
                            {
                                name: nested_value
                                for name, nested_value in nested_patch.items()
                                if name in current_value._client_writable
                            },
                        )
                    elif current_value is not None:
                        patched_copy = _copy_value(current_value)
                        patch_dataclass(patched_copy, nested_patch)
                        _write(field_name, patched_copy)
                        # The client already has this value: nothing to diff.
                        prev_classes = getattr(obj, "__prev_classes", {})
                        if field_name in prev_classes:
                            prev_classes[field_name] = patched_copy
                    elif not _is_control(actual_type):
                        _write(
                            field_name,
                            from_dict(
                                actual_type, _typed_items(actual_type, nested_patch)
                            ),
                        )
                elif isinstance(value, actual_type) or (value is None and is_optional):
                    _write(field_name, value)

            # List of dataclasses or values
            elif get_origin(actual_type) is list:
                if isinstance(value, list):
                    item_type = get_args(actual_type)[0]
                    if _is_control(item_type):
                        continue
                    if dataclasses.is_dataclass(item_type):
                        _write(
                            field_name, [from_dict(item_type, item) for item in value]
                        )
                    elif _admits_container(item_type) or not any(
                        isinstance(item, (dict, list)) for item in value
                    ):
                        _write(field_name, value)
                elif value is None and is_optional:
                    _write(field_name, value)

            # Enum
            elif is_enum(actual_type):
                if value is not None:
                    _write(field_name, actual_type(value))
                elif is_optional:
                    _write(field_name, None)

            # Simple literal or other value
            elif _admits_container(field_type) or not isinstance(value, (dict, list)):
                _write(field_name, value)
        except (AttributeError, TypeError, ValueError):
            logger.debug(
                "Ignored invalid value of %s.%s",
                cls.__name__,
                field_name,
                exc_info=True,
            )


def _is_control(value: Any) -> bool:
    """Whether `value` is a control or a control class."""
    return hasattr(value, "_client_writable")


def _admits_container(tp: Any) -> bool:
    """
    Whether a field annotated with `tp` can hold a `dict` or a `list` as sent.

    An annotation that can't be resolved, such as a forward reference, gets the benefit
    of the doubt.

    Args:
        tp: The annotation of the field.

    Returns:
        `False` if every type `tp` allows is a scalar or a dataclass, as a `dict` isn't
            converted to a dataclass of a union. `True` otherwise.
    """
    origin = get_origin(tp)
    if origin is Annotated:
        return _admits_container(get_args(tp)[0])
    if origin in (Union, types.UnionType):
        return any(_admits_container(arg) for arg in get_args(tp))
    return not (
        tp in _SCALAR_TYPES
        or dataclasses.is_dataclass(tp)
        or (isinstance(tp, type) and issubclass(tp, Enum))
    )


def _typed_items(cls: type, patch: dict) -> dict:
    """
    Returns the items of `patch` that can be used to build an instance of a value class.

    Args:
        cls: The dataclass to build.
        patch: Mapping of field names to values.

    Returns:
        `patch` without a `dict` or `list` meant for a field holding a single value.
    """
    try:
        hints = get_type_hints(cls, globalns=sys.modules[cls.__module__].__dict__)
    except Exception:
        hints = {f.name: f.type for f in dataclasses.fields(cls)}
    return {
        name: value
        for name, value in patch.items()
        if not isinstance(value, (dict, list))
        or dataclasses.is_dataclass(resolve_actual_type(hints.get(name)))
        or _admits_container(hints.get(name))
    }


def _public_keys(patch: dict) -> dict:
    """Returns the items of `patch` whose keys are public field names."""
    return {
        key: value
        for key, value in patch.items()
        if isinstance(key, str) and not key.startswith("_")
    }


def _copy_value(value: Any) -> Any:
    """
    Returns a copy of a value object that can be changed without affecting `value`.

    The copy gets its own property storage and diff snapshots, and has no pending
    changes.

    Args:
        value: The `@value` or plain dataclass instance to copy.

    Returns:
        A shallow copy of `value`.
    """
    copied = copy.copy(value)
    state = vars(copied)
    if "_values" in state:
        state["_values"] = dict(state["_values"])
        state["_dirty"] = {}
    if "__changes" in state:
        state["__changes"] = {}
    for snapshot in ("__prev_lists", "__prev_dicts", "__prev_classes"):
        if snapshot in state:
            state[snapshot] = dict(state[snapshot])
    return copied


def resolve_actual_type(tp: Any) -> Any:
    """
    Resolves effective runtime type for common optional annotations.

    For `Optional[T]` (represented as `Union[T, None]`), this function returns `T`.
    Other annotations are returned unchanged.

    Args:
        tp: Type annotation to resolve.

    Returns:
        Resolved type annotation.
    """
    origin = get_origin(tp)
    args = get_args(tp)

    if origin is Union and len(args) == 2 and type(None) in args:
        # It's Optional[T]
        return args[0] if args[1] is type(None) else args[1]

    return tp


def is_enum(tp: Any) -> bool:
    """
    Indicates whether a value is an enum class.

    Args:
        tp: Value to check.

    Returns:
        `True` if `tp` is a subclass of `enum.Enum`, otherwise `False`.
    """
    return isinstance(tp, type) and issubclass(tp, Enum)


def get_param_count(fn):
    """
    Returns the number of declared parameters for a callable.

    Args:
        fn: Callable object to inspect.

    Returns:
        Parameter count, or `None` when a signature cannot be determined.
    """
    try:
        return len(inspect.signature(fn).parameters)
    except (ValueError, TypeError):
        return None
