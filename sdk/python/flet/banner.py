from typing import List, Optional

from beartype import beartype

from flet import padding
from flet.control import Control, PaddingValue
from flet.ref import Ref


class Banner(Control):
    def __init__(
        self,
        ref: Ref = None,
        disabled: bool = None,
        visible: bool = None,
        data: any = None,
        #
        # Specific
        #
        open: bool = False,
        leading: Control = None,
        leading_padding: PaddingValue = None,
        content: Control = None,
        content_padding: PaddingValue = None,
        actions: List[Control] = None,
        force_actions_below: bool = None,
        bgcolor: str = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.__leading: Control = None
        self.__content: Control = None
        self.__actions = []

        self.open = open
        self.leading = leading
        self.leading_padding = leading_padding
        self.content = content
        self.content_padding = content_padding
        self.actions = actions
        self.force_actions_below = force_actions_below
        self.bgcolor = bgcolor

    def _get_control_name(self):
        return "banner"

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__content:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
        return children

    # open
    @property
    def open(self):
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    @beartype
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # modal
    @property
    def modal(self):
        return self._get_attr("modal", data_type="bool", def_value=False)

    @modal.setter
    @beartype
    def modal(self, value: Optional[bool]):
        self._set_attr("modal", value)

    # leading
    @property
    def leading(self):
        return self.__leading

    @leading.setter
    def leading(self, value):
        self.__leading = value

    # leading_padding
    @property
    def leading_padding(self):
        return self.__leading_padding

    @leading_padding.setter
    @beartype
    def leading_padding(self, value: PaddingValue):
        self.__leading_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("leadingPadding", value)

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # content_padding
    @property
    def content_padding(self):
        return self.__content_padding

    @content_padding.setter
    @beartype
    def content_padding(self, value: PaddingValue):
        self.__content_padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("contentPadding", value)

    # actions
    @property
    def actions(self):
        return self.__actions

    @actions.setter
    def actions(self, value):
        self.__actions = value or []

    # force_actions_below
    @property
    def force_actions_below(self):
        return self._get_attr("forceActionsBelow", data_type="bool", def_value=False)

    @force_actions_below.setter
    @beartype
    def force_actions_below(self, value: Optional[bool]):
        self._set_attr("forceActionsBelow", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    @beartype
    def bgcolor(self, value):
        self._set_attr("bgColor", value)
