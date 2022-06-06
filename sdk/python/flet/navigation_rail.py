from typing import Optional, Union

from beartype import beartype
from beartype.typing import List

from flet import padding
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber, PaddingValue
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

NavigationRailLabelType = Literal[None, "none", "all", "selected"]


class NavigationRailDestination(Control):
    def __init__(
        self,
        ref: Ref = None,
        icon: str = None,
        icon_content: Control = None,
        selected_icon: str = None,
        selected_icon_content: Control = None,
        label: str = None,
        label_content: Control = None,
        padding: PaddingValue = None,
    ):
        Control.__init__(self, ref=ref)
        self.label = label
        self.icon = icon
        self.__icon_content: Control = None
        self.icon_content = icon_content
        self.selected_icon = selected_icon
        self.__selected_icon_content: Control = None
        self.selected_icon_content = selected_icon_content
        self.__label_content: Control = None
        self.label_content = label_content
        self.padding = padding

    def _get_control_name(self):
        return "navigationraildestination"

    def _get_children(self):
        children = []
        if self.__label_content:
            self.__label_content._set_attr_internal("n", "label_content")
            children.append(self.__label_content)
        if self.__icon_content:
            self.__icon_content._set_attr_internal("n", "icon_content")
            children.append(self.__icon_content)
        if self.__selected_icon_content:
            self.__selected_icon_content._set_attr_internal(
                "n", "selected_icon_content"
            )
            children.append(self.__selected_icon_content)
        return children

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_content
    @property
    def icon_content(self):
        return self.__icon_content

    @icon_content.setter
    @beartype
    def icon_content(self, value: Optional[Control]):
        self.__icon_content = value

    # selected_icon
    @property
    def selected_icon(self):
        return self._get_attr("selectedIcon")

    @selected_icon.setter
    def selected_icon(self, value):
        self._set_attr("selectedIcon", value)

    # selected_icon_content
    @property
    def selected_icon_content(self):
        return self.__selected_icon_content

    @selected_icon_content.setter
    @beartype
    def selected_icon_content(self, value: Optional[Control]):
        self.__selected_icon_content = value

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # label_content
    @property
    def label_content(self):
        return self.__label_content

    @label_content.setter
    @beartype
    def label_content(self, value: Optional[Control]):
        self.__label_content = value

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value
        if value and isinstance(value, (int, float)):
            value = padding.all(value)
        self._set_attr_json("padding", value)


class NavigationRail(ConstrainedControl):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # NavigationRail-specific
        destinations: List[NavigationRailDestination] = None,
        selected_index: int = None,
        extended: bool = None,
        label_type: NavigationRailLabelType = None,
        bgcolor: str = None,
        leading: Control = None,
        trailing: Control = None,
        min_width: OptionalNumber = None,
        min_extended_width: OptionalNumber = None,
        group_alignment: OptionalNumber = None,
        on_change=None,
    ):

        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.destinations = destinations
        self.selected_index = selected_index
        self.extended = extended
        self.label_type = label_type
        self.bgcolor = bgcolor
        self.__leading = None
        self.leading = leading
        self.__trailing = trailing
        self.trailing = trailing
        self.min_width = min_width
        self.min_extended_width = min_extended_width
        self.group_alignment = group_alignment
        self.on_change = on_change

    def _get_control_name(self):
        return "navigationrail"

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        children.extend(self.__destinations)
        return children

    # destinations
    @property
    def destinations(self):
        return self.__destinations

    @destinations.setter
    @beartype
    def destinations(self, value: Optional[List[NavigationRailDestination]]):
        value = value or []
        self.__destinations = value

    # on_change
    @property
    def on_change(self):
        return self._get_event_handler("change")

    @on_change.setter
    def on_change(self, handler):
        self._add_event_handler("change", handler)

    # selected_index
    @property
    def selected_index(self):
        return self._get_attr("selectedIndex", data_type="int")

    @selected_index.setter
    @beartype
    def selected_index(self, value: Optional[int]):
        self._set_attr("selectedIndex", value)

    # label_type
    @property
    def label_type(self):
        return self._get_attr("labelType")

    @label_type.setter
    @beartype
    def label_type(self, value: NavigationRailLabelType):
        self._set_attr("labelType", value)

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # extended
    @property
    def extended(self):
        return self._get_attr("extended", data_type="bool", def_value=False)

    @extended.setter
    @beartype
    def extended(self, value: Optional[bool]):
        self._set_attr("extended", value)

    # leading
    @property
    def leading(self):
        return self.__leading

    @leading.setter
    @beartype
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # trailing
    @property
    def trailing(self):
        return self.__trailing

    @trailing.setter
    @beartype
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # min_width
    @property
    def min_width(self):
        return self._get_attr("minWidth")

    @min_width.setter
    @beartype
    def min_width(self, value: OptionalNumber):
        self._set_attr("minWidth", value)

    # min_extended_width
    @property
    def min_extended_width(self):
        return self._get_attr("minExtendedWidth")

    @min_extended_width.setter
    @beartype
    def min_extended_width(self, value: OptionalNumber):
        self._set_attr("minExtendedWidth", value)

    # group_alignment
    @property
    def group_alignment(self):
        return self._get_attr("groupAlignment")

    @group_alignment.setter
    @beartype
    def group_alignment(self, value: OptionalNumber):
        self._set_attr("groupAlignment", value)
