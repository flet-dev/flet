import dataclasses
from dataclasses import field
from typing import List, Optional, Union

from flet_core.shadow import BoxShadow
from flet_core.types import FontWeight


@dataclasses.dataclass
class TextStyle:
    size: Union[None, int, float] = field(default=None)
    weight: Optional[FontWeight] = field(default=None)
    italic: Optional[bool] = field(default=None)
    font_family: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
    shadow: Union[None, BoxShadow, List[BoxShadow]] = field(default=None)
