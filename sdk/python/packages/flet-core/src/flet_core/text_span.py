import dataclasses
from typing import List, Optional

from flet_core.text_style import TextStyle


@dataclasses.dataclass
class TextSpan:
    text: str
    style: Optional[TextStyle] = dataclasses.field(default=None)
    spans: Optional[List["TextSpan"]] = dataclasses.field(default=None)
