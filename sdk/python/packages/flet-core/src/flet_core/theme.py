import dataclasses
from dataclasses import field
from enum import Enum
from typing import Optional

from flet_core.types import ThemeMode

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

VisualDensityString = Literal[
    None, "standard", "compact", "comfortable", "adaptivePlatformDensity"
]


class ThemeVisualDensity(Enum):
    NONE = None
    STANDARD = "standard"
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    ADAPTIVEPLATFORMDENSITY = "adaptivePlatformDensity"


PageTransitionString = Literal["fadeUpwards", "openUpwards", "zoom", "cupertino"]


class PageTransitionTheme(Enum):
    NONE = "none"
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"


@dataclasses.dataclass
class PageTransitionsTheme:
    android: Optional[PageTransitionTheme] = field(default=None)
    ios: Optional[PageTransitionTheme] = field(default=None)
    linux: Optional[PageTransitionTheme] = field(default=None)
    macos: Optional[PageTransitionTheme] = field(default=None)
    windows: Optional[PageTransitionTheme] = field(default=None)


@dataclasses.dataclass
class ColorScheme:
    primary: Optional[str] = field(default=None)
    on_primary: Optional[str] = field(default=None)
    primary_container: Optional[str] = field(default=None)
    on_primary_container: Optional[str] = field(default=None)
    secondary: Optional[str] = field(default=None)
    on_secondary: Optional[str] = field(default=None)
    secondary_container: Optional[str] = field(default=None)
    on_secondary_container: Optional[str] = field(default=None)
    tertiary: Optional[str] = field(default=None)
    on_tertiary: Optional[str] = field(default=None)
    tertiary_container: Optional[str] = field(default=None)
    on_tertiary_container: Optional[str] = field(default=None)
    error: Optional[str] = field(default=None)
    on_error: Optional[str] = field(default=None)
    error_container: Optional[str] = field(default=None)
    on_error_container: Optional[str] = field(default=None)
    background: Optional[str] = field(default=None)
    on_background: Optional[str] = field(default=None)
    surface: Optional[str] = field(default=None)
    on_surface: Optional[str] = field(default=None)
    surface_variant: Optional[str] = field(default=None)
    on_surface_variant: Optional[str] = field(default=None)
    outline: Optional[str] = field(default=None)
    outline_variant: Optional[str] = field(default=None)
    shadow: Optional[str] = field(default=None)
    scrim: Optional[str] = field(default=None)
    inverse_surface: Optional[str] = field(default=None)
    on_inverse_surface: Optional[str] = field(default=None)
    inverse_primary: Optional[str] = field(default=None)
    surface_tint: Optional[str] = field(default=None)


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    primary_swatch: Optional[str] = field(default=None)
    color_scheme: Optional[ColorScheme] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: Optional[bool] = field(default=None)
    visual_density: ThemeVisualDensity = field(default=ThemeVisualDensity.STANDARD)
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
