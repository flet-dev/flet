import random
from enum import IntEnum
from typing import Optional, TypeVar

__all__ = ["BaseIcon"]

T = TypeVar("T", bound="BaseIcon")


class BaseIcon(IntEnum):
    @classmethod
    def random(
        cls: type[T],
        exclude: Optional[list[T]] = None,
        weights: Optional[dict[T, int]] = None,
    ) -> Optional[T]:
        """
        Selects a random icon from the subclass enum, with optional
        exclusions and weights.
        """
        choices = list(cls)
        if exclude:
            choices = [member for member in choices if member not in exclude]
            if not choices:
                return None
        if weights:
            weights_list = [weights.get(c, 1) for c in choices]
            return random.choices(choices, weights=weights_list)[0]
        return random.choice(choices)
