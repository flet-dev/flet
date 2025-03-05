import dataclasses
from typing import Any, Dict, List, Type, TypeVar, Union, get_args, get_origin

T = TypeVar("T")


def from_dict(cls: Type[T], data: Any) -> T:
    """Recursively converts a dictionary into a dataclass instance, handling nested lists and dictionaries."""
    if dataclasses.is_dataclass(cls):
        # Initialize a dataclass instance with proper field types
        field_values = {}
        for field in dataclasses.fields(cls):
            field_name = field.name
            field_type = field.type

            if field_name in data:
                value = data[field_name]
                field_values[field_name] = convert_value(field_type, value)

        return cls(**field_values)

    else:
        return convert_value(cls, data)


def convert_value(field_type: Type, value: Any) -> Any:
    """Handles conversion for nested dataclasses, lists, dictionaries, and basic types."""
    origin = get_origin(field_type)

    if dataclasses.is_dataclass(field_type):
        return from_dict(field_type, value)  # Recursively convert dataclass

    elif origin is list:
        item_type = get_args(field_type)[0]  # Extract list element type
        return [convert_value(item_type, item) for item in value]

    elif origin is dict:
        key_type, val_type = get_args(field_type)  # Extract key-value types
        return {
            convert_value(key_type, k): convert_value(val_type, v)
            for k, v in value.items()
        }

    else:
        return value  # Return value as-is (handles int, float, str, bool, etc.)
