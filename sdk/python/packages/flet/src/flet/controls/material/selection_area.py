from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler

__all__ = ["SelectionArea"]


@control("SelectionArea")
class SelectionArea(Control):
    """
    Flet controls are not selectable by default. SelectionArea is used to enable
    selection for its child control.
    """

    content: Control
    """
    The child control this selection area applies to.

    If you need to have multiple selectable controls, use container-like controls
    like [`Row`][flet.] or [`Column`][flet.], which have a `controls` property
    for this purpose.

    Raises:
        ValueError: If [`content`][(c).] is not visible.
    """

    on_change: Optional[ControlEventHandler["SelectionArea"]] = None
    """
    Called when the selected content changes.
    """

    def before_update(self):
        super().before_update()
        if not self.content.visible:
            raise ValueError("content must be visible")
