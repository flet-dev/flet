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

    Raises:
        AssertionError: If [`content`][(c).] is not visible
    """

    content: Control
    """
    The child control this selection area applies to.
    
    If you need to have multiple selectable controls, use container-like controls 
    like [`Row`][flet.Row] or [`Column`][flet.Column], which have a `controls` property for this purpose.
    """

    on_change: Optional[ControlEventHandler["SelectionArea"]] = None
    """
    Called when the selected content changes.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
