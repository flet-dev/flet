from dataclasses import dataclass

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.types import OptionalControlEventCallable


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
    
    on_dismiss: OptionalControlEventCallable = None
    """
    Fires when dialog is dismissed.
    """
