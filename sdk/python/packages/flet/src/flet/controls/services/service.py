import contextlib
from dataclasses import dataclass

from flet.controls.base_control import BaseControl
from flet.controls.context import context

__all__ = ["Service"]


@dataclass(kw_only=True)
class Service(BaseControl):
    """
    Base class for user services.
    """

    def init(self):
        super().init()
        with contextlib.suppress(RuntimeError):
            context.page._services.register_service(self)
