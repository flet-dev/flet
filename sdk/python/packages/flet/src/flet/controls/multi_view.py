from typing import Any

from flet.controls.base_control import control
from flet.controls.base_page import BasePage

__all__ = ["MultiView"]


@control()
class MultiView(BasePage):
    """
    Represents an additional app view managed by a multi-view session.

    Multi-view sessions can create more than one view for the same app. Each view
    has its own :attr:`view_id` and can receive an initial payload through
    :attr:`initial_data`.
    """

    view_id: int
    """
    Unique identifier of this view.
    """

    initial_data: dict[str, Any]
    """
    Initial payload provided when this view was opened.
    """
