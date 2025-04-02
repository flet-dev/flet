import asyncio
import sys
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Type, TypeVar, Union

from flet.core.badge import BadgeValue
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import Number, ResponsiveNumber
from flet.utils.strings import random_string

# Try importing `dataclass_transform()` for Python 3.11+, else use a no-op function
if sys.version_info >= (3, 11):  # Only use it for Python 3.11+
    from typing import dataclass_transform
else:

    def dataclass_transform():  # No-op decorator for older Python versions
        return lambda x: x


if TYPE_CHECKING:
    from .page import Page

__all__ = ["BaseControl", "Control", "Service", "control", "skip_field"]


def skip_field():
    return field(default=None, repr=False, metadata={"skip": True})


T = TypeVar("T", bound="Control")


@dataclass_transform()
def control(
    cls_or_type_name: Optional[Union[Type[T], str]] = None,
    *,
    post_init_args: int = 1,
    **dataclass_kwargs,
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """Decorator to optionally set 'type' while behaving like @dataclass.

    - Supports `@control` (without parentheses)
    - Supports `@control("custom_type")` (with optional arguments)
    - Supports `@control("custom_type", post_init_args=1)` to specify the number of `InitVar` arguments
    """

    # Case 1: If used as `@control` (without parentheses)
    if isinstance(cls_or_type_name, type):
        return _apply_control(
            cls_or_type_name, None, post_init_args, **dataclass_kwargs
        )

    # Case 2: If used as `@control("custom_type", post_init_args=N)`
    def wrapper(cls: Type[T]) -> Type[T]:
        return _apply_control(cls, cls_or_type_name, post_init_args, **dataclass_kwargs)

    return wrapper


def _apply_control(
    cls: Type[T], type_name: Optional[str], post_init_args: int, **dataclass_kwargs
) -> Type[T]:
    """Applies @control logic, ensuring compatibility with @dataclass."""
    cls = dataclass(**dataclass_kwargs)(cls)  # Apply @dataclass first

    orig_post_init = getattr(cls, "__post_init__", lambda self, *args: None)

    def new_post_init(self: T, *args):
        """Set the type only if a type_name is explicitly provided and type is not overridden."""
        if type_name is not None and (not hasattr(self, "_c") or self._c is None):
            self._c = type_name  # Only set type if explicitly provided

        # Pass only the correct number of arguments to `__post_init__`
        orig_post_init(self, *args[:post_init_args])

    setattr(cls, "__post_init__", new_post_init)
    return cls


@dataclass(kw_only=True)
class BaseControl:
    _i: int = field(init=False)
    _c: str = field(init=False)
    data: Any = skip_field()
    ref: InitVar[Optional[Ref[Any]]] = None

    def __post_init__(self, ref: Optional[Ref[Any]]):
        self.__class__.__hash__ = BaseControl.__hash__
        self._i = self.__hash__()
        if not hasattr(self, "_c") or self._c is None:
            cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            raise Exception(
                f"Control {cls_name} must have @control decorator with type_name specified."
            )

        if ref is not None:
            ref.current = self

        self.__method_calls: Dict[str, asyncio.Event] = {}
        self.__method_call_results: Dict[asyncio.Event, tuple[Any, Optional[str]]] = {}

    def __hash__(self) -> int:
        return object.__hash__(self)

    @property
    def parent(self) -> Optional["BaseControl"]:
        parent_ref = getattr(self, "_parent", None)
        return parent_ref() if parent_ref else None

    @property
    def page(self) -> Optional["Page"]:
        from .page import Page

        parent = self
        while parent:
            if isinstance(parent, Page):
                return parent
            parent = parent.parent
        return None

    def is_isolated(self):
        return False

    def build(self):
        pass

    def before_update(self):
        pass

    def did_mount(self):
        pass

    def will_unmount(self):
        pass

    # public methods
    def update(self) -> None:
        assert (
            self.page
        ), f"{self.__class__.__qualname__} Control must be added to the page first"
        self.page.update(self)

    async def _invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = 10,
    ) -> Any:
        assert (
            self.page
        ), f"{self.__class__.__qualname__} Control must be added to the page first"

        call_id = random_string(10)

        # register callback
        evt = asyncio.Event()
        self.__method_calls[call_id] = evt

        # call method
        result = self.page.get_session().invoke_method(
            self._i, call_id, method_name, arguments
        )

        try:
            await asyncio.wait_for(evt.wait(), timeout=timeout)
        except TimeoutError:
            if call_id in self.__method_calls:
                del self.__method_calls[call_id]
            raise TimeoutError(
                f"Timeout waiting for invokeMethod {method_name}({arguments}) call"
            )

        result, err = self.__method_call_results.pop(evt)
        if err:
            raise Exception(err)
        return result

    def _handle_invoke_method_results(
        self, call_id: str, result: Any, error: Optional[str]
    ) -> None:
        evt = self.__method_calls.pop(call_id, None)
        if evt is None:
            return
        self.__method_call_results[evt] = (result, error)
        evt.set()


@dataclass(kw_only=True)
class Control(BaseControl):
    expand: Union[None, bool, int] = None
    expand_loose: Optional[bool] = None
    col: Optional[ResponsiveNumber] = None
    opacity: Number = field(default=1.0)
    tooltip: Optional[TooltipValue] = None
    badge: Optional[BadgeValue] = None
    visible: bool = field(default=True)
    disabled: bool = field(default=False)
    rtl: bool = field(default=False)

    def before_update(self):
        assert 0.0 <= self.opacity <= 1.0, "opacity must be between 0.0 and 1.0"

    def clean(self) -> None:
        raise Exception("Deprecated!")


@dataclass(kw_only=True)
class Service(BaseControl):
    pass
