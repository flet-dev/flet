import weakref
from dataclasses import InitVar
from typing import Any, Callable, ClassVar, Generic, Optional, TypeVar

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.ref import Ref

__all__ = ["StateView"]

T = TypeVar("T")


@control("StateView", post_init_args=4)
class StateView(Control, Generic[T]):
    """
    Builds control tree on every update based on data.
    """

    state: InitVar[T]
    builder: InitVar[Callable[[T], Control]]
    state_key: InitVar[Optional[Callable[[T], Any]]] = None
    content: Optional[Control] = None

    # Cache: (control_id, state_id) -> control
    _builder_cache: ClassVar[weakref.WeakValueDictionary[tuple[int, Any], Control]] = (
        weakref.WeakValueDictionary()
    )

    def __post_init__(
        self,
        ref: Optional[Ref[Any]],
        state: T,
        builder: Callable[[T], Control],
        state_key: Optional[Callable[[T], Any]] = None,
    ):
        Control.__post_init__(self, ref)
        self._state: T = state
        self._builder = builder
        self._state_key = state_key

    def before_update(self):
        # print(f"StateView({self._i}).before_update")
        frozen = getattr(self, "_frozen", None)
        if frozen:
            del self._frozen

        cache_key = (self._i, self._state_key(self._state)) if self._state_key else None

        if cache_key is not None and cache_key in self._builder_cache:
            self.content = self._builder_cache[cache_key]
        else:
            self.content = self._builder(self._state)
            if cache_key is not None and self.content:
                self._builder_cache[cache_key] = self.content

        if self.content:
            object.__setattr__(self.content, "_frozen", True)
        if frozen:
            self._frozen = frozen
