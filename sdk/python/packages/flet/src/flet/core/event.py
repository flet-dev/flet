from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    target: int
    name: str
    data: Optional[str]
