import asyncio
import logging
import sys
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union

from flet.controls.control_event import ControlEvent
from flet.controls.control_id import ControlId
from flet.controls.keys import ScrollKey, ValueKey
from flet.controls.ref import Ref
from flet.utils.strings import random_string

logger = logging.getLogger("flet")
controls_log = logging.getLogger("flet_controls")

# Try importing `dataclass_transform()` for Python 3.11+, else use a no-op function
if sys.version_info >= (3, 11):  # Only use it for Python 3.11+
    from typing import dataclass_transform
else:

    def dataclass_transform():  # No-op decorator for older Python versions
        return lambda x: x


if TYPE_CHECKING:
    from .page import Page
    from .page_view import PageView

__all__ = [
    "BaseControl",
    "control",
    "skip_field",
]

_method_calls: dict[str, asyncio.Event] = {}
_method_call_results: dict[asyncio.Event, tuple[Any, Optional[str]]] = {}


def skip_field():
    return field(default=None, metadata={"skip": True})


T = TypeVar("T", bound="BaseControl")


@dataclass_transform()
def control(
    cls_or_type_name: Optional[Union[type[T], str]] = None,
    *,
    isolated: Optional[bool] = None,
    post_init_args: int = 1,
    **dataclass_kwargs,
) -> Union[type[T], Callable[[type[T]], type[T]]]:
    """Decorator to optionally set 'type' and 'isolated' while behaving like @dataclass.

    - Supports `@control` (without parentheses)
    - Supports `@control("custom_type")` (with optional arguments)
    - Supports `@control("custom_type", post_init_args=1, isolated=True)` to
      specify the number of `InitVar` arguments and isolation
    """

    # Case 1: If used as `@control` (without parentheses)
    if isinstance(cls_or_type_name, type):
        return _apply_control(
            cls_or_type_name, None, isolated, post_init_args, **dataclass_kwargs
        )

    # Case 2: If used as `@control("custom_type", post_init_args=N, isolated=True)`
    def wrapper(cls: type[T]) -> type[T]:
        return _apply_control(
            cls, cls_or_type_name, isolated, post_init_args, **dataclass_kwargs
        )

    return wrapper


def _apply_control(
    cls: type[T],
    type_name: Optional[str],
    isolated: Optional[bool],
    post_init_args: int,
    **dataclass_kwargs,
) -> type[T]:
    """Applies @control logic, ensuring compatibility with @dataclass."""
    cls = dataclass(**dataclass_kwargs)(cls)  # Apply @dataclass first

    orig_post_init = getattr(cls, "__post_init__", lambda self, *args: None)

    def new_post_init(self: T, *args):
        """Set the type and isolation only if explicitly provided."""
        if type_name is not None and (not hasattr(self, "_c") or self._c is None):
            self._c = type_name  # Only set type if explicitly provided

        if isolated is not None:
            self._isolated = isolated  # Set the _isolated field if provided

        # Pass only the correct number of arguments to `__post_init__`
        orig_post_init(self, *args[:post_init_args])

    cls.__post_init__ = new_post_init
    return cls


@dataclass(kw_only=True)
class BaseControl:
    _i: int = field(init=False, compare=False)
    _c: str = field(init=False)
    data: Any = skip_field()
    """
    Arbitrary data of any type that can be attached to a control.
    """

    key: Union[ValueKey, ScrollKey, str, int, float, bool, None] = None

    ref: InitVar[Optional[Ref["BaseControl"]]] = None
    """A reference to this control."""

    _internals: dict = field(default_factory=dict, init=False, repr=False, compare=False)

    def __post_init__(self, ref: Optional[Ref[Any]]):
        self.__class__.__hash__ = BaseControl.__hash__
        self._i = ControlId.next()
        if not hasattr(self, "_c") or self._c is None:
            cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            raise Exception(
                f"Control {cls_name} must have @control decorator with "
                "type_name specified."
            )

        if ref is not None:
            ref.current = self

        # control_id = self._i
        # object_id = id(self)
        # ctrl_type = self._c
        # weakref.finalize(
        #     self,
        #     lambda: controls_log.debug(
        #         f"Control was garbage collected: {ctrl_type}({control_id} - {object_id})"
        #     ),
        # )

    def __hash__(self) -> int:
        return object.__hash__(self)

    @property
    def parent(self) -> Optional["BaseControl"]:
        """
        The direct ancestor(parent) of this control.

        It defaults to `None` and will only have a value when this control is mounted (added to the page tree).

        The `Page` control (which is the root of the tree) is an exception - it always has `parent=None`.
        """
        parent_ref = getattr(self, "_parent", None)
        return parent_ref() if parent_ref else None

    @property
    def page(self) -> Optional[Union["Page", "PageView"]]:
        """The page (of type `Page` or `PageView`) to which this control belongs to."""
        from .page import Page, PageView

        parent = self.parent
        while parent:
            if isinstance(parent, (Page, PageView)):
                return parent
            parent = parent.parent
        return None

    def is_isolated(self):
        return hasattr(self, "_isolated") and self._isolated

    def init(self):
        pass

    def before_update(self):
        """
        `before_update()` method is called every time when the control is being updated.
        Make sure not to call `update()` method within `before_update()`.
        """
        pass

    def before_event(self, e: ControlEvent):
        return True

    def did_mount(self):
        controls_log.debug(f"{self._c}({self._i}).did_mount")
        pass

    def will_unmount(self):
        controls_log.debug(f"{self._c}({self._i}).will_unmount")
        pass

    # public methods
    def update(self) -> None:
        if hasattr(self, "_frozen"):
            raise Exception("Frozen control cannot be updated.")
        assert self.page, (
            f"{self.__class__.__qualname__} Control must be added to the page first"
        )
        self.page.update(self)

    async def _invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = 10,
    ) -> Any:
        assert self.page, (
            f"{self.__class__.__qualname__} Control must be added to the page first"
        )

        call_id = random_string(10)

        # register callback
        evt = asyncio.Event()
        _method_calls[call_id] = evt

        # call method
        result = self.page.get_session().invoke_method(
            self._i, call_id, method_name, arguments
        )

        try:
            await asyncio.wait_for(evt.wait(), timeout=timeout)
        except TimeoutError:
            if call_id in _method_calls:
                del _method_calls[call_id]
            raise TimeoutError(
                f"Timeout waiting for invokeMethod {method_name}({arguments}) call"
            ) from None

        result, err = _method_call_results.pop(evt)
        if err:
            raise Exception(err)
        return result

    def _handle_invoke_method_results(
        self, call_id: str, result: Any, error: Optional[str]
    ) -> None:
        evt = _method_calls.pop(call_id, None)
        if evt is None:
            return
        _method_call_results[evt] = (result, error)
        evt.set()
