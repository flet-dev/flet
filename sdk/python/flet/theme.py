import dataclasses
from dataclasses import field
from typing import Optional

try:
    from typing import Literal
except:
    from typing_extensions import Literal

VisualDensity = Literal[
    None, "standard", "compact", "comfortable", "adaptivePlatformDensity"
]


@dataclasses.dataclass
class Theme:
    color_scheme_seed: Optional[str] = field(default=None)
    brightness: Literal[None, "dark", "light"] = field(default="light")
    font_family: Optional[str] = field(default=None)
    use_material3: bool = field(default=True)
    visual_density: VisualDensity = field(default="standard")
