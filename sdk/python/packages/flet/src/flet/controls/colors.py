"""
Code to generate colors:
```
$lines = Get-Content "colors.dart"

$section = ''

foreach($line in $lines) {

    if ($line.Contains("case `"")) {
        $color = $line.Replace('case "', "").replace('":', "").trim()
        $ucolor = $color.toUpper()
        "$ucolor = `"$color`""
    } elseif ($line.Contains('Map<String, Color> _plainColors')) {
        $section = 'plain'
    } elseif ($line.Contains('Map<String, MaterialColor> _materialColors')) {
        $section = 'primary'
    } elseif ($line.Contains('Map<String, MaterialAccentColor> _materialAccentColors'))
    {
        $section = 'accent'
    } elseif ($line.startswith('  "')) {
        $color = $line.split('"')[1]
        $ucolor = $color.replace('deep', 'deep_') \
               .replace('light', 'light_') \
               .replace('grey', '_grey') \
               .replace('accent', '_accent')
        $ucolor = $ucolor.upper()
        "$ucolor = `"$color`""
        if ($section -eq 'primary') {
            $shades = @(50, 100, 200, 300, 400, 500, 600, 700, 800, 900)
            foreach($shade in $shades) {
                "$($ucolor)_$shade = `"$($color)$shade`""
            }
        } elseif ($section -eq 'accent') {
            $shades = @(100, 200, 400, 700)
            foreach($shade in $shades) {
                "$($ucolor)_$shade = `"$($color)$shade`""
            }
        }
    }
}
```

---

Code to sort the members:
```
s = sorted(Colors, key=lambda i: i.value)
for i in s:
    print(f'{i.name} = "{i.value}"')
```
"""

import random
from enum import Enum
from typing import TYPE_CHECKING, Optional, Union

from flet.utils.deprecated_enum import DeprecatedEnumMeta

if TYPE_CHECKING:
    from flet.controls.types import ColorValue

__all__ = ["Colors"]


class Colors(str, Enum, metaclass=DeprecatedEnumMeta):
    def __eq__(self, other):
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        if isinstance(other, Enum):
            return self.value.lower() == other.value.lower()
        return NotImplemented

    def __hash__(self):
        return hash(self.value.lower())

    @staticmethod
    def random(
        exclude: Optional[list["Colors"]] = None,
        weights: Optional[dict["Colors", int]] = None,
    ) -> Optional["Colors"]:
        """
        Selects a random color, with optional exclusions and weights.

        Args:
            exclude: A list of Colors to exclude from the selection.
            weights: A dictionary mapping color members to their respective weights for
                weighted random selection.

        Returns:
            A randomly selected color, or None if all members are excluded.

        Examples:
            >>> Colors.random(exclude=[Colors.RED, Colors.GREEN])
            Colors.BLUE
        """
        choices = list(Colors)
        if exclude:
            choices = [member for member in choices if member not in exclude]
            if not choices:
                return None
        if weights:
            weights_list = [weights.get(c, 1) for c in choices]
            return random.choices(choices, weights=weights_list)[0]
        return random.choice(choices)

    @staticmethod
    def with_opacity(opacity: Union[int, float], color: "ColorValue") -> str:
        """
        Returns a color with the given opacity.

        Args:
            opacity: The opacity value between `0.0` and `1.0`.
            color: The color to apply opacity to.

        Returns:
            A string representing the color with opacity, in the format
            `"color,opacity"`.

        Examples:
            >>> Colors.with_opacity(0.5, Colors.RED)
            'red,0.5'

        Raises:
            ValueError: If the opacity is not between `0` and `1` (inclusive).
        """
        if not (0 <= opacity <= 1):
            raise ValueError(
                f"opacity must be between 0.0 and 1.0 inclusive, got {opacity}"
            )
        color_str = color.value if isinstance(color, Enum) else color
        return f"{color_str},{opacity}"

    PRIMARY = "primary"
    ON_PRIMARY = "onprimary"
    PRIMARY_CONTAINER = "primarycontainer"
    ON_PRIMARY_CONTAINER = "onprimarycontainer"
    PRIMARY_FIXED = "primaryfixed"
    PRIMARY_FIXED_DIM = "primaryfixeddim"
    ON_PRIMARY_FIXED = "onprimaryfixed"
    ON_PRIMARY_FIXED_VARIANT = "onprimaryfixedvariant"

    SECONDARY = "secondary"
    ON_SECONDARY = "onsecondary"
    SECONDARY_CONTAINER = "secondarycontainer"
    ON_SECONDARY_CONTAINER = "onsecondarycontainer"
    SECONDARY_FIXED = "secondaryfixed"
    SECONDARY_FIXED_DIM = "secondaryfixeddim"
    ON_SECONDARY_FIXED = "onsecondaryfixed"
    ON_SECONDARY_FIXED_VARIANT = "onsecondaryfixedvariant"

    TERTIARY = "tertiary"
    ON_TERTIARY = "ontertiary"
    TERTIARY_CONTAINER = "tertiarycontainer"
    ON_TERTIARY_CONTAINER = "ontertiarycontainer"
    TERTIARY_FIXED = "tertiaryfixed"
    TERTIARY_FIXED_DIM = "tertiaryfixeddim"
    ON_TERTIARY_FIXED = "ontertiaryfixed"
    ON_TERTIARY_FIXED_VARIANT = "ontertiaryfixedvariant"

    ERROR = "error"
    ON_ERROR = "onerror"
    ERROR_CONTAINER = "errorcontainer"
    ON_ERROR_CONTAINER = "onerrorcontainer"

    SURFACE = "surface"
    ON_SURFACE = "onsurface"
    ON_SURFACE_VARIANT = "onsurfacevariant"
    SURFACE_TINT = "surfacetint"
    SURFACE_DIM = "surfacedim"
    SURFACE_BRIGHT = "surfacebright"
    SURFACE_CONTAINER = "surfacecontainer"
    SURFACE_CONTAINER_LOW = "surfacecontainerlow"
    SURFACE_CONTAINER_LOWEST = "surfacecontainerlowest"
    SURFACE_CONTAINER_HIGH = "surfacecontainerhigh"
    SURFACE_CONTAINER_HIGHEST = "surfacecontainerhighest"

    OUTLINE = "outline"
    OUTLINE_VARIANT = "outlinevariant"
    SHADOW = "shadow"
    SCRIM = "scrim"
    INVERSE_SURFACE = "inversesurface"
    ON_INVERSE_SURFACE = "oninversesurface"
    INVERSE_PRIMARY = "inverseprimary"

    AMBER = "amber"
    AMBER_100 = "amber100"
    AMBER_200 = "amber200"
    AMBER_300 = "amber300"
    AMBER_400 = "amber400"
    AMBER_50 = "amber50"
    AMBER_500 = "amber500"
    AMBER_600 = "amber600"
    AMBER_700 = "amber700"
    AMBER_800 = "amber800"
    AMBER_900 = "amber900"
    AMBER_ACCENT = "amberaccent"
    AMBER_ACCENT_100 = "amberaccent100"
    AMBER_ACCENT_200 = "amberaccent200"
    AMBER_ACCENT_400 = "amberaccent400"
    AMBER_ACCENT_700 = "amberaccent700"
    BLACK = "black"
    BLACK_12 = "black12"
    BLACK_26 = "black26"
    BLACK_38 = "black38"
    BLACK_45 = "black45"
    BLACK_54 = "black54"
    BLACK_87 = "black87"
    BLUE = "blue"
    BLUE_100 = "blue100"
    BLUE_200 = "blue200"
    BLUE_300 = "blue300"
    BLUE_400 = "blue400"
    BLUE_50 = "blue50"
    BLUE_500 = "blue500"
    BLUE_600 = "blue600"
    BLUE_700 = "blue700"
    BLUE_800 = "blue800"
    BLUE_900 = "blue900"
    BLUE_ACCENT = "blueaccent"
    BLUE_ACCENT_100 = "blueaccent100"
    BLUE_ACCENT_200 = "blueaccent200"
    BLUE_ACCENT_400 = "blueaccent400"
    BLUE_ACCENT_700 = "blueaccent700"
    BLUE_GREY = "bluegrey"
    BLUE_GREY_100 = "bluegrey100"
    BLUE_GREY_200 = "bluegrey200"
    BLUE_GREY_300 = "bluegrey300"
    BLUE_GREY_400 = "bluegrey400"
    BLUE_GREY_50 = "bluegrey50"
    BLUE_GREY_500 = "bluegrey500"
    BLUE_GREY_600 = "bluegrey600"
    BLUE_GREY_700 = "bluegrey700"
    BLUE_GREY_800 = "bluegrey800"
    BLUE_GREY_900 = "bluegrey900"
    BROWN = "brown"
    BROWN_100 = "brown100"
    BROWN_200 = "brown200"
    BROWN_300 = "brown300"
    BROWN_400 = "brown400"
    BROWN_50 = "brown50"
    BROWN_500 = "brown500"
    BROWN_600 = "brown600"
    BROWN_700 = "brown700"
    BROWN_800 = "brown800"
    BROWN_900 = "brown900"
    CYAN = "cyan"
    CYAN_100 = "cyan100"
    CYAN_200 = "cyan200"
    CYAN_300 = "cyan300"
    CYAN_400 = "cyan400"
    CYAN_50 = "cyan50"
    CYAN_500 = "cyan500"
    CYAN_600 = "cyan600"
    CYAN_700 = "cyan700"
    CYAN_800 = "cyan800"
    CYAN_900 = "cyan900"
    CYAN_ACCENT = "cyanaccent"
    CYAN_ACCENT_100 = "cyanaccent100"
    CYAN_ACCENT_200 = "cyanaccent200"
    CYAN_ACCENT_400 = "cyanaccent400"
    CYAN_ACCENT_700 = "cyanaccent700"
    DEEP_ORANGE = "deeporange"
    DEEP_ORANGE_100 = "deeporange100"
    DEEP_ORANGE_200 = "deeporange200"
    DEEP_ORANGE_300 = "deeporange300"
    DEEP_ORANGE_400 = "deeporange400"
    DEEP_ORANGE_50 = "deeporange50"
    DEEP_ORANGE_500 = "deeporange500"
    DEEP_ORANGE_600 = "deeporange600"
    DEEP_ORANGE_700 = "deeporange700"
    DEEP_ORANGE_800 = "deeporange800"
    DEEP_ORANGE_900 = "deeporange900"
    DEEP_ORANGE_ACCENT = "deeporangeaccent"
    DEEP_ORANGE_ACCENT_100 = "deeporangeaccent100"
    DEEP_ORANGE_ACCENT_200 = "deeporangeaccent200"
    DEEP_ORANGE_ACCENT_400 = "deeporangeaccent400"
    DEEP_ORANGE_ACCENT_700 = "deeporangeaccent700"
    DEEP_PURPLE = "deeppurple"
    DEEP_PURPLE_100 = "deeppurple100"
    DEEP_PURPLE_200 = "deeppurple200"
    DEEP_PURPLE_300 = "deeppurple300"
    DEEP_PURPLE_400 = "deeppurple400"
    DEEP_PURPLE_50 = "deeppurple50"
    DEEP_PURPLE_500 = "deeppurple500"
    DEEP_PURPLE_600 = "deeppurple600"
    DEEP_PURPLE_700 = "deeppurple700"
    DEEP_PURPLE_800 = "deeppurple800"
    DEEP_PURPLE_900 = "deeppurple900"
    DEEP_PURPLE_ACCENT = "deeppurpleaccent"
    DEEP_PURPLE_ACCENT_100 = "deeppurpleaccent100"
    DEEP_PURPLE_ACCENT_200 = "deeppurpleaccent200"
    DEEP_PURPLE_ACCENT_400 = "deeppurpleaccent400"
    DEEP_PURPLE_ACCENT_700 = "deeppurpleaccent700"
    GREEN = "green"
    GREEN_100 = "green100"
    GREEN_200 = "green200"
    GREEN_300 = "green300"
    GREEN_400 = "green400"
    GREEN_50 = "green50"
    GREEN_500 = "green500"
    GREEN_600 = "green600"
    GREEN_700 = "green700"
    GREEN_800 = "green800"
    GREEN_900 = "green900"
    GREEN_ACCENT = "greenaccent"
    GREEN_ACCENT_100 = "greenaccent100"
    GREEN_ACCENT_200 = "greenaccent200"
    GREEN_ACCENT_400 = "greenaccent400"
    GREEN_ACCENT_700 = "greenaccent700"
    GREY = "grey"
    GREY_100 = "grey100"
    GREY_200 = "grey200"
    GREY_300 = "grey300"
    GREY_400 = "grey400"
    GREY_50 = "grey50"
    GREY_500 = "grey500"
    GREY_600 = "grey600"
    GREY_700 = "grey700"
    GREY_800 = "grey800"
    GREY_900 = "grey900"
    INDIGO = "indigo"
    INDIGO_100 = "indigo100"
    INDIGO_200 = "indigo200"
    INDIGO_300 = "indigo300"
    INDIGO_400 = "indigo400"
    INDIGO_50 = "indigo50"
    INDIGO_500 = "indigo500"
    INDIGO_600 = "indigo600"
    INDIGO_700 = "indigo700"
    INDIGO_800 = "indigo800"
    INDIGO_900 = "indigo900"
    INDIGO_ACCENT = "indigoaccent"
    INDIGO_ACCENT_100 = "indigoaccent100"
    INDIGO_ACCENT_200 = "indigoaccent200"
    INDIGO_ACCENT_400 = "indigoaccent400"
    INDIGO_ACCENT_700 = "indigoaccent700"
    LIGHT_BLUE = "lightblue"
    LIGHT_BLUE_100 = "lightblue100"
    LIGHT_BLUE_200 = "lightblue200"
    LIGHT_BLUE_300 = "lightblue300"
    LIGHT_BLUE_400 = "lightblue400"
    LIGHT_BLUE_50 = "lightblue50"
    LIGHT_BLUE_500 = "lightblue500"
    LIGHT_BLUE_600 = "lightblue600"
    LIGHT_BLUE_700 = "lightblue700"
    LIGHT_BLUE_800 = "lightblue800"
    LIGHT_BLUE_900 = "lightblue900"
    LIGHT_BLUE_ACCENT = "lightblueaccent"
    LIGHT_BLUE_ACCENT_100 = "lightblueaccent100"
    LIGHT_BLUE_ACCENT_200 = "lightblueaccent200"
    LIGHT_BLUE_ACCENT_400 = "lightblueaccent400"
    LIGHT_BLUE_ACCENT_700 = "lightblueaccent700"
    LIGHT_GREEN = "lightgreen"
    LIGHT_GREEN_100 = "lightgreen100"
    LIGHT_GREEN_200 = "lightgreen200"
    LIGHT_GREEN_300 = "lightgreen300"
    LIGHT_GREEN_400 = "lightgreen400"
    LIGHT_GREEN_50 = "lightgreen50"
    LIGHT_GREEN_500 = "lightgreen500"
    LIGHT_GREEN_600 = "lightgreen600"
    LIGHT_GREEN_700 = "lightgreen700"
    LIGHT_GREEN_800 = "lightgreen800"
    LIGHT_GREEN_900 = "lightgreen900"
    LIGHT_GREEN_ACCENT = "lightgreenaccent"
    LIGHT_GREEN_ACCENT_100 = "lightgreenaccent100"
    LIGHT_GREEN_ACCENT_200 = "lightgreenaccent200"
    LIGHT_GREEN_ACCENT_400 = "lightgreenaccent400"
    LIGHT_GREEN_ACCENT_700 = "lightgreenaccent700"
    LIME = "lime"
    LIME_100 = "lime100"
    LIME_200 = "lime200"
    LIME_300 = "lime300"
    LIME_400 = "lime400"
    LIME_50 = "lime50"
    LIME_500 = "lime500"
    LIME_600 = "lime600"
    LIME_700 = "lime700"
    LIME_800 = "lime800"
    LIME_900 = "lime900"
    LIME_ACCENT = "limeaccent"
    LIME_ACCENT_100 = "limeaccent100"
    LIME_ACCENT_200 = "limeaccent200"
    LIME_ACCENT_400 = "limeaccent400"
    LIME_ACCENT_700 = "limeaccent700"
    ORANGE = "orange"
    ORANGE_100 = "orange100"
    ORANGE_200 = "orange200"
    ORANGE_300 = "orange300"
    ORANGE_400 = "orange400"
    ORANGE_50 = "orange50"
    ORANGE_500 = "orange500"
    ORANGE_600 = "orange600"
    ORANGE_700 = "orange700"
    ORANGE_800 = "orange800"
    ORANGE_900 = "orange900"
    ORANGE_ACCENT = "orangeaccent"
    ORANGE_ACCENT_100 = "orangeaccent100"
    ORANGE_ACCENT_200 = "orangeaccent200"
    ORANGE_ACCENT_400 = "orangeaccent400"
    ORANGE_ACCENT_700 = "orangeaccent700"
    PINK = "pink"
    PINK_100 = "pink100"
    PINK_200 = "pink200"
    PINK_300 = "pink300"
    PINK_400 = "pink400"
    PINK_50 = "pink50"
    PINK_500 = "pink500"
    PINK_600 = "pink600"
    PINK_700 = "pink700"
    PINK_800 = "pink800"
    PINK_900 = "pink900"
    PINK_ACCENT = "pinkaccent"
    PINK_ACCENT_100 = "pinkaccent100"
    PINK_ACCENT_200 = "pinkaccent200"
    PINK_ACCENT_400 = "pinkaccent400"
    PINK_ACCENT_700 = "pinkaccent700"
    PURPLE = "purple"
    PURPLE_100 = "purple100"
    PURPLE_200 = "purple200"
    PURPLE_300 = "purple300"
    PURPLE_400 = "purple400"
    PURPLE_50 = "purple50"
    PURPLE_500 = "purple500"
    PURPLE_600 = "purple600"
    PURPLE_700 = "purple700"
    PURPLE_800 = "purple800"
    PURPLE_900 = "purple900"
    PURPLE_ACCENT = "purpleaccent"
    PURPLE_ACCENT_100 = "purpleaccent100"
    PURPLE_ACCENT_200 = "purpleaccent200"
    PURPLE_ACCENT_400 = "purpleaccent400"
    PURPLE_ACCENT_700 = "purpleaccent700"
    RED = "red"
    RED_100 = "red100"
    RED_200 = "red200"
    RED_300 = "red300"
    RED_400 = "red400"
    RED_50 = "red50"
    RED_500 = "red500"
    RED_600 = "red600"
    RED_700 = "red700"
    RED_800 = "red800"
    RED_900 = "red900"
    RED_ACCENT = "redaccent"
    RED_ACCENT_100 = "redaccent100"
    RED_ACCENT_200 = "redaccent200"
    RED_ACCENT_400 = "redaccent400"
    RED_ACCENT_700 = "redaccent700"
    TEAL = "teal"
    TEAL_100 = "teal100"
    TEAL_200 = "teal200"
    TEAL_300 = "teal300"
    TEAL_400 = "teal400"
    TEAL_50 = "teal50"
    TEAL_500 = "teal500"
    TEAL_600 = "teal600"
    TEAL_700 = "teal700"
    TEAL_800 = "teal800"
    TEAL_900 = "teal900"
    TEAL_ACCENT = "tealaccent"
    TEAL_ACCENT_100 = "tealaccent100"
    TEAL_ACCENT_200 = "tealaccent200"
    TEAL_ACCENT_400 = "tealaccent400"
    TEAL_ACCENT_700 = "tealaccent700"
    TRANSPARENT = "transparent"
    WHITE = "white"
    WHITE_10 = "white10"
    WHITE_12 = "white12"
    WHITE_24 = "white24"
    WHITE_30 = "white30"
    WHITE_38 = "white38"
    WHITE_54 = "white54"
    WHITE_60 = "white60"
    WHITE_70 = "white70"
    YELLOW = "yellow"
    YELLOW_100 = "yellow100"
    YELLOW_200 = "yellow200"
    YELLOW_300 = "yellow300"
    YELLOW_400 = "yellow400"
    YELLOW_50 = "yellow50"
    YELLOW_500 = "yellow500"
    YELLOW_600 = "yellow600"
    YELLOW_700 = "yellow700"
    YELLOW_800 = "yellow800"
    YELLOW_900 = "yellow900"
    YELLOW_ACCENT = "yellowaccent"
    YELLOW_ACCENT_100 = "yellowaccent100"
    YELLOW_ACCENT_200 = "yellowaccent200"
    YELLOW_ACCENT_400 = "yellowaccent400"
    YELLOW_ACCENT_700 = "yellowaccent700"


# TODO - remove in Flet 1.0
_DEPRECATED_COLOR_ALIASES = {
    "BLACK12": ("BLACK_12", "Use Colors.BLACK_12 instead."),
    "BLACK26": ("BLACK_26", "Use Colors.BLACK_26 instead."),
    "BLACK38": ("BLACK_38", "Use Colors.BLACK_38 instead."),
    "BLACK45": ("BLACK_45", "Use Colors.BLACK_45 instead."),
    "BLACK54": ("BLACK_54", "Use Colors.BLACK_54 instead."),
    "BLACK87": ("BLACK_87", "Use Colors.BLACK_87 instead."),
    "WHITE10": ("WHITE_10", "Use Colors.WHITE_10 instead."),
    "WHITE12": ("WHITE_12", "Use Colors.WHITE_12 instead."),
    "WHITE24": ("WHITE_24", "Use Colors.WHITE_24 instead."),
    "WHITE30": ("WHITE_30", "Use Colors.WHITE_30 instead."),
    "WHITE38": ("WHITE_38", "Use Colors.WHITE_38 instead."),
    "WHITE54": ("WHITE_54", "Use Colors.WHITE_54 instead."),
    "WHITE60": ("WHITE_60", "Use Colors.WHITE_60 instead."),
    "WHITE70": ("WHITE_70", "Use Colors.WHITE_70 instead."),
}

Colors._deprecated_members_ = _DEPRECATED_COLOR_ALIASES

for alias_name, (target_name, _) in _DEPRECATED_COLOR_ALIASES.items():
    Colors._member_map_[alias_name] = getattr(Colors, target_name)
