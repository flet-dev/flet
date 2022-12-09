import dataclasses
from dataclasses import field
from typing import Optional, Union

from flet.types import FontWeight, FontWeightString


@dataclasses.dataclass
class TextStyle:
    size: Union[None, int, float] = field(default=None)
    weight: Union[FontWeight, FontWeightString] = field(default=None)
    italic: Optional[bool] = field(default=None)
    font_family: Optional[str] = field(default=None)
    color: Optional[str] = field(default=None)
    bgcolor: Optional[str] = field(default=None)
