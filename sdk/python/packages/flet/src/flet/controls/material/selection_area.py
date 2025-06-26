from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler

__all__ = ["SelectionArea"]


@control("SelectionArea")
class SelectionArea(Control):
    """
    Flet controls are not selectable by default. SelectionArea is used to enable
    selection for its child control.

    Online docs: https://flet.dev/docs/controls/selectionarea
    """

    content: Control
    """
    A child Control contained by the SelectionArea. If you need to have multiple
    selectable controls, use `Row`, `Column`, or `Stack`, which have a `controls`
    property, and then provide multiple controls to that control.
    """

    on_change: OptionalControlEventHandler["SelectionArea"] = None
    """
    Fires when the selected content changes.
    """

    def before_update(self):
        super().before_update()
        assert self.content.visible, "content must be visible"
