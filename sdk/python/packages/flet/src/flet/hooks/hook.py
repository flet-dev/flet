from dataclasses import dataclass
from typing import TYPE_CHECKING

from flet.components.component_owned import ComponentOwned

if TYPE_CHECKING:
    pass


@dataclass()
class Hook(ComponentOwned):
    pass
