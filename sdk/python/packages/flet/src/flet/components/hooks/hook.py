from dataclasses import dataclass
from typing import TYPE_CHECKING

from flet.components.component_owned import ComponentOwned

if TYPE_CHECKING:
    pass


@dataclass()
class Hook(ComponentOwned):
    """
    Base class for component hook state objects.

    Each hook instance is bound to an owning component via
    [`ComponentOwned`][flet.] and reused by position across
    renders, allowing hook-specific subclasses to persist state between renders.
    """

    pass
