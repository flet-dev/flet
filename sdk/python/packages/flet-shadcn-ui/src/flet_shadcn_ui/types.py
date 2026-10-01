from enum import Enum

__all__ = [
    "AlertVariant",
    "BadgeVariant",
    "ButtonSize",
    "ButtonVariant",
    "ColorScheme",
]


class ColorScheme(Enum):
    """
    Built-in Shadcn color schemes.

    Each scheme has a light and a dark variant; the variant is picked from
    :attr:`flet_shadcn_ui.Theme.brightness` or the page theme.
    """

    BLUE = "blue"
    """Blue color scheme."""

    GRAY = "gray"
    """Gray color scheme."""

    GREEN = "green"
    """Green color scheme."""

    NEUTRAL = "neutral"
    """Neutral color scheme."""

    ORANGE = "orange"
    """Orange color scheme."""

    RED = "red"
    """Red color scheme."""

    ROSE = "rose"
    """Rose color scheme."""

    SLATE = "slate"
    """Slate color scheme. This is the default."""

    STONE = "stone"
    """Stone color scheme."""

    VIOLET = "violet"
    """Violet color scheme."""

    YELLOW = "yellow"
    """Yellow color scheme."""

    ZINC = "zinc"
    """Zinc color scheme."""


class ButtonVariant(Enum):
    """
    Visual variants of a :class:`~flet_shadcn_ui.Button`.
    """

    PRIMARY = "primary"
    """Solid button using the primary color. This is the default."""

    DESTRUCTIVE = "destructive"
    """Solid button for dangerous or irreversible actions."""

    OUTLINE = "outline"
    """Transparent button with a border."""

    SECONDARY = "secondary"
    """Solid button using the secondary color."""

    GHOST = "ghost"
    """Transparent button without a border that shows a background on hover."""

    LINK = "link"
    """Text-only button that is underlined on hover."""


class ButtonSize(Enum):
    """
    Sizes of a :class:`~flet_shadcn_ui.Button`.
    """

    REGULAR = "regular"
    """Regular size. This is the default."""

    SM = "sm"
    """Small size."""

    LG = "lg"
    """Large size."""


class AlertVariant(Enum):
    """
    Visual variants of an :class:`~flet_shadcn_ui.Alert`.
    """

    PRIMARY = "primary"
    """Neutral alert. This is the default."""

    DESTRUCTIVE = "destructive"
    """Alert for errors and other destructive situations."""


class BadgeVariant(Enum):
    """
    Visual variants of a :class:`~flet_shadcn_ui.Badge`.
    """

    PRIMARY = "primary"
    """Solid badge using the primary color. This is the default."""

    SECONDARY = "secondary"
    """Solid badge using the secondary color."""

    OUTLINE = "outline"
    """Transparent badge with a border."""

    DESTRUCTIVE = "destructive"
    """Solid badge for errors and other destructive states."""
