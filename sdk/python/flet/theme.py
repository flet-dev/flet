import dataclasses
from dataclasses import field
from typing import Optional
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
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: bool = field(default=True)
    visual_density: ThemeVisualDensity = field(default=ThemeVisualDensity.STANDARD)
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
