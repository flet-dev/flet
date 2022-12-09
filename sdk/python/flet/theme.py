import dataclasses
from dataclasses import field
from typing import Optional, Union
from enum import Enum

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
    ADAPTIVE_PLATFORM_DENSITY = "adaptivePlatformDensity"


PageTransitionString = Literal["fadeUpwards", "openUpwards", "zoom", "cupertino"]


class PageTransitionTheme(Enum):
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"


@dataclasses.dataclass
class PageTransitionsTheme:
    android: Union[PageTransitionTheme, PageTransitionString, None] = field(default=None)
    ios: Union[PageTransitionTheme, PageTransitionString, None] = field(default=None)
    linux: Union[PageTransitionTheme, PageTransitionString, None] = field(default=None)
    macos: Union[PageTransitionTheme, PageTransitionString, None] = field(default=None)
    windows: Union[PageTransitionTheme, PageTransitionString, None] = field(default=None)


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: bool = field(default=True)
    visual_density: Union[ThemeVisualDensity, VisualDensityString] = field(default=ThemeVisualDensity.STANDARD)
    page_transitions: Union[PageTransitionsTheme, PageTransitionString] = field(default_factory=PageTransitionsTheme)
