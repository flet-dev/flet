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

    A service registers itself with the current page when it is constructed, right
    after its `init()` returns, so everything set in `init()` - before or after
    `super().init()` - is part of the message that adds the service to the client.

    Inside `init()` the service isn't attached to the page yet: `self.page` and
    `self.update()` raise, so use `ft.context.page` there. A service constructed
    outside a Flet app callback (for example, at module level or in a plain
    `threading.Thread`) has no current page and is not registered.

    Every field declared on a service, public or private, is sent to the client, so
    its value must be serializable. Keep Python-only state (callables, clients,
    handles) in attributes assigned in `init()` without declaring them as fields.
    """

    _auto_register: ClassVar[bool] = True
    """
    Whether constructing an instance registers it with the current page.

    Set to `False` as a class attribute to opt out.
    """

    def __post_init__(self, ref: Optional[Ref[Any]]):
        """
        Finalize the service and register it with the current page.

        The client creates the service's Dart `FletService` and calls its `init()`
        as soon as the message that adds the service arrives, using only the
        properties in that message. Registration therefore waits until `init()` has
        returned, which also means an `init()` override is registered whether or not
        it calls `super().init()`.

        A subclass that overrides this method is registered inside its
        `super().__post_init__(ref)` call, so fields it sets after that call reach
        the client with the next update instead of the first message. Set such
        fields in `init()`.
        """
        super().__post_init__(ref)
        if not self._auto_register:
            return
        try:
            page = context.page
        except RuntimeError:
            return
        page._services.register_service(self)
