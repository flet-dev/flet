import weakref
from dataclasses import InitVar, dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from flet.components.component import Component


# `eq=False` keeps identity-based `__eq__`/`__hash__` from `object`. These are
# lifecycle objects tracked in lists and matched with `in`/`list.remove`, so two
# distinct instances must never compare equal - a generated `__eq__` compares
# fields and would match (and remove) the wrong instance. See #6776.
#
# `@dataclass` regenerates `__eq__` on every subclass, so each subclass of
# `ComponentOwned` must repeat `eq=False`; inheriting it is not enough.
@dataclass(eq=False)
class ComponentOwned:
    """
    Base mixin for objects owned by a component via weak reference.

    Used by hook/subscription state objects that must reference their owning
    component without creating strong-reference cycles.

    Subclasses are compared by identity, not by field values.
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
