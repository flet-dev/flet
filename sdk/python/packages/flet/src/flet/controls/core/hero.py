from typing import Annotated

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.controls.validation import V

__all__ = ["Hero"]


@control("Hero")
class Hero(LayoutControl):
    """
    Marks the [`content`][(c).] as a shared element for route transitions.

    Place a `Hero` with the same [`tag`][(c).] in both source and destination views to
    animate that control between routes.
    """

    tag: Annotated[
        str,
        V.instance_of(str),
    ]
    """
    A unique identifier used to match source and destination Hero controls.

    Raises:
        ValueError: If it is not of type `str`.
    """

    content: Annotated[
        Control,
        V.visible_control(),
    ]
    """
    The control to display and animate.

    Raises:
        ValueError: If it is not visible.
    """

    transition_on_user_gestures: bool = False
    """
    Whether to animate when the route is transitioned by a \
    user gesture (for example, iOS back swipe).
    """
