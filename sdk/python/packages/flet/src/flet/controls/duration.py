from dataclasses import dataclass
from typing import Optional, Union

__all__ = ["Duration", "DurationValue", "OptionalDurationValue"]


@dataclass
class Duration:
    microseconds: int = 0
    milliseconds: int = 0
    seconds: int = 0
    minutes: int = 0
    hours: int = 0
    days: int = 0


DurationValue = Union[int, Duration]
OptionalDurationValue = Optional[DurationValue]
