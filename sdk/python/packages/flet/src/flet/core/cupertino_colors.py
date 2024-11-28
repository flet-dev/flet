"""
url='https://raw.githubusercontent.com/flutter/flutter/stable/packages/flutter/lib/src/cupertino/colors.dart'
output_file="$HOME/cupertino_python_colors.txt"
curl -s $url | python -c '
import re

for line in __import__("sys").stdin:
    match1 = re.search(r"static const CupertinoDynamicColor ([a-zA-Z0-9_]+)", line)
    match2 = re.search(r"static const Color ([a-zA-Z0-9_]+)", line)
    if match1:
        print("{} = \"{}\"".format(match1.group(1).upper(), match1.group(1)))
    elif match2:
        print("{} = \"{}\"".format(match2.group(1).upper(), match2.group(1)))
' >> "$output_file"
"""

import random
from enum import Enum, EnumMeta
from typing import Dict, List, Optional, Union, TYPE_CHECKING
from warnings import warn

from flet.utils import deprecated

if TYPE_CHECKING:
    from flet.core.types import ColorValue


class CupertinoColorsDeprecated(EnumMeta):
    def __getattribute__(self, item):
        if not item.startswith("_") and item.isupper():
            warn(
                "cupertino_colors enum is deprecated since version 0.25.0 and will be removed in version 0.28.0. "
                "Use CupertinoColors enum instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        return EnumMeta.__getattribute__(self, item)


class cupertino_colors(str, Enum, metaclass=CupertinoColorsDeprecated):
    @staticmethod
    def with_opacity(opacity: Union[int, float], color: "ColorValue") -> str:
        """
        Returns the color with the specified opacity.

        Args:
            opacity: The opacity value, which must be between 0 and 1.
            color: The color value.

        Returns:
            A string representing the color value with the specified opacity appended.

        Raises:
            AssertionError: If the opacity is not between 0 and 1 (inclusive).
        """
        assert 0 <= opacity <= 1, "opacity must be between 0 and 1"
        color_str = color.value if isinstance(color, Enum) else color
        return f"{color_str},{opacity}"

    @staticmethod
    def random():
        return random.choice(list(cupertino_colors))

    @staticmethod
    @deprecated(
        reason="Use cupertino_colors.random() method instead.",
        version="0.25.0",
        delete_version="0.28.0",
    )
    def random_color():
        return random.choice(list(cupertino_colors))

    PRIMARY = "primary"
    ON_PRIMARY = "onprimary"
    ACTIVE_BLUE = "activeBlue"
    ACTIVE_GREEN = "activeGreen"
    ACTIVE_ORANGE = "activeOrange"
    WHITE = "cupertinoWhite"
    BLACK = "cupertinoBlack"
    LIGHT_BACKGROUND_GRAY = "lightBackgroundGray"
    EXTRA_LIGHT_BACKGROUND_GRAY = "extraLightBackgroundGray"
    DARK_BACKGROUND_GRAY = "darkBackgroundGray"
    INACTIVE_GRAY = "inactiveGray"
    DESTRUCTIVE_RED = "destructiveRed"
    SYSTEM_BLUE = "systemBlue"
    SYSTEM_GREEN = "systemGreen"
    SYSTEM_MINT = "systemMint"
    SYSTEM_INDIGO = "systemIndigo"
    SYSTEM_ORANGE = "systemOrange"
    SYSTEM_PINK = "systemPink"
    SYSTEM_BROWN = "systemBrown"
    SYSTEM_PURPLE = "systemPurple"
    SYSTEM_RED = "systemRed"
    SYSTEM_TEAL = "systemTeal"
    SYSTEM_CYAN = "systemCyan"
    SYSTEM_YELLOW = "systemYellow"
    SYSTEM_GREY = "systemGrey"
    SYSTEM_GREY2 = "systemGrey2"
    SYSTEM_GREY3 = "systemGrey3"
    SYSTEM_GREY4 = "systemGrey4"
    SYSTEM_GREY5 = "systemGrey5"
    SYSTEM_GREY6 = "systemGrey6"
    LABEL = "label"
    SECONDARY_LABEL = "secondaryLabel"
    TERTIARY_LABEL = "tertiaryLabel"
    QUATERNARY_LABEL = "quaternaryLabel"
    SYSTEM_FILL = "systemFill"
    SECONDARY_SYSTEM_FILL = "secondarySystemFill"
    TERTIARY_SYSTEM_FILL = "tertiarySystemFill"
    QUATERNARY_SYSTEM_FILL = "quaternarySystemFill"
    PLACEHOLDER_TEXT = "placeholderText"
    SYSTEM_BACKGROUND = "systemBackground"
    SECONDARY_SYSTEM_BACKGROUND = "secondarySystemBackground"
    TERTIARY_SYSTEM_BACKGROUND = "tertiarySystemBackground"
    SYSTEM_GROUPED_BACKGROUND = "systemGroupedBackground"
    SECONDARY_SYSTEM_GROUPED_BACKGROUND = "secondarySystemGroupedBackground"
    TERTIARY_SYSTEM_GROUPED_BACKGROUND = "tertiarySystemGroupedBackground"
    SEPARATOR = "separator"
    OPAQUE_SEPARATOR = "opaqueSeparator"
    LINK = "link"


class CupertinoColors(str, Enum):
    @staticmethod
    def with_opacity(opacity: Union[int, float], color: "ColorValue") -> str:
        """
        Returns the color with the specified opacity.

        Args:
            opacity: The opacity value, which must be between 0 and 1.
            color: The color value.

        Returns:
            A string representing the color value with the specified opacity appended.

        Raises:
            AssertionError: If the opacity is not between 0 and 1 (inclusive).
        """
        assert 0 <= opacity <= 1, "opacity must be between 0 and 1"
        color_str = color.value if isinstance(color, Enum) else color
        return f"{color_str},{opacity}"

    @staticmethod
    def random(
        exclude: Optional[List["CupertinoColors"]] = None,
        weights: Optional[Dict["CupertinoColors", int]] = None,
    ) -> Optional["CupertinoColors"]:
        """
        Selects a random color, with optional exclusions and weights.

        Args:
            exclude: A list of colors members to exclude from the selection.
            weights: A dictionary mapping color members to their respective weights for weighted random selection.

        Returns:
            A randomly selected color, or None if all members are excluded.
        """
        choices = list(CupertinoColors)
        if exclude:
            choices = [member for member in choices if member not in exclude]
            if not choices:
                return None
        if weights:
            weights_list = [weights.get(c, 1) for c in choices]
            return random.choices(choices, weights=weights_list)[0]
        return random.choice(choices)

    PRIMARY = "primary"
    ON_PRIMARY = "onprimary"
    ACTIVE_BLUE = "activeBlue"
    ACTIVE_GREEN = "activeGreen"
    ACTIVE_ORANGE = "activeOrange"
    WHITE = "cupertinoWhite"
    BLACK = "cupertinoBlack"
    LIGHT_BACKGROUND_GRAY = "lightBackgroundGray"
    EXTRA_LIGHT_BACKGROUND_GRAY = "extraLightBackgroundGray"
    DARK_BACKGROUND_GRAY = "darkBackgroundGray"
    INACTIVE_GRAY = "inactiveGray"
    DESTRUCTIVE_RED = "destructiveRed"
    SYSTEM_BLUE = "systemBlue"
    SYSTEM_GREEN = "systemGreen"
    SYSTEM_MINT = "systemMint"
    SYSTEM_INDIGO = "systemIndigo"
    SYSTEM_ORANGE = "systemOrange"
    SYSTEM_PINK = "systemPink"
    SYSTEM_BROWN = "systemBrown"
    SYSTEM_PURPLE = "systemPurple"
    SYSTEM_RED = "systemRed"
    SYSTEM_TEAL = "systemTeal"
    SYSTEM_CYAN = "systemCyan"
    SYSTEM_YELLOW = "systemYellow"
    SYSTEM_GREY = "systemGrey"
    SYSTEM_GREY2 = "systemGrey2"
    SYSTEM_GREY3 = "systemGrey3"
    SYSTEM_GREY4 = "systemGrey4"
    SYSTEM_GREY5 = "systemGrey5"
    SYSTEM_GREY6 = "systemGrey6"
    LABEL = "label"
    SECONDARY_LABEL = "secondaryLabel"
    TERTIARY_LABEL = "tertiaryLabel"
    QUATERNARY_LABEL = "quaternaryLabel"
    SYSTEM_FILL = "systemFill"
    SECONDARY_SYSTEM_FILL = "secondarySystemFill"
    TERTIARY_SYSTEM_FILL = "tertiarySystemFill"
    QUATERNARY_SYSTEM_FILL = "quaternarySystemFill"
    PLACEHOLDER_TEXT = "placeholderText"
    SYSTEM_BACKGROUND = "systemBackground"
    SECONDARY_SYSTEM_BACKGROUND = "secondarySystemBackground"
    TERTIARY_SYSTEM_BACKGROUND = "tertiarySystemBackground"
    SYSTEM_GROUPED_BACKGROUND = "systemGroupedBackground"
    SECONDARY_SYSTEM_GROUPED_BACKGROUND = "secondarySystemGroupedBackground"
    TERTIARY_SYSTEM_GROUPED_BACKGROUND = "tertiarySystemGroupedBackground"
    SEPARATOR = "separator"
    OPAQUE_SEPARATOR = "opaqueSeparator"
    LINK = "link"
