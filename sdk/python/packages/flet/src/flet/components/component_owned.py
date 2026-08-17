import weakref
from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet.components.component import Component


# Identity equality (eq=False) is required: these are lifecycle objects tracked
# in lists and matched with `in`/`list.remove`. The dataclass fields are all
# InitVars, so a generated __eq__ would compare no fields and make every
# instance equal, matching/removing the wrong subscription (see #6776).
@dataclass(eq=False)
class ComponentOwned:
    """
    Base mixin for objects owned by a component via weak reference.

    Used by hook/subscription state objects that must reference their owning
    component without creating strong-reference cycles.
    """

    owner: InitVar["Component"]
    """
    Component that owns this object.
    """

    def __post_init__(self, owner: "Component") -> None:
        self._component = weakref.ref(owner)

    @property
    def component(self) -> Optional["Component"]:
        """
        The current owning component, if still alive.

        Returns:
            The owner component, or `None` if the weak reference is no longer valid.
        """
        return self._component()

    @component.setter
    def component(self, value: "Component") -> None:
        self._component = weakref.ref(value)
