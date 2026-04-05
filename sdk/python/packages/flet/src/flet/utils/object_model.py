import dataclasses
import inspect
import sys
from enum import Enum
from typing import Any, Union, get_args, get_origin, get_type_hints

from flet.utils.from_dict import from_dict


def patch_dataclass(obj: Any, patch: dict):
    """
    Applies a partial update to a dataclass instance in place.

    The function resolves field type hints and updates matching fields from `patch`,
    including support for nested dataclasses, lists, enum values, and plain values.
    Fields starting with `_` are set directly even when they are not declared in type
    hints.

    For ``@control`` / ``@value`` objects (those with ``_values`` and
    ``_prop_defaults``), Prop fields are written directly into ``_values`` rather
    than going through ``Prop.__set__``.  This avoids unnecessary dirty-tracking,
    frozen-checks, and ``_notify`` calls — none of which are needed when applying
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

    for field_name, value in patch.items():
        if field_name in hints:
            field_type = hints[field_name]
            current_value = getattr(obj, field_name, None)
            actual_type = resolve_actual_type(field_type)

            if isinstance(actual_type, str):
                continue  # unresolved forward ref

            # Nested dataclass patching
            if dataclasses.is_dataclass(actual_type) and isinstance(value, dict):
                if current_value is None:
                    _write(field_name, from_dict(actual_type, value))
                else:
                    patch_dataclass(current_value, value)

            # List of dataclasses or values
            elif get_origin(actual_type) is list and isinstance(value, list):
                item_type = get_args(actual_type)[0]
                if dataclasses.is_dataclass(item_type):
                    _write(field_name, [from_dict(item_type, item) for item in value])
                else:
                    _write(field_name, value)

            # Enum
            elif is_enum(actual_type):
                _write(field_name, actual_type(value))

            # Simple literal or other value
            else:
                _write(field_name, value)
        elif field_name.startswith("_"):
            setattr(obj, field_name, value)


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
