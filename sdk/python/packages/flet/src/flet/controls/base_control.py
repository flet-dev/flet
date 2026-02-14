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
    """
    Creates a dataclass field excluded from control tree traversal and patching.

    The returned field uses `metadata={"skip": True}` so runtime diff/configuration
    logic ignores it. This is intended for Python-side state that must not
    participate in UI reconciliation/serialization.
    """
    return field(default=None, metadata={"skip": True})


T = TypeVar("T", bound="BaseControl")


@overload
def control(cls: type[T]) -> type[T]:
    """
    Overload for using `@control` without arguments.

    Applies dataclass behavior and control wiring to `cls` using default options.
    """
    ...


@overload
def control(
    dart_widget_name: Optional[Union[type[T], str]] = None,
    *,
    isolated: Optional[bool] = None,
    post_init_args: int = 1,
    **dataclass_kwargs: Any,
) -> Callable[[type[T]], type[T]]:
    """
    Overload for using `@control(...)` with explicit decorator arguments.

    Returns a class decorator that applies dataclass behavior and optional
    control metadata (`dart_widget_name`, `isolated`, `post_init_args`).
    """
    ...


@dataclass_transform()
def control(
    dart_widget_name: Optional[Union[type[T], str]] = None,
    *,
    isolated: Optional[bool] = None,
    post_init_args: int = 1,
    **dataclass_kwargs: Any,
) -> Union[type[T], Callable[[type[T]], type[T]]]:
    """
    Decorator to optionally set widget name and 'isolated' while behaving like \
    [`@dataclass`][dataclasses.dataclass].

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
    """
    Base class for all Flet controls and services.
    """

    _i: int = field(init=False, compare=False)
    """
    Runtime-generated internal control id used by the session protocol.
    """

    _c: str = field(init=False)
    """
    Dart-side control type name set by the `@control` decorator.
    """

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
        """
        Finalize control bootstrap after dataclass initialization.

        Assigns an internal id, validates `@control` metadata, attaches `ref`
        when provided, and then calls `init()`. Override `init()` for setup
        logic; avoid overriding this method in normal controls.
        """
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
        """
        Preserve object-identity hashing for mutable dataclass controls.
        """
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
            if isinstance(parent, Page):
                return parent
            parent = parent.parent
        raise RuntimeError(
            f"{self.__class__.__qualname__}({self._i}) "
            "Control must be added to the page first"
        )

    def is_isolated(self):
        """
        Return whether this control is marked as isolated.

        Isolated controls are excluded from parent-driven update traversal and
        are expected to manage their own update boundaries.
        """
        return hasattr(self, "_isolated") and self._isolated

    def init(self):
        """
        Called after control instance initialization and before \
        the first build / update cycle.

        Override this hook to perform lightweight setup that depends on initialized
        fields. Do not call `update()` here.
        """
        pass

    def build(self):
        """
        Called once during control initialization to define its child controls.
        `page` property is available/usable in this method.
        """
        pass

    def before_update(self):
        """
        This method is called every time when this control is being updated.

        Note:
            Make sure not to call/request an `update()` here.
        """
        pass

    def _before_update_safe(self):
        """
        Run `before_update()` while preserving the frozen marker.

        Internal runtime helper. It temporarily removes `_frozen` so the hook
        can adjust properties and then restores the previous frozen state.
        """
        frozen = getattr(self, "_frozen", None)
        if frozen is not None:
            del self._frozen

        self.before_update()

        if frozen is not None:
            self._frozen = frozen

    def before_event(self, e: ControlEvent):
        """
        Intercept an event before its handler is executed.

        Return `False` to cancel dispatch. Return `True` or `None` to continue
        normal event processing.
        """
        return True

    def did_mount(self):
        """
        Called after the control is mounted into the page tree.

        Override to start resources that require an attached page, for example
        subscriptions, timers, or service listeners.
        """
        controls_log.debug(f"{self}.did_mount()")
        pass

    def will_unmount(self):
        """
        Called before the control is removed from the page tree.

        Override to dispose resources created in `did_mount()`, such as
        subscriptions, timers, or external handles.
        """
        controls_log.debug(f"{self}.will_unmount()")
        pass

    # public methods
    def update(self) -> None:
        """
        Request a UI update for this control.

        Call after changing control state or properties. The control must be
        attached to a page and not marked as frozen.
        """
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
        """
        Invoke a runtime method for this control via the active session.

        Internal async bridge used by controls and services for imperative
        method calls on the backend/runtime side.
        """
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
        """
        Resolve and dispatch an event to the matching `on_<event>` handler.

        Internal helper that builds event objects, calls `before_event()`,
        executes sync/async handlers, and notifies session progress.
        """
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
        """
        Transfer transient runtime state from a previous control instance.

        This hook is used by reconciliation when replacing controls with newer
        instances of the same logical node. Override to copy extra runtime
        fields, and always call `super()._migrate_state(other)` first.
        """
        if not isinstance(other, BaseControl):
            return
        self._i = other._i
        if self.data is None:
            self.data = other.data

    def __str__(self):
        """
        Return a debug-friendly control identifier string.
        """
        return f"{self._c}({self._i} - {id(self)})"
