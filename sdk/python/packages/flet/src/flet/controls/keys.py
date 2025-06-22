from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass()
class Key:
    value: Union[str, int, float, bool]
    _type: Optional[str] = field(init=False, repr=False, compare=False, default=None)

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class ValueKey(Key):
    def __post_init__(self):
        self._type = "value"


@dataclass
class ScrollKey(Key):
    def __post_init__(self):
        self._type = "scroll"
