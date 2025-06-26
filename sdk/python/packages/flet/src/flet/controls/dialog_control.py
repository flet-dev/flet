from dataclasses import dataclass

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.control_event import OptionalControlEventHandler


@dataclass(kw_only=True)
class DialogControl(AdaptiveControl):
    """
    TBD
    """

    open: bool = False
    """
    Set to `True` to display a dialog.

    Value is of type `bool` and defaults to `False`.
    """

    on_dismiss: OptionalControlEventHandler["DialogControl"] = None
    """
    Fires when dialog is dismissed.
    """
