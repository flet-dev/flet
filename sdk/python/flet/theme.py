import dataclasses
from dataclasses import field
from typing import Optional

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

VisualDensity = Literal[
    None, "standard", "compact", "comfortable", "adaptivePlatformDensity"
]

PageTransition = Literal["fadeUpwards", "openUpwards", "zoom", "cupertino"]


@dataclasses.dataclass
class PageTransitionsTheme:
    android: Optional[PageTransition] = field(default=None)
    ios: Optional[PageTransition] = field(default=None)
    linux: Optional[PageTransition] = field(default=None)
    macos: Optional[PageTransition] = field(default=None)
    windows: Optional[PageTransition] = field(default=None)


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    font_family: Optional[str] = field(default=None)
    use_material3: bool = field(default=True)
    visual_density: VisualDensity = field(default="standard")
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
