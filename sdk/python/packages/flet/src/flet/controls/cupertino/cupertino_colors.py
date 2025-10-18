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

---

Code to sort the members:
```
s = sorted(CupertinoColors, key=lambda i: i.name)
for i in s:
    print(f'{i.name} = "{i.value}"')
```
"""

import random
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

if TYPE_CHECKING:
    from flet.controls.types import ColorValue

__all__ = ["CupertinoColors"]


class CupertinoColors(str, Enum):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        if isinstance(other, Enum):
            return self.value.lower() == other.value.lower()
        return NotImplemented

    def __hash__(self):
        return hash(self.value.lower())

    @staticmethod
    def with_opacity(opacity: Union[int, float], color: "ColorValue") -> str:
        """
        Returns the color with the specified opacity.

        Args:
            opacity: The opacity value between `0.0` and `1.0`.
            color: The color to apply opacity to.

        Returns:
            A string representing the color with opacity,
                in the format `"color,opacity"`.

        Examples:
            >>> CupertinoColors.with_opacity(0.5, CupertinoColors.WHITE)
            'white,0.5'

        Raises:
            ValueError: If the opacity is not between `0` and `1` (inclusive).
        """
        if not (0 <= opacity <= 1):
            raise ValueError(
                f"opacity must be between 0.0 and 1.0 inclusive, got {opacity}"
            )
        color_str = color.value if isinstance(color, Enum) else color
        return f"{color_str},{opacity}"

    @staticmethod
    def random(
        exclude: Optional[list["CupertinoColors"]] = None,
        weights: Optional[dict["CupertinoColors", int]] = None,
    ) -> Optional["CupertinoColors"]:
        """
        Selects a random color, with optional exclusions and weights.

        Args:
            exclude: A list of colors members to exclude from the selection.
            weights: A dictionary mapping color members to their respective weights for
                weighted random selection.

        Returns:
            A randomly selected color, or None if all members are excluded.

        Examples:
            >>> CupertinoColors.random(exclude=[CupertinoColors.WHITE])
            CupertinoColors.ON_PRIMARY
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

    ACTIVE_BLUE = "activeBlue"
    ACTIVE_GREEN = "activeGreen"
    ACTIVE_ORANGE = "activeOrange"
    BLACK = "cupertinoBlack"
    DARK_BACKGROUND_GRAY = "darkBackgroundGray"
    DESTRUCTIVE_RED = "destructiveRed"
    EXTRA_LIGHT_BACKGROUND_GRAY = "extraLightBackgroundGray"
    INACTIVE_GRAY = "inactiveGray"
    LABEL = "label"
    LIGHT_BACKGROUND_GRAY = "lightBackgroundGray"
    LINK = "link"
    ON_PRIMARY = "onprimary"
    OPAQUE_SEPARATOR = "opaqueSeparator"
    PLACEHOLDER_TEXT = "placeholderText"
    PRIMARY = "primary"
    QUATERNARY_LABEL = "quaternaryLabel"
    QUATERNARY_SYSTEM_FILL = "quaternarySystemFill"
    SECONDARY_LABEL = "secondaryLabel"
    SECONDARY_SYSTEM_BACKGROUND = "secondarySystemBackground"
    SECONDARY_SYSTEM_FILL = "secondarySystemFill"
    SECONDARY_SYSTEM_GROUPED_BACKGROUND = "secondarySystemGroupedBackground"
    SEPARATOR = "separator"
    SYSTEM_BACKGROUND = "systemBackground"
    SYSTEM_BLUE = "systemBlue"
    SYSTEM_BROWN = "systemBrown"
    SYSTEM_CYAN = "systemCyan"
    SYSTEM_FILL = "systemFill"
    SYSTEM_GREEN = "systemGreen"
    SYSTEM_GREY = "systemGrey"
    SYSTEM_GREY2 = "systemGrey2"
    SYSTEM_GREY3 = "systemGrey3"
    SYSTEM_GREY4 = "systemGrey4"
    SYSTEM_GREY5 = "systemGrey5"
    SYSTEM_GREY6 = "systemGrey6"
    SYSTEM_GROUPED_BACKGROUND = "systemGroupedBackground"
    SYSTEM_INDIGO = "systemIndigo"
    SYSTEM_MINT = "systemMint"
    SYSTEM_ORANGE = "systemOrange"
    SYSTEM_PINK = "systemPink"
    SYSTEM_PURPLE = "systemPurple"
    SYSTEM_RED = "systemRed"
    SYSTEM_TEAL = "systemTeal"
    SYSTEM_YELLOW = "systemYellow"
    TERTIARY_LABEL = "tertiaryLabel"
    TERTIARY_SYSTEM_BACKGROUND = "tertiarySystemBackground"
    TERTIARY_SYSTEM_FILL = "tertiarySystemFill"
    TERTIARY_SYSTEM_GROUPED_BACKGROUND = "tertiarySystemGroupedBackground"
    WHITE = "cupertinoWhite"
