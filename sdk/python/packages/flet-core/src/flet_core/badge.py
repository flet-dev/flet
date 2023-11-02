from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class Badge(Control):
    """
    A Material Design "badge".

    Badges are used to show notifications, counts, or status information on navigation items such as NavigationBar or NavigationRail destinations
    or a button's icon.

    Example:
        ```


        ```

        -----

        Online docs: https://flet.dev/docs/controls/badge
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        # height: OptionalNumber = None,
        # thickness: OptionalNumber = None,
        # color: Optional[str] = None,
        label: Optional[str] = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        # self.height = height
        # self.thickness = thickness
        # self.color = color
        self.label = label

    def _get_control_name(self):
        return "badge"

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)
