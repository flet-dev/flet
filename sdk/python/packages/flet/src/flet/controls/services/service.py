from dataclasses import dataclass
from typing import Any, ClassVar, Optional

from flet.controls.base_control import BaseControl
from flet.controls.context import context
from flet.controls.ref import Ref

__all__ = ["Service"]


@dataclass(kw_only=True)
class Service(BaseControl):
    """
    Base class for user services.

    By default, construction registers the service with the current page after
    `init()` returns, whether or not the override calls `super().init()`. Set client
    properties and event handlers in `init()` so they are included in registration
    and available when the Dart service initializes. Without a current page context,
    the service is constructed but not registered.

    Note:
        Inside `init()`, the service isn't attached to the page yet: `self.page`
        and `self.update()` raise. Use `ft.context.page` to access the current page.

    Declared fields participate in serialization unless excluded with
    `metadata={"skip": True}`; a leading underscore does not exclude a field.
    Keep Python-only state, such as clients or handles, in excluded fields or
    attributes assigned in `init()` without declaring them as fields.
    """

    _auto_register: ClassVar[bool] = True
    """
    Whether constructing an instance registers it with the current page.

    Set to `False` as a class attribute to opt out.
    """

    def __post_init__(self, ref: Optional[Ref[Any]]):
        """
        Finalize the service and register it with the current page.

        Prefer overriding `init()` for setup. If this method is overridden,
        registration occurs inside `super().__post_init__(ref)`: fields assigned
        after that call require a later update to reach the client.
        """
        super().__post_init__(ref)
        if not self._auto_register:
            return
        try:
            page = context.page
        except RuntimeError:
            return
        page._services.register_service(self)
