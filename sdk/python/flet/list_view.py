from typing import List, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import PaddingValue


class ListView(ConstrainedControl):
    def __init__(
        self,
        controls: List[Control] = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        horizontal: bool = None,
        spacing: OptionalNumber = None,
        item_extent: OptionalNumber = None,
        first_item_prototype: bool = None,
        divider_thickness: OptionalNumber = None,
        padding: PaddingValue = None,
        auto_scroll: bool = None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.__controls: List[Control] = []
        self.controls = controls
        self.horizontal = horizontal
        self.spacing = spacing
        self.divider_thickness = divider_thickness
        self.item_extent = item_extent
        self.first_item_prototype = first_item_prototype
        self.padding = padding
        self.auto_scroll = auto_scroll

    def _get_control_name(self):
        return "listview"

    def _before_build_command(self):
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        return self.__controls

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # horizontal
    @property
    def horizontal(self):
        return self._get_attr("horizontal")

    @horizontal.setter
    @beartype
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # spacing
    @property
    def spacing(self):
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # divider_thickness
    @property
    def divider_thickness(self):
        return self._get_attr("dividerThickness")

    @divider_thickness.setter
    @beartype
    def divider_thickness(self, value: OptionalNumber):
        self._set_attr("dividerThickness", value)

    # item_extent
    @property
    def item_extent(self):
        return self._get_attr("itemExtent")

    @item_extent.setter
    @beartype
    def item_extent(self, value: OptionalNumber):
        self._set_attr("itemExtent", value)

    # first_item_prototype
    @property
    def first_item_prototype(self):
        return self._get_attr("firstItemPrototype")

    @first_item_prototype.setter
    @beartype
    def first_item_prototype(self, value: Optional[bool]):
        self._set_attr("firstItemPrototype", value)

    # padding
    @property
    def padding(self):
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    def controls(self, value):
        self.__controls = value or []

    # auto_scroll
    @property
    def auto_scroll(self):
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)
