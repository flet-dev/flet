from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class MapLayer(Control):
    """
    Abstract class for all map layers.
    """

    def __init__(
        self,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            data=data,
        )
