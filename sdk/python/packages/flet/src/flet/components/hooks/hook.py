from dataclasses import dataclass
from typing import TYPE_CHECKING

from flet.components.component_owned import ComponentOwned

if TYPE_CHECKING:
    pass


# eq=False: hooks are stored per render slot and compared by identity; a
# field-based __eq__ would make distinct hooks compare equal (see #6776).
@dataclass(eq=False)
class Hook(ComponentOwned):
    """
    Base class for component hook state objects.

    Each hook instance is bound to an owning component via
    `ComponentOwned` and reused by position across
    renders, allowing hook-specific subclasses to persist state between renders.
    """

    pass
