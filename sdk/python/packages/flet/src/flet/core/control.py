from dataclasses import InitVar, dataclass, field
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    dataclass_transform,
)

from flet.core.badge import BadgeValue
from flet.core.event import Event
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import OptionalNumber, ResponsiveNumber

if TYPE_CHECKING:
    from .page import Page


def event(type: Type[Event]):
    return field(default=None, metadata={"type": type})


def skip_field():
    return field(default=None, repr=False, metadata={"skip": True})


EventHandler: TypeAlias = Callable[[Event], None]

T = TypeVar("T", bound="Control")


@dataclass_transform()
def control(
    cls_or_type_name: Optional[Union[Type[T], str]] = None, **dataclass_kwargs
) -> Union[Type[T], Callable[[Type[T]], Type[T]]]:
    """Decorator to optionally set 'type' while behaving like @dataclass.

    - Supports `@control` (without parentheses)
    - Supports `@control("custom_type")` (with optional arguments)
    """

    # Case 1: If used as `@control` (without parentheses)
    if isinstance(cls_or_type_name, type):
        return _apply_control(cls_or_type_name, None, **dataclass_kwargs)

    # Case 2: If used as `@control("custom_type")`
    def wrapper(cls: Type[T]) -> Type[T]:
        return _apply_control(cls, cls_or_type_name, **dataclass_kwargs)

    return wrapper


def _apply_control(
    cls: Type[T], type_name: Optional[str], **dataclass_kwargs
) -> Type[T]:
    """Applies @control logic, ensuring compatibility with @dataclass."""
    cls = dataclass(**dataclass_kwargs)(cls)  # Apply @dataclass first

    orig_post_init = getattr(cls, "__post_init__", lambda self, ref=None: None)

    def new_post_init(self: T, ref: Optional["Ref[T]"] = None) -> None:
        """Set the type only if a type_name is explicitly provided and type is not overridden."""
        if type_name is not None and (not hasattr(self, "type") or self.type is None):
            self.type = type_name  # Only set type if explicitly provided
        orig_post_init(self, ref)  # Call the original __post_init__

    setattr(cls, "__post_init__", new_post_init)
    return cls


@dataclass(kw_only=True)
class Control:
    id: int = field(init=False)
    type: str = field(init=False)
    expand: Union[None, bool, int] = None
    expand_loose: Optional[bool] = None
    col: Optional[ResponsiveNumber] = None
    opacity: OptionalNumber = None
    tooltip: Optional[TooltipValue] = None
    badge: Optional[BadgeValue] = None
    visible: Optional[bool] = None
    disabled: Optional[bool] = None
    rtl: Optional[bool] = None
    data: Any = skip_field()
    ref: InitVar[Optional[Ref[Any]]] = None

    def __post_init__(self, ref: Optional[Ref[Any]]):
        self.__class__.__hash__ = Control.__hash__
        self.id = self.__hash__()
        if not hasattr(self, "type") or self.type is None:
            cls_name = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            raise Exception(
                f"Control {cls_name} must have @control decorator with type_name specified."
            )

        if ref is not None:
            ref.current = self

    def __hash__(self) -> int:
        return object.__hash__(self)

    @property
    def parent(self) -> Optional["Control"]:
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

    def is_isolated(self) -> bool:
        return False

    def build(self):
        pass

    def before_update(self):
        pass

    def did_mount(self):
        pass

    def will_unmount(self):
        pass

    # # opacity
    # @property
    # def opacity(self) -> float:
    #     return self._get_attr("opacity", data_type="float", def_value=1.0)

    # @opacity.setter
    # def opacity(self, value: OptionalNumber):
    #     assert (
    #         value is None or 0.0 <= value <= 1.0
    #     ), "opacity must be between 0.0 and 1.0"
    #     self._set_attr("opacity", value)

    # public methods
    def update(self) -> None:
        # assert (
        #     self.__page
        # ), f"{self.__class__.__qualname__} Control must be added to the page first"
        # self.__page.update(self)
        pass

    async def update_async(self) -> None:
        # assert (
        #     self.__page
        # ), f"{self.__class__.__qualname__} Control must be added to the page"
        # await self.__page.update_async(self)
        pass

    def clean(self) -> None:
        raise Exception("Deprecated!")

    def invoke_method(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
        wait_timeout: Optional[float] = 5,
    ) -> Optional[str]:
        # assert (
        #     self.__page
        # ), f"{self.__class__.__qualname__} Control must be added to the page first"
        # if arguments:
        #     # remove items with None values and convert other values to string
        #     arguments = {k: str(v) for k, v in arguments.items() if v is not None}
        # return self.__page._invoke_method(
        #     control_id=self.uid,
        #     method_name=method_name,
        #     arguments=arguments,
        #     wait_for_result=wait_for_result,
        #     wait_timeout=wait_timeout,
        # )
        return None

    def invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
        wait_timeout: Optional[float] = 5,
    ):
        # assert (
        #     self.__page
        # ), f"{self.__class__.__qualname__} Control must be added to the page first"
        # if arguments:
        #     # remove items with None values and convert other values to string
        #     arguments = {k: str(v) for k, v in arguments.items() if v is not None}
        # return self.__page._invoke_method_async(
        #     control_id=self.uid,
        #     method_name=method_name,
        #     arguments=arguments,
        #     wait_for_result=wait_for_result,
        #     wait_timeout=wait_timeout,
        # )
        return None
