from dataclasses import dataclass
from typing import Any, Optional, get_args, get_type_hints


@dataclass
class Event:
    target: int
    name: str
    data: Optional[str]


def get_event_field_type(control: Any, field_name: str):
    hints = get_type_hints(control)
    callable_type = get_args(hints[field_name])[0]  # Get `Callable[[EventType], None]`
    return get_args(callable_type)[0][0]  # Get `EventType`
