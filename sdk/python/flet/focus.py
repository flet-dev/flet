import dataclasses
import time
from typing import Optional


@dataclasses.dataclass
class FocusData:
    ts: str = dataclasses.field(default=str(time.time()))
    d: Optional[str] = dataclasses.field(default=True)
