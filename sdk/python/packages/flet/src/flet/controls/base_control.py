import inspect
import logging
import sys
from dataclasses import InitVar, dataclass, field
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union, overload

from flet.controls.context import _context_page, context
from flet.controls.control_event import ControlEvent, get_event_field_type
from flet.controls.id_counter import ControlId
from flet.controls.keys import KeyValue
from flet.controls.ref import Ref
from flet.utils.from_dict import from_dict
from flet.utils.object_model import get_param_count

logger = logging.getLogger("flet")
controls_log = logging.getLogger("flet_controls")

if sys.version_info >= (3, 11):
    from typing import dataclass_transform
else:
    from typing_extensions import dataclass_transform


if TYPE_CHECKING:
    from .base_page import BasePage
    from .page import Page

__all__ = [
    "BaseControl",
    "control",
    "skip_field",
]


def skip_field():
    return field(default=None, metadata={"skip": True})


T = TypeVar("T", bound="BaseControl")


@overload
def control(cls: type[T]) -> type[T]: ...


@overload
def control(
    dart_widget_name: Optional[Union[type[T], str]] = None,
    *,
    isolated: Optional[bool] = None,
    post_init_args: int = 1,
    **dataclass_kwargs: Any,
) -> Callable[[type[T]], type[T]]: ...


@dataclass_transform()
def control(
    dart_widget_name: Optional[Union[type[T], str]] = None,
    *,
    isolated: Optional[bool] = None,
    post_init_args: int = 1,
    **dataclass_kwargs: Any,
) -> Union[type[T], Callable[[type[T]], type[T]]]:
    """
    Decorator to optionally set widget name and 'isolated' while behaving
    like [`@dataclass`][dataclasses.dataclass].

    Parameters:
        dart_widget_name: The name of widget on Dart side.
        isolated: If `True`, marks the control as isolated. An isolated control
            is excluded from page updates when its parent control is updated.
        post_init_args: Number of InitVar arguments to pass to __post_init__.
        dataclass_kwargs: Additional keyword arguments passed to `@dataclass`.

    Usage:
        - Supports `@control` (without parentheses)
        - Supports `@control("WidgetName")` (with optional arguments)
        - Supports `@control("WidgetName", post_init_args=1, isolated=True)` to
            specify the number of `InitVar` arguments and isolation
    """

    # Case 1: If used as `@control` (without parentheses)
    if isinstance(dart_widget_name, type):
        return _apply_control(
            dart_widget_name, None, isolated, post_init_args, **dataclass_kwargs
        )

    # Case 2: If used as `@control("custom_type", post_init_args=N, isolated=True)`
    def wrapper(cls: type[T]) -> type[T]:
        return _apply_control(
            cls, dart_widget_name, isolated, post_init_args, **dataclass_kwargs
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
    Arbitrary data of any type.
    """

    key: Optional[KeyValue] = None

    ref: InitVar[Optional[Ref["BaseControl"]]] = None
    """A reference to this control."""

    _internals: dict = field(
        default_factory=dict, init=False, repr=False, compare=False
    )
    """
    A dictionary for storing internal control configuration.
    """

    def __post_init__(self, ref: Optional[Ref[Any]]):
        self.__class__.__hash__ = BaseControl.__hash__
        self._i = ControlId.next()
        if not hasattr(self, "_c") or self._c is None:
            cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            raise ValueError(
                f"Control {cls_name} must have @control decorator with "
                "type_name specified."
            )

        if ref is not None:
            ref.current = self

        self.init()

        # control_id = self._i
        # object_id = id(self)
        # ctrl_type = self._c
        # weakref.finalize(
        #     self,
        #     lambda: controls_log.debug(
        #         f"Control was garbage collected: {ctrl_type}({control_id} "
        #         f"- {object_id})"
        #     ),
        # )

    def __hash__(self) -> int:
        return object.__hash__(self)

    @property
    def parent(self) -> Optional["BaseControl"]:
        """
        The direct ancestor(parent) of this control.

        It defaults to `None` and will only have a value when this control is mounted
        (added to the page tree).

        The `Page` control (which is the root of the tree) is an exception - it always
        has `parent=None`.
        """
        parent_ref = getattr(self, "_parent", None)
        return parent_ref() if parent_ref else None

    @property
    def page(self) -> Union["Page", "BasePage"]:
        """
        The page to which this control belongs to.
        """
        from .page import Page

        parent = self
        while parent:
            if isinstance(parent, (Page)):
                return parent
            parent = parent.parent
        raise RuntimeError(
            f"{self.__class__.__qualname__}({self._i}) "
            "Control must be added to the page first"
        )

    def is_isolated(self):
        return hasattr(self, "_isolated") and self._isolated

    def init(self):
        pass

    def build(self):
        """
        Called once during control initialization to define its child controls.
        self.page is available in this method.
        """
        pass

    def before_update(self):
        """
        This method is called every time when this control is being updated.

        /// details | Note
        Make sure not to call/request an `update()` here.
        ///
        """
        pass

    def _before_update_safe(self):
        frozen = getattr(self, "_frozen", None)
        if frozen is not None:
            del self._frozen

        self.before_update()

        if frozen is not None:
            self._frozen = frozen

    def before_event(self, e: ControlEvent):
        return True

    def did_mount(self):
        controls_log.debug(f"{self}.did_mount()")
        pass

    def will_unmount(self):
        controls_log.debug(f"{self}.will_unmount()")
        pass

    # public methods
    def update(self) -> None:
        if hasattr(self, "_frozen"):
            raise RuntimeError("Frozen control cannot be updated.")
        if not self.page:
            raise RuntimeError(
                f"{self.__class__.__qualname__} Control must be added to the page first"
            )
        self.page.update(self)

    async def _invoke_method(
        self,
        method_name: str,
        arguments: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = None,
    ) -> Any:
        if not self.page:
            raise RuntimeError(
                f"{self.__class__.__qualname__} Control must be added to the page first"
            )

        return await self.page.session.invoke_method(
            self._i, method_name, arguments, timeout
        )

    async def _trigger_event(
        self, event_name: str, event_data: Any, e: Optional[ControlEvent] = None
    ):
        field_name = f"on_{event_name}"
        if not hasattr(self, field_name):
            # field_name not defined
            return

        event_type = get_event_field_type(self, field_name)
        if event_type is None:
            return

        if e is None:
            if event_type == ControlEvent or not isinstance(event_data, dict):
                # simple ControlEvent
                e = ControlEvent(control=self, name=event_name, data=event_data)
            else:
                # custom ControlEvent
                args = {
                    "control": self,
                    "name": event_name,
                    **(event_data or {}),
                }
                e = from_dict(event_type, args)

        handle_event = self.before_event(e)

        if handle_event is None or handle_event:
            _context_page.set(self.page)
            context.reset_auto_update()

            controls_log.debug(f"Trigger event {self}.{field_name} {e}")

            if not self.page:
                raise RuntimeError(
                    "Control must be added to a page before triggering events. Use "
                    "page.add(control) or add it to a parent control that's on a page."
                )
            session = self.page.session

            # Handle async and sync event handlers accordingly
            event_handler = getattr(self, field_name)
            if inspect.iscoroutinefunction(event_handler):
                if get_param_count(event_handler) == 0:
                    await event_handler()
                else:
                    await event_handler(e)

            elif inspect.isasyncgenfunction(event_handler):
                if get_param_count(event_handler) == 0:
                    async for _ in event_handler():
                        await session.after_event(session.index.get(self._i))
                else:
                    async for _ in event_handler(e):
                        await session.after_event(session.index.get(self._i))
                return

            elif inspect.isgeneratorfunction(event_handler):
                if get_param_count(event_handler) == 0:
                    for _ in event_handler():
                        await session.after_event(session.index.get(self._i))
                else:
                    for _ in event_handler(e):
                        await session.after_event(session.index.get(self._i))
                return

            elif callable(event_handler):
                if get_param_count(event_handler) == 0:
                    event_handler()
                else:
                    event_handler(e)

            await session.after_event(session.index.get(self._i))

    def _migrate_state(self, other: "BaseControl"):
        if not isinstance(other, BaseControl):
            return
        self._i = other._i
        if self.data is None:
            self.data = other.data

    def __str__(self):
        return f"{self._c}({self._i} - {id(self)})"
