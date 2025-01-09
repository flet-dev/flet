from enum import Enum


class ExtendedEnum(Enum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return self.value == other.value
