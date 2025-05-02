from typing import Any, Optional

from flet.controls.base_control import BaseControl, control
from flet.controls.control import Control
from flet.controls.types import OptionalNumber

__all__ = ["MultiView"]


@control("MultiView")
class MultiView(BaseControl):
    view_id: int
    initial_data: dict[str, Any]
    content: Optional[Control] = None
    width: OptionalNumber = None
    height: OptionalNumber = None
