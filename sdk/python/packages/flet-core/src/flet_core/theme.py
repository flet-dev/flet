import dataclasses
from dataclasses import field
from enum import Enum, EnumMeta
from typing import Dict, Optional, Union
from warnings import warn

from flet_core.border import BorderSide
from flet_core.border_radius import BorderRadius
from flet_core.text_style import TextStyle
from flet_core.types import MaterialState, PaddingValue, Brightness

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

VisualDensityString = Literal[
    None, "standard", "compact", "comfortable", "adaptivePlatformDensity"
]


class ThemeVisualDensityDeprecated(EnumMeta):
    def __getattribute__(self, item):
        if item == "ADAPTIVEPLATFORMDENSITY":
            warn(
                "ADAPTIVEPLATFORMDENSITY is deprecated, use ADAPTIVE_PLATFORM_DENSITY instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        return EnumMeta.__getattribute__(self, item)


class ThemeVisualDensity(Enum, metaclass=ThemeVisualDensityDeprecated):
    NONE = None
    STANDARD = "standard"
    COMPACT = "compact"
    COMFORTABLE = "comfortable"
    ADAPTIVEPLATFORMDENSITY = "adaptivePlatformDensity"
    ADAPTIVE_PLATFORM_DENSITY = "adaptivePlatformDensity"


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
class TextTheme:
    body_large: Optional[TextStyle] = field(default=None)
    body_medium: Optional[TextStyle] = field(default=None)
    body_small: Optional[TextStyle] = field(default=None)
    display_large: Optional[TextStyle] = field(default=None)
    display_medium: Optional[TextStyle] = field(default=None)
    display_small: Optional[TextStyle] = field(default=None)
    headline_large: Optional[TextStyle] = field(default=None)
    headline_medium: Optional[TextStyle] = field(default=None)
    headline_small: Optional[TextStyle] = field(default=None)
    label_large: Optional[TextStyle] = field(default=None)
    label_medium: Optional[TextStyle] = field(default=None)
    label_small: Optional[TextStyle] = field(default=None)
    title_large: Optional[TextStyle] = field(default=None)
    title_medium: Optional[TextStyle] = field(default=None)
    title_small: Optional[TextStyle] = field(default=None)


@dataclasses.dataclass
class ScrollbarTheme:
    thumb_visibility: Union[None, bool, Dict[MaterialState, bool]] = field(default=None)
    thickness: Union[None, float, Dict[MaterialState, float]] = field(default=None)
    track_visibility: Union[None, bool, Dict[MaterialState, bool]] = field(default=None)
    radius: Optional[float] = field(default=None)
    thumb_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    track_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    track_border_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)
    cross_axis_margin: Optional[float] = field(default=None)
    main_axis_margin: Optional[float] = field(default=None)
    min_thumb_length: Optional[float] = field(default=None)
    interactive: Optional[bool] = field(default=None)


@dataclasses.dataclass
class TabsTheme:
    divider_color: Optional[str] = field(default=None)
    indicator_border_radius: Optional[BorderRadius] = field(default=None)
    indicator_border_side: Optional[BorderSide] = field(default=None)
    indicator_padding: PaddingValue = field(default=None)
    indicator_color: Optional[str] = field(default=None)
    indicator_tab_size: Optional[bool] = field(default=None)
    label_color: Optional[str] = field(default=None)
    unselected_label_color: Optional[str] = field(default=None)
    overlay_color: Union[None, str, Dict[MaterialState, str]] = field(default=None)


@dataclasses.dataclass
class SystemOverlayStyle:
    status_bar_color: Optional[str] = field(default=None)
    system_navigation_bar_color: Optional[str] = field(default=None)
    system_navigation_bar_divider_color: Optional[str] = field(default=None)
    enforce_system_navigation_bar_contrast: Optional[bool] = field(default=None)
    enforce_system_status_bar_contrast: Optional[bool] = field(default=None)
    system_navigation_bar_icon_brightness: Optional[Brightness] = field(default=None)
    status_bar_brightness: Optional[Brightness] = field(default=None)
    status_bar_icon_brightness: Optional[Brightness] = field(default=None)


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    primary_swatch: Optional[str] = field(default=None)
    color_scheme: Optional[ColorScheme] = field(default=None)
    text_theme: Optional[TextTheme] = field(default=None)
    primary_text_theme: Optional[TextTheme] = field(default=None)
    scrollbar_theme: Optional[ScrollbarTheme] = field(default=None)
    tabs_theme: Optional[TabsTheme] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: Optional[bool] = field(default=None)
    visual_density: ThemeVisualDensity = field(default=ThemeVisualDensity.STANDARD)
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
    system_overlay_style: SystemOverlayStyle = field(default_factory=SystemOverlayStyle)
