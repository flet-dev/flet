from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class Placeholder(Control):
    """
    A placeholder box.

    -----

    Online docs: https://flet.dev/docs/controls/placeholder
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        color: Optional[str] = None,
        fallback_height: OptionalNumber = None,
        fallback_width: OptionalNumber = None,
        stroke_width: OptionalNumber = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            data=data,
        )

        self.content = content
        self.color = color
        self.fallback_height = fallback_height
        self.fallback_width = fallback_width
        self.stroke_width = stroke_width

    def _get_control_name(self):
        return "placeholder"

    def _get_children(self):
        return [self.content] if self.content is not None else []

    # fallback_height
    @property
    def fallback_height(self) -> OptionalNumber:
        return self._get_attr("fallbackHeight", data_type="float", def_value=400.0)

    @fallback_height.setter
    def fallback_height(self, value: OptionalNumber):
        assert value is None or value >= 0, "fallback_height cannot be negative"
        self._set_attr("fallbackHeight", value)

    # fallback_width
    @property
    def fallback_width(self) -> OptionalNumber:
        return self._get_attr("fallbackWidth", data_type="float", def_value=400.0)

    @fallback_width.setter
    def fallback_width(self, value: OptionalNumber):
        assert value is None or value >= 0, "fallback_width cannot be negative"
        self._set_attr("fallbackWidth", value)

    # stroke_width
    @property
    def stroke_width(self) -> OptionalNumber:
        return self._get_attr("strokeWidth", data_type="float", def_value=2.0)

    @stroke_width.setter
    def stroke_width(self, value: OptionalNumber):
        self._set_attr("strokeWidth", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color", def_value="bluegrey700")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
