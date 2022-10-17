from typing import Any, List, Optional

from beartype import beartype
from flet.animation import Curve
from flet.charts.types import GridLines

from flet.control import Control, MainAxisAlignment, OptionalNumber
from flet.ref import Ref
from flet.types import PaddingValue


class LineChartAxisLabel(Control):
    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        value: OptionalNumber = None,
        label: Optional[Control] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

    def _get_control_name(self):
        return "l"

    def _get_children(self):
        children = []
        return children
