from dataclasses import field
from typing import ClassVar, Optional

from flet.controls._validation import ControlRule, V
from flet.controls.animation import Animation, AnimationCurve
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import Duration
from flet.controls.types import ColorValue, StrOrControl

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
    The content of this dialog, displayed in a light font at the center of this \
    dialog.

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
    The animation style to be used when the system keyboard intrudes into the space \
    that the dialog is placed in.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier below this dialog.

    If `None`, then [`DialogTheme.barrier_color`][flet.] is used.
    If that is also `None`, the default is `Colors.BLACK_54`.
    """

    __outbound_rules__: ClassVar[tuple[ControlRule, ...]] = (
        V.ensure(
            lambda ctrl: (isinstance(ctrl.title, str))
            or (isinstance(ctrl.title, Control) and ctrl.title.visible)
            or (ctrl.content is not None and ctrl.content.visible)
            or any(action.visible for action in ctrl.actions),
            message=(
                "AlertDialog has nothing to display. Provide at minimum one of the "
                "following: title, content, actions"
            ),
        ),
    )
