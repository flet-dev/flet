from typing import Annotated, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl
from flet.utils.validation import V

__all__ = ["Hero", "HeroTag"]

HeroTag = Union[str, int, float, bool]
"""Type alias for Hero tag values.

Represents an identifier used to match source and destination [`Hero`][flet.]
controls during route transitions.
"""


@control("Hero")
class Hero(LayoutControl):
    """
    Marks the [`content`][(c).] as a shared element for route transitions.

    Place a `Hero` with the same [`tag`][(c).] in both source and destination views to
    animate that control between routes.
    """

    tag: Annotated[
        HeroTag,
        V.instance_of((str, int, float, bool)),
    ]
    """
    A unique identifier used to match source and destination Hero controls.

    Raises:
        ValueError: If it is not of type `str`, `int`, `float`, or `bool`.
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
