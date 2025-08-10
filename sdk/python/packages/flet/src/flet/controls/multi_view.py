from typing import Any

from flet.controls.base_control import control
from flet.controls.base_page import BasePage

__all__ = ["MultiView"]


@control()
class MultiView(BasePage):
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
