"""
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
    } elseif ($line.Contains('Map<String, MaterialAccentColor> _materialAccentColors')) {
        $section = 'accent'
    } elseif ($line.startswith('  "')) {
        $color = $line.split('"')[1]
        $ucolor = $color.replace('deep', 'deep_').replace('light', 'light_').replace('grey', '_grey').replace('accent', '_accent').toUpper()

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
"""

import random
from enum import Enum, EnumMeta
from typing import Dict, List, Optional, Union
from warnings import warn

from flet.utils import deprecated


class ColorsDeprecated(EnumMeta):
    def __getattribute__(self, item):
        if not item.startswith("_"):
            warn(
                "colors enum is deprecated since version 0.25.0 and will be removed in version 0.28.0. "
                "Use Colors enum instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        return EnumMeta.__getattribute__(self, item)


class colors(str, Enum, metaclass=ColorsDeprecated):
    def with_opacity(self, opacity: Union[int, float]) -> str:
        assert 0 <= opacity <= 1, "opacity must be between 0 and 1"
        return f"{self.value},{opacity}"

    @staticmethod
    def random():
        return random.choice(list(colors))

    @staticmethod
    @deprecated(
        reason="Use colors.random() method instead.",
        version="0.25.0",
        delete_version="0.28.0",
    )
    def random_color():
        return random.choice(list(colors))

    PRIMARY = "primary"
    ON_PRIMARY = "onprimary"
    PRIMARY_CONTAINER = "primarycontainer"
    ON_PRIMARY_CONTAINER = "onprimarycontainer"
    SECONDARY = "secondary"
    ON_SECONDARY = "onsecondary"
    SECONDARY_CONTAINER = "secondarycontainer"
    ON_SECONDARY_CONTAINER = "onsecondarycontainer"
    TERTIARY = "tertiary"
    ON_TERTIARY = "ontertiary"
    TERTIARY_CONTAINER = "tertiarycontainer"
    ON_TERTIARY_CONTAINER = "ontertiarycontainer"
    ERROR = "error"
    ON_ERROR = "onerror"
    ERROR_CONTAINER = "errorcontainer"
    ON_ERROR_CONTAINER = "onerrorcontainer"
    OUTLINE = "outline"
    OUTLINE_VARIANT = "outlinevariant"
    BACKGROUND = "background"  # deprecated - use SURFACE instead
    ON_BACKGROUND = "onbackground"  # deprecated - use ON_SURFACE instead
    SURFACE = "surface"
    ON_SURFACE = "onsurface"
    SURFACE_TINT = "surfacetint"
    SURFACE_VARIANT = (
        "surfacevariant"  # deprecated - use SURFACE_CONTAINER_HIGHEST instead
    )
    SURFACE_CONTAINER_HIGHEST = "surfaceContainerHighest"
    ON_SURFACE_VARIANT = "onsurfacevariant"
    INVERSE_SURFACE = "inversesurface"
    ON_INVERSE_SURFACE = "oninversesurface"
    INVERSE_PRIMARY = "inverseprimary"
    SHADOW = "shadow"
    SCRIM = "scrim"

    WHITE10 = "white10"
    WHITE12 = "white12"
    WHITE24 = "white24"
    WHITE30 = "white30"
    WHITE38 = "white38"
    WHITE54 = "white54"
    WHITE60 = "white60"
    WHITE70 = "white70"
    WHITE = "white"
    TRANSPARENT = "transparent"
    BLACK12 = "black12"
    BLACK26 = "black26"
    BLACK38 = "black38"
    BLACK45 = "black45"
    BLACK54 = "black54"
    BLACK87 = "black87"
    BLACK = "black"
    RED = "red"
    RED_50 = "red50"
    RED_100 = "red100"
    RED_200 = "red200"
    RED_300 = "red300"
    RED_400 = "red400"
    RED_500 = "red500"
    RED_600 = "red600"
    RED_700 = "red700"
    RED_800 = "red800"
    RED_900 = "red900"
    PINK = "pink"
    PINK_50 = "pink50"
    PINK_100 = "pink100"
    PINK_200 = "pink200"
    PINK_300 = "pink300"
    PINK_400 = "pink400"
    PINK_500 = "pink500"
    PINK_600 = "pink600"
    PINK_700 = "pink700"
    PINK_800 = "pink800"
    PINK_900 = "pink900"
    PURPLE = "purple"
    PURPLE_50 = "purple50"
    PURPLE_100 = "purple100"
    PURPLE_200 = "purple200"
    PURPLE_300 = "purple300"
    PURPLE_400 = "purple400"
    PURPLE_500 = "purple500"
    PURPLE_600 = "purple600"
    PURPLE_700 = "purple700"
    PURPLE_800 = "purple800"
    PURPLE_900 = "purple900"
    DEEP_PURPLE = "deeppurple"
    DEEP_PURPLE_50 = "deeppurple50"
    DEEP_PURPLE_100 = "deeppurple100"
    DEEP_PURPLE_200 = "deeppurple200"
    DEEP_PURPLE_300 = "deeppurple300"
    DEEP_PURPLE_400 = "deeppurple400"
    DEEP_PURPLE_500 = "deeppurple500"
    DEEP_PURPLE_600 = "deeppurple600"
    DEEP_PURPLE_700 = "deeppurple700"
    DEEP_PURPLE_800 = "deeppurple800"
    DEEP_PURPLE_900 = "deeppurple900"
    INDIGO = "indigo"
    INDIGO_50 = "indigo50"
    INDIGO_100 = "indigo100"
    INDIGO_200 = "indigo200"
    INDIGO_300 = "indigo300"
    INDIGO_400 = "indigo400"
    INDIGO_500 = "indigo500"
    INDIGO_600 = "indigo600"
    INDIGO_700 = "indigo700"
    INDIGO_800 = "indigo800"
    INDIGO_900 = "indigo900"
    BLUE = "blue"
    BLUE_50 = "blue50"
    BLUE_100 = "blue100"
    BLUE_200 = "blue200"
    BLUE_300 = "blue300"
    BLUE_400 = "blue400"
    BLUE_500 = "blue500"
    BLUE_600 = "blue600"
    BLUE_700 = "blue700"
    BLUE_800 = "blue800"
    BLUE_900 = "blue900"
    LIGHT_BLUE = "lightblue"
    LIGHT_BLUE_50 = "lightblue50"
    LIGHT_BLUE_100 = "lightblue100"
    LIGHT_BLUE_200 = "lightblue200"
    LIGHT_BLUE_300 = "lightblue300"
    LIGHT_BLUE_400 = "lightblue400"
    LIGHT_BLUE_500 = "lightblue500"
    LIGHT_BLUE_600 = "lightblue600"
    LIGHT_BLUE_700 = "lightblue700"
    LIGHT_BLUE_800 = "lightblue800"
    LIGHT_BLUE_900 = "lightblue900"
    CYAN = "cyan"
    CYAN_50 = "cyan50"
    CYAN_100 = "cyan100"
    CYAN_200 = "cyan200"
    CYAN_300 = "cyan300"
    CYAN_400 = "cyan400"
    CYAN_500 = "cyan500"
    CYAN_600 = "cyan600"
    CYAN_700 = "cyan700"
    CYAN_800 = "cyan800"
    CYAN_900 = "cyan900"
    TEAL = "teal"
    TEAL_50 = "teal50"
    TEAL_100 = "teal100"
    TEAL_200 = "teal200"
    TEAL_300 = "teal300"
    TEAL_400 = "teal400"
    TEAL_500 = "teal500"
    TEAL_600 = "teal600"
    TEAL_700 = "teal700"
    TEAL_800 = "teal800"
    TEAL_900 = "teal900"
    GREEN = "green"
    GREEN_50 = "green50"
    GREEN_100 = "green100"
    GREEN_200 = "green200"
    GREEN_300 = "green300"
    GREEN_400 = "green400"
    GREEN_500 = "green500"
    GREEN_600 = "green600"
    GREEN_700 = "green700"
    GREEN_800 = "green800"
    GREEN_900 = "green900"
    LIGHT_GREEN = "lightgreen"
    LIGHT_GREEN_50 = "lightgreen50"
    LIGHT_GREEN_100 = "lightgreen100"
    LIGHT_GREEN_200 = "lightgreen200"
    LIGHT_GREEN_300 = "lightgreen300"
    LIGHT_GREEN_400 = "lightgreen400"
    LIGHT_GREEN_500 = "lightgreen500"
    LIGHT_GREEN_600 = "lightgreen600"
    LIGHT_GREEN_700 = "lightgreen700"
    LIGHT_GREEN_800 = "lightgreen800"
    LIGHT_GREEN_900 = "lightgreen900"
    LIME = "lime"
    LIME_50 = "lime50"
    LIME_100 = "lime100"
    LIME_200 = "lime200"
    LIME_300 = "lime300"
    LIME_400 = "lime400"
    LIME_500 = "lime500"
    LIME_600 = "lime600"
    LIME_700 = "lime700"
    LIME_800 = "lime800"
    LIME_900 = "lime900"
    YELLOW = "yellow"
    YELLOW_50 = "yellow50"
    YELLOW_100 = "yellow100"
    YELLOW_200 = "yellow200"
    YELLOW_300 = "yellow300"
    YELLOW_400 = "yellow400"
    YELLOW_500 = "yellow500"
    YELLOW_600 = "yellow600"
    YELLOW_700 = "yellow700"
    YELLOW_800 = "yellow800"
    YELLOW_900 = "yellow900"
    AMBER = "amber"
    AMBER_50 = "amber50"
    AMBER_100 = "amber100"
    AMBER_200 = "amber200"
    AMBER_300 = "amber300"
    AMBER_400 = "amber400"
    AMBER_500 = "amber500"
    AMBER_600 = "amber600"
    AMBER_700 = "amber700"
    AMBER_800 = "amber800"
    AMBER_900 = "amber900"
    ORANGE = "orange"
    ORANGE_50 = "orange50"
    ORANGE_100 = "orange100"
    ORANGE_200 = "orange200"
    ORANGE_300 = "orange300"
    ORANGE_400 = "orange400"
    ORANGE_500 = "orange500"
    ORANGE_600 = "orange600"
    ORANGE_700 = "orange700"
    ORANGE_800 = "orange800"
    ORANGE_900 = "orange900"
    DEEP_ORANGE = "deeporange"
    DEEP_ORANGE_50 = "deeporange50"
    DEEP_ORANGE_100 = "deeporange100"
    DEEP_ORANGE_200 = "deeporange200"
    DEEP_ORANGE_300 = "deeporange300"
    DEEP_ORANGE_400 = "deeporange400"
    DEEP_ORANGE_500 = "deeporange500"
    DEEP_ORANGE_600 = "deeporange600"
    DEEP_ORANGE_700 = "deeporange700"
    DEEP_ORANGE_800 = "deeporange800"
    DEEP_ORANGE_900 = "deeporange900"
    BROWN = "brown"
    BROWN_50 = "brown50"
    BROWN_100 = "brown100"
    BROWN_200 = "brown200"
    BROWN_300 = "brown300"
    BROWN_400 = "brown400"
    BROWN_500 = "brown500"
    BROWN_600 = "brown600"
    BROWN_700 = "brown700"
    BROWN_800 = "brown800"
    BROWN_900 = "brown900"
    BLUE_GREY = "bluegrey"
    BLUE_GREY_50 = "bluegrey50"
    BLUE_GREY_100 = "bluegrey100"
    BLUE_GREY_200 = "bluegrey200"
    BLUE_GREY_300 = "bluegrey300"
    BLUE_GREY_400 = "bluegrey400"
    BLUE_GREY_500 = "bluegrey500"
    BLUE_GREY_600 = "bluegrey600"
    BLUE_GREY_700 = "bluegrey700"
    BLUE_GREY_800 = "bluegrey800"
    BLUE_GREY_900 = "bluegrey900"
    RED_ACCENT = "redaccent"
    RED_ACCENT_100 = "redaccent100"
    RED_ACCENT_200 = "redaccent200"
    RED_ACCENT_400 = "redaccent400"
    RED_ACCENT_700 = "redaccent700"
    PINK_ACCENT = "pinkaccent"
    PINK_ACCENT_100 = "pinkaccent100"
    PINK_ACCENT_200 = "pinkaccent200"
    PINK_ACCENT_400 = "pinkaccent400"
    PINK_ACCENT_700 = "pinkaccent700"
    PURPLE_ACCENT = "purpleaccent"
    PURPLE_ACCENT_100 = "purpleaccent100"
    PURPLE_ACCENT_200 = "purpleaccent200"
    PURPLE_ACCENT_400 = "purpleaccent400"
    PURPLE_ACCENT_700 = "purpleaccent700"
    DEEP_PURPLE_ACCENT = "deeppurpleaccent"
    DEEP_PURPLE_ACCENT_100 = "deeppurpleaccent100"
    DEEP_PURPLE_ACCENT_200 = "deeppurpleaccent200"
    DEEP_PURPLE_ACCENT_400 = "deeppurpleaccent400"
    DEEP_PURPLE_ACCENT_700 = "deeppurpleaccent700"
    INDIGO_ACCENT = "indigoaccent"
    INDIGO_ACCENT_100 = "indigoaccent100"
    INDIGO_ACCENT_200 = "indigoaccent200"
    INDIGO_ACCENT_400 = "indigoaccent400"
    INDIGO_ACCENT_700 = "indigoaccent700"
    BLUE_ACCENT = "blueaccent"
    BLUE_ACCENT_100 = "blueaccent100"
    BLUE_ACCENT_200 = "blueaccent200"
    BLUE_ACCENT_400 = "blueaccent400"
    BLUE_ACCENT_700 = "blueaccent700"
    LIGHT_BLUE_ACCENT = "lightblueaccent"
    LIGHT_BLUE_ACCENT_100 = "lightblueaccent100"
    LIGHT_BLUE_ACCENT_200 = "lightblueaccent200"
    LIGHT_BLUE_ACCENT_400 = "lightblueaccent400"
    LIGHT_BLUE_ACCENT_700 = "lightblueaccent700"
    CYAN_ACCENT = "cyanaccent"
    CYAN_ACCENT_100 = "cyanaccent100"
    CYAN_ACCENT_200 = "cyanaccent200"
    CYAN_ACCENT_400 = "cyanaccent400"
    CYAN_ACCENT_700 = "cyanaccent700"
    TEAL_ACCENT = "tealaccent"
    TEAL_ACCENT_100 = "tealaccent100"
    TEAL_ACCENT_200 = "tealaccent200"
    TEAL_ACCENT_400 = "tealaccent400"
    TEAL_ACCENT_700 = "tealaccent700"
    GREEN_ACCENT = "greenaccent"
    GREEN_ACCENT_100 = "greenaccent100"
    GREEN_ACCENT_200 = "greenaccent200"
    GREEN_ACCENT_400 = "greenaccent400"
    GREEN_ACCENT_700 = "greenaccent700"
    LIGHT_GREEN_ACCENT = "lightgreenaccent"
    LIGHT_GREEN_ACCENT_100 = "lightgreenaccent100"
    LIGHT_GREEN_ACCENT_200 = "lightgreenaccent200"
    LIGHT_GREEN_ACCENT_400 = "lightgreenaccent400"
    LIGHT_GREEN_ACCENT_700 = "lightgreenaccent700"
    LIME_ACCENT = "limeaccent"
    LIME_ACCENT_100 = "limeaccent100"
    LIME_ACCENT_200 = "limeaccent200"
    LIME_ACCENT_400 = "limeaccent400"
    LIME_ACCENT_700 = "limeaccent700"
    YELLOW_ACCENT = "yellowaccent"
    YELLOW_ACCENT_100 = "yellowaccent100"
    YELLOW_ACCENT_200 = "yellowaccent200"
    YELLOW_ACCENT_400 = "yellowaccent400"
    YELLOW_ACCENT_700 = "yellowaccent700"
    AMBER_ACCENT = "amberaccent"
    AMBER_ACCENT_100 = "amberaccent100"
    AMBER_ACCENT_200 = "amberaccent200"
    AMBER_ACCENT_400 = "amberaccent400"
    AMBER_ACCENT_700 = "amberaccent700"
    ORANGE_ACCENT = "orangeaccent"
    ORANGE_ACCENT_100 = "orangeaccent100"
    ORANGE_ACCENT_200 = "orangeaccent200"
    ORANGE_ACCENT_400 = "orangeaccent400"
    ORANGE_ACCENT_700 = "orangeaccent700"
    DEEP_ORANGE_ACCENT = "deeporangeaccent"
    DEEP_ORANGE_ACCENT_100 = "deeporangeaccent100"
    DEEP_ORANGE_ACCENT_200 = "deeporangeaccent200"
    DEEP_ORANGE_ACCENT_400 = "deeporangeaccent400"
    DEEP_ORANGE_ACCENT_700 = "deeporangeaccent700"
    GREY = "grey"
    GREY_50 = "grey50"
    GREY_100 = "grey100"
    GREY_200 = "grey200"
    GREY_300 = "grey300"
    GREY_400 = "grey400"
    GREY_500 = "grey500"
    GREY_600 = "grey600"
    GREY_700 = "grey700"
    GREY_800 = "grey800"
    GREY_900 = "grey900"


class Colors(str, Enum):
    def with_opacity(self, opacity: Union[int, float]) -> str:
        """
        Returns the color with the specified opacity.

        Args:
            opacity: The opacity value, which must be between 0 and 1.

        Returns:
            A string representing the color value with the specified opacity appended.

        Raises:
            AssertionError: If the opacity is not between 0 and 1 (inclusive).
        """
        assert 0 <= opacity <= 1, "opacity must be between 0 and 1"
        return f"{self.value},{opacity}"

    @staticmethod
    def random(
        exclude: Optional[List["Colors"]] = None,
        weights: Optional[Dict["Colors", int]] = None,
    ) -> Optional["Colors"]:
        """
        Selects a random color, with optional exclusions and weights.

        Args:
            exclude: A list of colors members to exclude from the selection.
            weights: A dictionary mapping color members to their respective weights for weighted random selection.

        Returns:
            A randomly selected color, or None if all members are excluded.
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

    PRIMARY = "primary"
    ON_PRIMARY = "onprimary"
    PRIMARY_CONTAINER = "primarycontainer"
    ON_PRIMARY_CONTAINER = "onprimarycontainer"
    SECONDARY = "secondary"
    ON_SECONDARY = "onsecondary"
    SECONDARY_CONTAINER = "secondarycontainer"
    ON_SECONDARY_CONTAINER = "onsecondarycontainer"
    TERTIARY = "tertiary"
    ON_TERTIARY = "ontertiary"
    TERTIARY_CONTAINER = "tertiarycontainer"
    ON_TERTIARY_CONTAINER = "ontertiarycontainer"
    ERROR = "error"
    ON_ERROR = "onerror"
    ERROR_CONTAINER = "errorcontainer"
    ON_ERROR_CONTAINER = "onerrorcontainer"
    OUTLINE = "outline"
    OUTLINE_VARIANT = "outlinevariant"
    SURFACE = "surface"  # previously BACKGROUND
    ON_SURFACE = "onsurface"  # previously ON_BACKGROUND
    SURFACE_TINT = "surfacetint"
    SURFACE_CONTAINER_HIGHEST = "surfaceContainerHighest"  # previously SURFACE_VARIANT
    ON_SURFACE_VARIANT = "onsurfacevariant"
    INVERSE_SURFACE = "inversesurface"
    ON_INVERSE_SURFACE = "oninversesurface"
    INVERSE_PRIMARY = "inverseprimary"
    SHADOW = "shadow"
    SCRIM = "scrim"

    WHITE10 = "white10"
    WHITE12 = "white12"
    WHITE24 = "white24"
    WHITE30 = "white30"
    WHITE38 = "white38"
    WHITE54 = "white54"
    WHITE60 = "white60"
    WHITE70 = "white70"
    WHITE = "white"
    TRANSPARENT = "transparent"
    BLACK12 = "black12"
    BLACK26 = "black26"
    BLACK38 = "black38"
    BLACK45 = "black45"
    BLACK54 = "black54"
    BLACK87 = "black87"
    BLACK = "black"
    RED = "red"
    RED_50 = "red50"
    RED_100 = "red100"
    RED_200 = "red200"
    RED_300 = "red300"
    RED_400 = "red400"
    RED_500 = "red500"
    RED_600 = "red600"
    RED_700 = "red700"
    RED_800 = "red800"
    RED_900 = "red900"
    PINK = "pink"
    PINK_50 = "pink50"
    PINK_100 = "pink100"
    PINK_200 = "pink200"
    PINK_300 = "pink300"
    PINK_400 = "pink400"
    PINK_500 = "pink500"
    PINK_600 = "pink600"
    PINK_700 = "pink700"
    PINK_800 = "pink800"
    PINK_900 = "pink900"
    PURPLE = "purple"
    PURPLE_50 = "purple50"
    PURPLE_100 = "purple100"
    PURPLE_200 = "purple200"
    PURPLE_300 = "purple300"
    PURPLE_400 = "purple400"
    PURPLE_500 = "purple500"
    PURPLE_600 = "purple600"
    PURPLE_700 = "purple700"
    PURPLE_800 = "purple800"
    PURPLE_900 = "purple900"
    DEEP_PURPLE = "deeppurple"
    DEEP_PURPLE_50 = "deeppurple50"
    DEEP_PURPLE_100 = "deeppurple100"
    DEEP_PURPLE_200 = "deeppurple200"
    DEEP_PURPLE_300 = "deeppurple300"
    DEEP_PURPLE_400 = "deeppurple400"
    DEEP_PURPLE_500 = "deeppurple500"
    DEEP_PURPLE_600 = "deeppurple600"
    DEEP_PURPLE_700 = "deeppurple700"
    DEEP_PURPLE_800 = "deeppurple800"
    DEEP_PURPLE_900 = "deeppurple900"
    INDIGO = "indigo"
    INDIGO_50 = "indigo50"
    INDIGO_100 = "indigo100"
    INDIGO_200 = "indigo200"
    INDIGO_300 = "indigo300"
    INDIGO_400 = "indigo400"
    INDIGO_500 = "indigo500"
    INDIGO_600 = "indigo600"
    INDIGO_700 = "indigo700"
    INDIGO_800 = "indigo800"
    INDIGO_900 = "indigo900"
    BLUE = "blue"
    BLUE_50 = "blue50"
    BLUE_100 = "blue100"
    BLUE_200 = "blue200"
    BLUE_300 = "blue300"
    BLUE_400 = "blue400"
    BLUE_500 = "blue500"
    BLUE_600 = "blue600"
    BLUE_700 = "blue700"
    BLUE_800 = "blue800"
    BLUE_900 = "blue900"
    LIGHT_BLUE = "lightblue"
    LIGHT_BLUE_50 = "lightblue50"
    LIGHT_BLUE_100 = "lightblue100"
    LIGHT_BLUE_200 = "lightblue200"
    LIGHT_BLUE_300 = "lightblue300"
    LIGHT_BLUE_400 = "lightblue400"
    LIGHT_BLUE_500 = "lightblue500"
    LIGHT_BLUE_600 = "lightblue600"
    LIGHT_BLUE_700 = "lightblue700"
    LIGHT_BLUE_800 = "lightblue800"
    LIGHT_BLUE_900 = "lightblue900"
    CYAN = "cyan"
    CYAN_50 = "cyan50"
    CYAN_100 = "cyan100"
    CYAN_200 = "cyan200"
    CYAN_300 = "cyan300"
    CYAN_400 = "cyan400"
    CYAN_500 = "cyan500"
    CYAN_600 = "cyan600"
    CYAN_700 = "cyan700"
    CYAN_800 = "cyan800"
    CYAN_900 = "cyan900"
    TEAL = "teal"
    TEAL_50 = "teal50"
    TEAL_100 = "teal100"
    TEAL_200 = "teal200"
    TEAL_300 = "teal300"
    TEAL_400 = "teal400"
    TEAL_500 = "teal500"
    TEAL_600 = "teal600"
    TEAL_700 = "teal700"
    TEAL_800 = "teal800"
    TEAL_900 = "teal900"
    GREEN = "green"
    GREEN_50 = "green50"
    GREEN_100 = "green100"
    GREEN_200 = "green200"
    GREEN_300 = "green300"
    GREEN_400 = "green400"
    GREEN_500 = "green500"
    GREEN_600 = "green600"
    GREEN_700 = "green700"
    GREEN_800 = "green800"
    GREEN_900 = "green900"
    LIGHT_GREEN = "lightgreen"
    LIGHT_GREEN_50 = "lightgreen50"
    LIGHT_GREEN_100 = "lightgreen100"
    LIGHT_GREEN_200 = "lightgreen200"
    LIGHT_GREEN_300 = "lightgreen300"
    LIGHT_GREEN_400 = "lightgreen400"
    LIGHT_GREEN_500 = "lightgreen500"
    LIGHT_GREEN_600 = "lightgreen600"
    LIGHT_GREEN_700 = "lightgreen700"
    LIGHT_GREEN_800 = "lightgreen800"
    LIGHT_GREEN_900 = "lightgreen900"
    LIME = "lime"
    LIME_50 = "lime50"
    LIME_100 = "lime100"
    LIME_200 = "lime200"
    LIME_300 = "lime300"
    LIME_400 = "lime400"
    LIME_500 = "lime500"
    LIME_600 = "lime600"
    LIME_700 = "lime700"
    LIME_800 = "lime800"
    LIME_900 = "lime900"
    YELLOW = "yellow"
    YELLOW_50 = "yellow50"
    YELLOW_100 = "yellow100"
    YELLOW_200 = "yellow200"
    YELLOW_300 = "yellow300"
    YELLOW_400 = "yellow400"
    YELLOW_500 = "yellow500"
    YELLOW_600 = "yellow600"
    YELLOW_700 = "yellow700"
    YELLOW_800 = "yellow800"
    YELLOW_900 = "yellow900"
    AMBER = "amber"
    AMBER_50 = "amber50"
    AMBER_100 = "amber100"
    AMBER_200 = "amber200"
    AMBER_300 = "amber300"
    AMBER_400 = "amber400"
    AMBER_500 = "amber500"
    AMBER_600 = "amber600"
    AMBER_700 = "amber700"
    AMBER_800 = "amber800"
    AMBER_900 = "amber900"
    ORANGE = "orange"
    ORANGE_50 = "orange50"
    ORANGE_100 = "orange100"
    ORANGE_200 = "orange200"
    ORANGE_300 = "orange300"
    ORANGE_400 = "orange400"
    ORANGE_500 = "orange500"
    ORANGE_600 = "orange600"
    ORANGE_700 = "orange700"
    ORANGE_800 = "orange800"
    ORANGE_900 = "orange900"
    DEEP_ORANGE = "deeporange"
    DEEP_ORANGE_50 = "deeporange50"
    DEEP_ORANGE_100 = "deeporange100"
    DEEP_ORANGE_200 = "deeporange200"
    DEEP_ORANGE_300 = "deeporange300"
    DEEP_ORANGE_400 = "deeporange400"
    DEEP_ORANGE_500 = "deeporange500"
    DEEP_ORANGE_600 = "deeporange600"
    DEEP_ORANGE_700 = "deeporange700"
    DEEP_ORANGE_800 = "deeporange800"
    DEEP_ORANGE_900 = "deeporange900"
    BROWN = "brown"
    BROWN_50 = "brown50"
    BROWN_100 = "brown100"
    BROWN_200 = "brown200"
    BROWN_300 = "brown300"
    BROWN_400 = "brown400"
    BROWN_500 = "brown500"
    BROWN_600 = "brown600"
    BROWN_700 = "brown700"
    BROWN_800 = "brown800"
    BROWN_900 = "brown900"
    BLUE_GREY = "bluegrey"
    BLUE_GREY_50 = "bluegrey50"
    BLUE_GREY_100 = "bluegrey100"
    BLUE_GREY_200 = "bluegrey200"
    BLUE_GREY_300 = "bluegrey300"
    BLUE_GREY_400 = "bluegrey400"
    BLUE_GREY_500 = "bluegrey500"
    BLUE_GREY_600 = "bluegrey600"
    BLUE_GREY_700 = "bluegrey700"
    BLUE_GREY_800 = "bluegrey800"
    BLUE_GREY_900 = "bluegrey900"
    RED_ACCENT = "redaccent"
    RED_ACCENT_100 = "redaccent100"
    RED_ACCENT_200 = "redaccent200"
    RED_ACCENT_400 = "redaccent400"
    RED_ACCENT_700 = "redaccent700"
    PINK_ACCENT = "pinkaccent"
    PINK_ACCENT_100 = "pinkaccent100"
    PINK_ACCENT_200 = "pinkaccent200"
    PINK_ACCENT_400 = "pinkaccent400"
    PINK_ACCENT_700 = "pinkaccent700"
    PURPLE_ACCENT = "purpleaccent"
    PURPLE_ACCENT_100 = "purpleaccent100"
    PURPLE_ACCENT_200 = "purpleaccent200"
    PURPLE_ACCENT_400 = "purpleaccent400"
    PURPLE_ACCENT_700 = "purpleaccent700"
    DEEP_PURPLE_ACCENT = "deeppurpleaccent"
    DEEP_PURPLE_ACCENT_100 = "deeppurpleaccent100"
    DEEP_PURPLE_ACCENT_200 = "deeppurpleaccent200"
    DEEP_PURPLE_ACCENT_400 = "deeppurpleaccent400"
    DEEP_PURPLE_ACCENT_700 = "deeppurpleaccent700"
    INDIGO_ACCENT = "indigoaccent"
    INDIGO_ACCENT_100 = "indigoaccent100"
    INDIGO_ACCENT_200 = "indigoaccent200"
    INDIGO_ACCENT_400 = "indigoaccent400"
    INDIGO_ACCENT_700 = "indigoaccent700"
    BLUE_ACCENT = "blueaccent"
    BLUE_ACCENT_100 = "blueaccent100"
    BLUE_ACCENT_200 = "blueaccent200"
    BLUE_ACCENT_400 = "blueaccent400"
    BLUE_ACCENT_700 = "blueaccent700"
    LIGHT_BLUE_ACCENT = "lightblueaccent"
    LIGHT_BLUE_ACCENT_100 = "lightblueaccent100"
    LIGHT_BLUE_ACCENT_200 = "lightblueaccent200"
    LIGHT_BLUE_ACCENT_400 = "lightblueaccent400"
    LIGHT_BLUE_ACCENT_700 = "lightblueaccent700"
    CYAN_ACCENT = "cyanaccent"
    CYAN_ACCENT_100 = "cyanaccent100"
    CYAN_ACCENT_200 = "cyanaccent200"
    CYAN_ACCENT_400 = "cyanaccent400"
    CYAN_ACCENT_700 = "cyanaccent700"
    TEAL_ACCENT = "tealaccent"
    TEAL_ACCENT_100 = "tealaccent100"
    TEAL_ACCENT_200 = "tealaccent200"
    TEAL_ACCENT_400 = "tealaccent400"
    TEAL_ACCENT_700 = "tealaccent700"
    GREEN_ACCENT = "greenaccent"
    GREEN_ACCENT_100 = "greenaccent100"
    GREEN_ACCENT_200 = "greenaccent200"
    GREEN_ACCENT_400 = "greenaccent400"
    GREEN_ACCENT_700 = "greenaccent700"
    LIGHT_GREEN_ACCENT = "lightgreenaccent"
    LIGHT_GREEN_ACCENT_100 = "lightgreenaccent100"
    LIGHT_GREEN_ACCENT_200 = "lightgreenaccent200"
    LIGHT_GREEN_ACCENT_400 = "lightgreenaccent400"
    LIGHT_GREEN_ACCENT_700 = "lightgreenaccent700"
    LIME_ACCENT = "limeaccent"
    LIME_ACCENT_100 = "limeaccent100"
    LIME_ACCENT_200 = "limeaccent200"
    LIME_ACCENT_400 = "limeaccent400"
    LIME_ACCENT_700 = "limeaccent700"
    YELLOW_ACCENT = "yellowaccent"
    YELLOW_ACCENT_100 = "yellowaccent100"
    YELLOW_ACCENT_200 = "yellowaccent200"
    YELLOW_ACCENT_400 = "yellowaccent400"
    YELLOW_ACCENT_700 = "yellowaccent700"
    AMBER_ACCENT = "amberaccent"
    AMBER_ACCENT_100 = "amberaccent100"
    AMBER_ACCENT_200 = "amberaccent200"
    AMBER_ACCENT_400 = "amberaccent400"
    AMBER_ACCENT_700 = "amberaccent700"
    ORANGE_ACCENT = "orangeaccent"
    ORANGE_ACCENT_100 = "orangeaccent100"
    ORANGE_ACCENT_200 = "orangeaccent200"
    ORANGE_ACCENT_400 = "orangeaccent400"
    ORANGE_ACCENT_700 = "orangeaccent700"
    DEEP_ORANGE_ACCENT = "deeporangeaccent"
    DEEP_ORANGE_ACCENT_100 = "deeporangeaccent100"
    DEEP_ORANGE_ACCENT_200 = "deeporangeaccent200"
    DEEP_ORANGE_ACCENT_400 = "deeporangeaccent400"
    DEEP_ORANGE_ACCENT_700 = "deeporangeaccent700"
    GREY = "grey"
    GREY_50 = "grey50"
    GREY_100 = "grey100"
    GREY_200 = "grey200"
    GREY_300 = "grey300"
    GREY_400 = "grey400"
    GREY_500 = "grey500"
    GREY_600 = "grey600"
    GREY_700 = "grey700"
    GREY_800 = "grey800"
    GREY_900 = "grey900"
