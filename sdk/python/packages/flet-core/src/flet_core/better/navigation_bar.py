from typing import Optional, Union, Any

from flet_core.ref import Ref
from flet_core.control import Control
from flet_core.types import ResponsiveNumber, OptionalNumber


class BetterNavigationBar(Control):
    def __init__(
        self,
        # TODO: Navigation bar arguments
        # Control
        ref: Ref,
        expand: Optional[Union[bool, int]],
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            col=col,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

    # TODO: All methods from NavigationBar and change()
