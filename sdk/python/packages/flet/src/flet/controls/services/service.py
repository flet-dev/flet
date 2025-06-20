from dataclasses import dataclass

from flet.controls.base_control import BaseControl

__all__ = ["Service"]


@dataclass(kw_only=True)
class Service(BaseControl):
    pass
