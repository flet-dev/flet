from typing import Optional

from beartype import beartype
from beartype.typing import List

from flet.control import Control, OptionalNumber
from flet.ref import Ref


class AppBar(Control):
    def __init__(
        self,
        ref: Ref = None,
        leading: Control = None,
        leading_width: OptionalNumber = None,
        title: Control = None,
        center_title: bool = None,
        toolbar_height: OptionalNumber = None,
        color: str = None,
        bgcolor: str = None,
        actions: List[Control] = None,
    ):
        Control.__init__(self, ref=ref)

        self.__leading: Control = None
        self.__title: Control = None
        self.__actions: List[Control] = []

        self.leading = leading
        self.leading_width = leading_width
        self.title = title
        self.center_title = center_title
        self.toolbar_height = toolbar_height
        self.color = color
        self.bgcolor = bgcolor
        self.actions = actions

    def _get_control_name(self):
        return "appbar"

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # leading
    @property
    def leading(self):
        return self.__leading

    @leading.setter
    @beartype
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # leading_width
    @property
    def leading_width(self):
        return self._get_attr("leadingWidth")

    @leading_width.setter
    @beartype
    def leading_width(self, value: OptionalNumber):
        self._set_attr("leadingWidth", value)

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    @beartype
    def title(self, value: Optional[Control]):
        self.__title = value

    # center_title
    @property
    def center_title(self):
        return self._get_attr("centerTitle", data_type="bool", def_value=False)

    @center_title.setter
    @beartype
    def center_title(self, value: Optional[bool]):
        self._set_attr("centerTitle", value)

    # toolbar_height
    @property
    def toolbar_height(self):
        return self._get_attr("toolbarHeight")

    @toolbar_height.setter
    @beartype
    def toolbar_height(self, value: OptionalNumber):
        self._set_attr("toolbarHeight", value)

    # color
    @property
    def color(self):
        return self._get_attr("color")

    @color.setter
    def color(self, value):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value or []
