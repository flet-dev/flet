from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control

__all__ = ["Center"]


@control("Center")
class Center(Control):
    """
    Centers content.

    -----

    Online docs: https://flet.dev/docs/controls/center
    """

    content: Optional[Control] = None
