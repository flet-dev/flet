import random
from enum import IntEnum
from typing import Optional, TypeVar

__all__ = ["IconData"]

T = TypeVar("T", bound="IconData")


class IconData(IntEnum):
    """
    Represents an icon used in the UI.

    An icon can come from:

    - the Material icon set via the [`Icons`][flet.] enum,
    - the Cupertino icon set via the [`CupertinoIcons`][flet.] enum,
    - or a custom icon set defined by the developer.

    Internally, an icon is stored as an integer that encodes icon's index
    in its originating code set.

    Encoding structure:

    - Lower 16 bits (bits 0-15): the icon's index.
    - Third byte (bits 16-24): the icon set identifier (set ID),
        which distinguishes between icon sets like Material, Cupertino, etc.

    This encoding scheme allows a single integer to uniquely represent any icon
    across multiple icon sets.
    """

    def __new__(cls, value):
        """
        Create a new IconData enum member.

        Args:
            value: The encoded integer representing the icon.

        Returns:
            An instance of the enum with the encoded value.
        """
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Hook called when a subclass is defined. Used to attach metadata.

        Keyword Args:
            package_name: The Flutter package where the icon set is defined.
            class_name: The name of Flutter class with icon definitions.
        """
        cls._package_name = kwargs.pop("package_name", "")
        cls._class_name = kwargs.pop("class_name", "")
        super().__init_subclass__(**kwargs)

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
