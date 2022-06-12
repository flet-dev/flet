from typing import Optional, Union

from beartype import beartype

from flet import border_radius
from flet.border_radius import BorderRadius
from flet.control import BorderRadiusValue, Control, OptionalNumber
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal


ImageFit = Literal[
    None, "none", "contain", "cover", "fill", "fitHeight", "fitWidth", "scaleDown"
]

ImageRepeat = Literal[None, "noRepeat", "repeat", "repeatX", "repeatY"]


class Image(Control):
    def __init__(
        self,
        ref: Ref = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        expand: Union[bool, int] = None,
        opacity: OptionalNumber = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        src: str = None,
        repeat: ImageRepeat = None,
        fit: ImageFit = None,
        border_radius: BorderRadiusValue = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.width = width
        self.height = height
        self.src = src
        self.fit = fit
        self.repeat = repeat
        self.border_radius = border_radius

    def _get_control_name(self):
        return "image"

    # src
    @property
    def src(self):
        return self._get_attr("src")

    @src.setter
    def src(self, value):
        self._set_attr("src", value)

    # fit
    @property
    def fit(self):
        return self._get_attr("fit")

    @fit.setter
    @beartype
    def fit(self, value: ImageFit):
        self._set_attr("fit", value)

    # repeat
    @property
    def repeat(self):
        return self._get_attr("repeat")

    @repeat.setter
    @beartype
    def repeat(self, value: ImageRepeat):
        self._set_attr("repeat", value)

    # width
    @property
    def width(self) -> OptionalNumber:
        return self._get_attr("width")

    @width.setter
    @beartype
    def width(self, value: OptionalNumber):
        self._set_attr("width", value)

    # height
    @property
    def height(self):
        return self._get_attr("height")

    @height.setter
    @beartype
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # border_radius
    @property
    def border_radius(self):
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value
        if value and isinstance(value, (int, float)):
            value = border_radius.all(value)
        self._set_attr_json("borderRadius", value)
