from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.client_action import ClientAction
from flet.controls.control import Control

__all__ = ["ActionControl"]


@control(kw_only=True)
class ActionControl(Control):
    """
    Base class for controls that can perform :class:`~flet.ClientAction` work when
    they are activated.

    Browsers only allow a page to open a file picker, write to the clipboard, show
    a share sheet or open a new tab while they are handling the user's click or key
    press. Sending that click to your Python code and acting on the reply takes
    longer than the permission lasts, so those operations are silently ignored on
    iOS Safari while Android and desktop browsers let them through. Controls
    inheriting from this class accept an :attr:`action`, which the client performs
    inside the original gesture instead.

    Extension developers can inherit from this class to give their own controls the
    same capability; the client runs whatever actions the control declares before
    the control's own click event is dispatched.
    """

    action: Optional[Union[ClientAction, list[ClientAction]]] = None
    """
    Action(s) performed by the client when this control is activated, without a
    round trip to your Python code.

    Use this for operations a browser only permits while it is handling the
    user's click, such as opening a file picker, writing to the clipboard,
    showing a share sheet or opening a new tab.
    See :class:`~flet.ClientAction`.
    """
