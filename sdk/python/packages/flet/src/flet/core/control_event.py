from dataclasses import dataclass
from typing import TYPE_CHECKING

from flet.core.event import Event

if TYPE_CHECKING:
    from .control import Control
    from .page import Page


@dataclass
class ControlEvent(Event):
    control: "Control"
    page: "Page"
