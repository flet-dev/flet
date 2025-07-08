from dataclasses import dataclass
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.control_event import ControlEventHandler


@dataclass(kw_only=True)
class DialogControl(AdaptiveControl):
    """
    A base class for dialog controls.
    """

    open: bool = False
    """
    Set to `True` to display this dialog.
    """

    on_dismiss: Optional[ControlEventHandler["DialogControl"]] = None
    """
    Called when dialog is dismissed.
    """
