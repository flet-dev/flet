import dataclasses
import sys
from enum import Enum
from typing import (
    Any,
    ForwardRef,
    TypeVar,
    Union,
    get_args,
    get_origin,
    get_type_hints,
)

from flet.utils.typing_utils import eval_type

T = TypeVar("T")


def from_dict(cls: type[T], data: Any) -> T:
    # Handle generic types and ForwardRefs
    origin = get_origin(cls) or cls
    args = get_args(cls)

    # If cls is a generic like Event[T], resolve T
    if args:
        cls = origin  # drop the generic info; dataclasses only apply to the base class

    # If cls is a ForwardRef, resolve it
    if isinstance(cls, ForwardRef):
        globalns = sys.modules[cls.__module__].__dict__
        cls = eval_type(cls, globalns, None)

    if dataclasses.is_dataclass(cls):
        try:
            type_hints = get_type_hints(
                cls, globalns=sys.modules[cls.__module__].__dict__
            )
        except Exception:
            type_hints = {f.name: f.type for f in dataclasses.fields(cls)}  # fallback

        init_values = {}
        post_values = {}

        for field in dataclasses.fields(cls):
            field_name = field.name
            field_type = type_hints.get(field_name, field.type)
            data_field_name = field.metadata.get("data_field", field_name)

            if data_field_name in data:
                value = data[data_field_name]
                converted = convert_value(field_type, value)
                init_values[field_name] = converted

                # set _prev_* values
                post_values[f"_prev_{field_name}"] = converted

        # First create the object using init-only fields
        instance = cls(**init_values)

        # Now set the _prev_* fields via setattr (won’t raise errors
        # if they're not declared)
        for k, v in post_values.items():
            setattr(instance, k, v)

        return instance

    else:
        return convert_value(cls, data)


def convert_value(field_type: type, value: Any) -> Any:
    """
    Converts a value to its appropriate type based on the field_type.
    Handles nested dataclasses, enums, lists, dicts, and optionals.

    Args:
        field_type: The type to convert the value to.
        value: The value to convert.

    Returns:
        The converted value.
    """
    origin = get_origin(field_type)
    args = get_args(field_type)

    # Optional[T]
    if origin is Union and type(None) in args:
        inner_type = [arg for arg in args if arg is not type(None)][0]
        if value is None:
            return None
        return convert_value(inner_type, value)

    # Enum
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(value)

    # Dataclass
    if dataclasses.is_dataclass(field_type) and isinstance(value, dict):
        return from_dict(field_type, value)

    # List[T]
    if origin is list and isinstance(value, list):
        item_type = args[0]
        return [convert_value(item_type, item) for item in value]

    # Dict[K, V]
    if origin is dict and isinstance(value, dict):
        key_type, val_type = args
        return {
            convert_value(key_type, k): convert_value(val_type, v)
            for k, v in value.items()
        }

    return value  # literal


def is_literal(value: Any) -> bool:
    """
    Checks if a value is a basic literal (int, float, str, bool, or None).

    Args:
        value: The value to check.

    Returns:
        True if the value is a literal type; False otherwise.
    """
    return isinstance(value, (int, float, str, bool, type(None)))
