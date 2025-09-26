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
    """

    modal: bool = False
    """
    Whether this dialog cannot be dismissed by clicking the area outside of it.
    """

    title: Optional[StrOrControl] = None
    """
    The title of this dialog, displayed in a large font at the top of this dialog.

    Typically a [`Text`][flet.] control.
    """

    content: Optional[Control] = None
    """
    The content of this dialog, displayed in a light font at the center of this dialog.

    Typically a [`Column`][flet.] that contains
    the dialog's [`Text`][flet.] message.
    """

    actions: list[Control] = field(default_factory=list)
    """
    A set of actions that are displayed at the bottom of the dialog.

    Typically this is a list of [`CupertinoDialogAction`][flet.] controls.
    """

    inset_animation: Animation = field(
        default_factory=lambda: Animation(
            curve=AnimationCurve.DECELERATE, duration=Duration(milliseconds=100)
        )
    )
    """
    The animation style to be used when the system keyboard intrudes into the space
    that the dialog is placed in.
    """

    def before_update(self):
        super().before_update()
        if not (
            (isinstance(self.title, str) or self.title.visible)
            or (self.content and self.content.visible)
            or any(a.visible for a in self.actions)
        ):
            raise ValueError(
                "AlertDialog has nothing to display. Provide at minimum one of the "
                "following: title, content, actions"
            )
