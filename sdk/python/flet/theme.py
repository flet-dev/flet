import dataclasses
from dataclasses import field

try:
    from typing import Literal
except:
    from typing_extensions import Literal


@dataclasses.dataclass
class Theme:
    color_scheme_seed: str = field(default=None)
    brightness: Literal[None, "dark", "light"] = field(default="light")
    font_family: str = field(default=None)
    use_material3: bool = field(default=False)
