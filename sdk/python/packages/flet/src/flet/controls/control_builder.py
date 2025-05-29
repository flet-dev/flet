from dataclasses import InitVar
from typing import Any, Callable, Generic, Optional, TypeVar

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.ref import Ref

__all__ = ["ControlBuilder"]

T = TypeVar("T")


@control("ControlBuilder", post_init_args=3)
class ControlBuilder(Control, Generic[T]):
    """
    Builds control tree on every update based on data.

    -----

    Online docs: https://flet.dev/docs/controls/controlbuilder
    """

    state: InitVar[T]
    builder: InitVar[Callable[[T], Control]]
    content: Optional[Control] = None

    def __post_init__(
        self, ref: Optional[Ref[Any]], state: T, builder: Callable[[T], Control]
    ):
        Control.__post_init__(self, ref)
        self._state: T = state
        self._builder = builder

    def before_update(self):
        frozen = getattr(self, "_frozen", None)
        if frozen:
            del self._frozen
        self.content = self._builder(self._state)
        if self.content:
            object.__setattr__(self.content, "_frozen", True)
        if frozen:
            self._frozen = frozen
