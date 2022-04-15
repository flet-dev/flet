import dataclasses
from dataclasses import field

from beartype._decor.main import beartype

try:
    from typing import Literal
except:
    from typing_extensions import Literal


@beartype
@dataclasses.dataclass
class Theme:
    color_scheme_seed: str = field(default=None)
    brightness: Literal[None, "dark", "light"] = field(default="light")
    use_material3: bool = field(default=False)
