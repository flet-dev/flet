from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    OffsetValue,
)


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
        content: Optional[Control] = None,
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
        offset: OffsetValue = None,
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
        self.content = content
        self.offset = offset

    def _get_control_name(self):
        return "badge"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("offset", self.__offset)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # label
    @property
    def label(self) -> Optional[str]:
        return self._get_attr("label")

    @label.setter
    def label(self, value: Optional[str]):
        self._set_attr("label", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value
