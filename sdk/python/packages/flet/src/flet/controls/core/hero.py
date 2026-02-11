from typing import Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl

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

    tag: HeroTag
    """
    A unique identifier used to match source and destination Hero controls.

    Raises:
        ValueError: If not provided or not of type `str`, `int`, `float`, or `bool`.
    """

    content: Control
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

    def before_update(self):
        super().before_update()
        if self.tag is None:
            raise ValueError("tag must be provided")
        if not isinstance(self.tag, (str, int, float, bool)):
            raise ValueError(
                f"tag must be str, int, float, or bool, got {type(self.tag)}"
            )
        if not self.content.visible:
            raise ValueError("content must be visible")
