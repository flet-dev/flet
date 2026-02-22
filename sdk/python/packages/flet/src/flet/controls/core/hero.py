from typing import Annotated, Union

from flet.controls._validation import V
from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.layout_control import LayoutControl

__all__ = ["Hero"]


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

    def before_update(self):
        super().before_update()
        if self.tag is None:
            raise ValueError("tag must be provided")
        if not isinstance(self.tag, (str, int, float, bool)):
            raise ValueError(
                f"tag must be str, int, float, or bool, got {type(self.tag)}"
            )
