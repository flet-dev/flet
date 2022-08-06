from typing import Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref


class Markdown(ConstrainedControl):
    def __init__(
        self,
        value: str = None,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        selectable: bool = None,
        foreground_image_url: str = None,
        background_image_url: str = None,
        radius: OptionalNumber = None,
        min_radius: OptionalNumber = None,
        max_radius: OptionalNumber = None,
        color: str = None,
        bgcolor: str = None,
        content: Control = None,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.selectable = selectable
        self.foreground_image_url = foreground_image_url
        self.background_image_url = background_image_url
        self.radius = radius
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.color = color
        self.bgcolor = bgcolor
        self.content = content

    def _get_control_name(self):
        return "markdown"

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value):
        self._set_attr("value", value)

    # selectable
    @property
    def selectable(self):
        return self._get_attr("selectable", data_type="bool", def_value=False)

    @selectable.setter
    @beartype
    def selectable(self, value: Optional[bool]):
        self._set_attr("selectable", value)

    # foreground_image_url
    @property
    def foreground_image_url(self):
        return self._get_attr("foregroundImageUrl")

    @foreground_image_url.setter
    def foreground_image_url(self, value):
        self._set_attr("foregroundImageUrl", value)

    # background_image_url
    @property
    def background_image_url(self):
        return self._get_attr("backgroundImageUrl")

    @background_image_url.setter
    def background_image_url(self, value):
        self._set_attr("backgroundImageUrl", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # radius
    @property
    def radius(self):
        return self._get_attr("radius")

    @radius.setter
    def radius(self, value):
        self._set_attr("radius", value)

    # min_radius
    @property
    def min_radius(self):
        return self._get_attr("minRadius")

    @min_radius.setter
    def min_radius(self, value):
        self._set_attr("minRadius", value)

    # max_radius
    @property
    def max_radius(self):
        return self._get_attr("maxRadius")

    @max_radius.setter
    def max_radius(self, value):
        self._set_attr("maxRadius", value)

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

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
