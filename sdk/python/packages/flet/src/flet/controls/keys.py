from dataclasses import dataclass
from typing import Union


@dataclass()
class Key:
    value: Union[str, int, float, bool]
    type: str = ""

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class ValueKey(Key):
    def __post_init__(self):
        self.type = "value"


@dataclass
class ScrollKey(Key):
    def __post_init__(self):
        self.type = "scroll"
