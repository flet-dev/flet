import weakref
from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet.components.component import Component


@dataclass()
class ComponentOwned:
    owner: InitVar["Component"]

    def __post_init__(self, owner: "Component") -> None:
        self._component = weakref.ref(owner)

    @property
    def component(self) -> Optional["Component"]:
        return self._component()

    @component.setter
    def component(self, value: "Component") -> None:
        self._component = weakref.ref(value)
