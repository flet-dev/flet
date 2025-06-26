from typing import Any

from flet.controls.base_control import control
from flet.controls.page_view import PageView

__all__ = ["MultiView"]


@control()
class MultiView(PageView):
    """
    TBD
    """
    
    view_id: int
    """
    TBD
    """
    initial_data: dict[str, Any]
    """
    TBD
    """
