from enum import Enum


class ExtendedEnum(Enum):
    """
    ExtendedEnum allows case-insensitive string comparison when checking equality.
    """

    def __eq__(self, other):
        """
        Compares the enum value with a string (case-insensitive) or another enum.

        Args:
            other (str | ExtendedEnum): Value to compare.

        Returns:
            bool: True if values match, False otherwise.
        """
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        elif isinstance(other, ExtendedEnum):
            return self.value == other.value
        else:
            return False

    def __hash__(self):
        return hash(self.value)
