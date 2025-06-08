import dataclasses
import inspect
import sys
from enum import Enum
from typing import Any, Union, get_args, get_origin, get_type_hints

from flet.utils.from_dict import from_dict


def patch_dataclass(obj: Any, patch: dict):
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
                    object.__setattr__(obj, field_name, from_dict(actual_type, value))
                else:
                    patch_dataclass(current_value, value)

            # List of dataclasses or values
            elif get_origin(actual_type) is list and isinstance(value, list):
                item_type = get_args(actual_type)[0]
                if dataclasses.is_dataclass(item_type):
                    object.__setattr__(
                        obj, field_name, [from_dict(item_type, item) for item in value]
                    )
                else:
                    object.__setattr__(obj, field_name, value)

            # Enum
            elif is_enum(actual_type):
                enum_value = actual_type(value)
                object.__setattr__(obj, field_name, enum_value)

            # Simple literal or other value
            else:
                object.__setattr__(obj, field_name, value)
        elif field_name.startswith("_"):
            setattr(obj, field_name, value)


def resolve_actual_type(tp: Any) -> Any:
    origin = get_origin(tp)
    args = get_args(tp)

    if origin is Union and len(args) == 2 and type(None) in args:
        # It's Optional[T]
        return args[0] if args[1] is type(None) else args[1]

    return tp


def is_enum(tp: Any) -> bool:
    return isinstance(tp, type) and issubclass(tp, Enum)


def get_param_count(fn):
    try:
        return len(inspect.signature(fn).parameters)
    except (ValueError, TypeError):
        return None
