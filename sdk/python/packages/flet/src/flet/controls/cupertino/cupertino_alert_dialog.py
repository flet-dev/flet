from dataclasses import field
from typing import Optional

from flet.controls.animation import Animation, AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import Duration
from flet.controls.types import StrOrControl

__all__ = ["CupertinoAlertDialog"]


@control("CupertinoAlertDialog")
class CupertinoAlertDialog(DialogControl):
    """
    An iOS-style alert dialog.

    An alert dialog informs the user about situations that require acknowledgement. An
    alert dialog has an optional title and an optional list of actions. The title is
    displayed above the content and the actions are displayed below the content.

    Online docs: https://flet.dev/docs/controls/cupertinoalertdialog
    """

    modal: bool = False
    """
    If set to True, dialog cannot be dismissed by clicking the area outside of it.
    The default value is False.
    """

    title: Optional[StrOrControl] = None
    """
    The (optional) title of the dialog is displayed in a large font at the top of the 
    dialog.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    content: Optional[Control] = None
    """
    The (optional) content of the dialog is displayed in the center of the dialog in a 
    lighter font.

    Typically this is a [`Column`](https://flet.dev/docs/controls/column) that contains 
    the dialog's [`Text`](https://flet.dev/docs/controls/text) message.
    """

    actions: list[Control] = field(default_factory=list)
    """
    The (optional) set of actions that are displayed at the bottom of the dialog.

    Typically this is a list of 
    [`CupertinoDialogAction`](https://flet.dev/docs/controls/cupertinodialogaction) 
    controls.
    """

    inset_animation: Animation = field(
        default_factory=lambda: Animation(
            curve=AnimationCurve.DECELERATE, duration=Duration(milliseconds=100)
        )
    )
    """
    The animation style to be used when the system keyboard intrudes into the space 
    that the dialog is placed in.

    Value is of type 
    [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    def before_update(self):
        super().before_update()
        assert (
            (isinstance(self.title, str) or self.title.visible)
            or (self.content and self.content.visible)
            or any(a.visible for a in self.actions)
        ), "AlertDialog has nothing to display. Provide at minimum one of the "
        "following: title, content, actions"
