from typing import Any

from flet.controls.base_control import control
from flet.controls.page_view import PageView

__all__ = ["MultiView"]


@control()
class MultiView(PageView):
    view_id: int
    initial_data: dict[str, Any]
