import contextlib
from dataclasses import dataclass

from flet.controls.base_control import BaseControl
from flet.controls.context import context

__all__ = ["Service"]


@dataclass(kw_only=True)
class Service(BaseControl):
    def init(self):
        super().init()
        with contextlib.suppress(RuntimeError):
            context.page._user_services.register_service(self)
