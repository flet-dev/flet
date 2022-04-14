from dataclasses import MISSING, dataclass, field
from typing import Dict, List, Literal, Optional

from beartype._decor.main import beartype


@beartype
@dataclass
class Theme:
    color_scheme_seed: str = field(default=None)
    brightness: Literal[None, "dark", "light"] = field(default="light")
    use_material3: bool = field(default=False)
