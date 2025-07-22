from enum import Enum


class SelectionType(Enum):
    SINGLE = 0
    MULTIPLE = 1
    RANGE = 2

    @staticmethod
    def from_value(value):
        return SelectionType(value)
