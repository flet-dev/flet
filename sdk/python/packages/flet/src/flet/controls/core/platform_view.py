from dataclasses import dataclass
from typing import Any

__all__ = ["PlatformView"]


@dataclass
class PlatformView:
    view_id: int
    initial_data: Any
