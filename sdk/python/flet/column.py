from typing import Any, Optional, Union

from beartype import beartype
from beartype.typing import List

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber, ScrollMode
from flet.ref import Ref
from flet.types import (
    AnimationValue,
    CrossAxisAlignment,
    CrossAxisAlignmentString,
    MainAxisAlignment,
    MainAxisAlignmentString,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class Column(ConstrainedControl):
    def __init__(
        self,
        controls: Optional[List[Control]] = None,
        ref: Optional[Ref] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        aspect_ratio: OptionalNumber = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        on_animation_end=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Column specific
        #
        alignment: MainAxisAlignment = MainAxisAlignment.NONE,
        horizontal_alignment: CrossAxisAlignment = CrossAxisAlignment.NONE,
        spacing: OptionalNumber = None,
        tight: Optional[bool] = None,
        wrap: Optional[bool] = None,
        run_spacing: OptionalNumber = None,
        scroll: ScrollMode = None,
        auto_scroll: Optional[bool] = None,
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
            col=col,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            aspect_ratio=aspect_ratio,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            on_animation_end=on_animation_end,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.controls = controls
        self.horizontal_alignment = horizontal_alignment
        self.alignment = alignment
        self.spacing = spacing
        self.tight = tight
        self.wrap = wrap
        self.run_spacing = run_spacing
        self.scroll = scroll
        self.auto_scroll = auto_scroll

    def _get_control_name(self):
        return "column"

    def _get_children(self):
        return self.__controls

    def clean(self):
        Control.clean(self)
        self.__controls.clear()

    # tight
    @property
    def tight(self) -> Optional[bool]:
        return self._get_attr("tight", data_type="bool", def_value=False)

    @tight.setter
    @beartype
    def tight(self, value: Optional[bool]):
        self._set_attr("tight", value)

    # alignment
    @property
    def alignment(self) -> MainAxisAlignment:
        return self.__alignment

    @alignment.setter
    def alignment(self, value: MainAxisAlignment):
        self.__alignment = value
        if isinstance(value, MainAxisAlignment):
            self._set_attr("alignment", value.value)
        else:
            self.__set_alignment(value)

    @beartype
    def __set_alignment(self, value: MainAxisAlignmentString):
        self._set_attr("alignment", value)

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> CrossAxisAlignment:
        return self.__horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self.__horizontal_alignment = value
        if isinstance(value, CrossAxisAlignment):
            self._set_attr("horizontalAlignment", value.value)
        else:
            self.__set_horizontal_alignment(value)

    @beartype
    def __set_horizontal_alignment(self, value: CrossAxisAlignmentString):
        self._set_attr("horizontalAlignment", value)

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self._get_attr("spacing")

    @spacing.setter
    @beartype
    def spacing(self, value: OptionalNumber):
        self._set_attr("spacing", value)

    # wrap
    @property
    def wrap(self) -> Optional[bool]:
        return self._get_attr("wrap", data_type="bool", def_value=False)

    @wrap.setter
    @beartype
    def wrap(self, value: Optional[bool]):
        self._set_attr("wrap", value)

    # run_spacing
    @property
    def run_spacing(self) -> OptionalNumber:
        return self._get_attr("runSpacing")

    @run_spacing.setter
    @beartype
    def run_spacing(self, value: OptionalNumber):
        self._set_attr("runSpacing", value)

    # scroll
    @property
    def scroll(self):
        return self.__scroll

    @scroll.setter
    @beartype
    def scroll(self, value: ScrollMode):
        self.__scroll = value
        if value is True:
            value = "auto"
        elif value is False:
            value = "none"
        self._set_attr("scroll", value)

    # auto_scroll
    @property
    def auto_scroll(self) -> Optional[bool]:
        return self._get_attr("autoScroll")

    @auto_scroll.setter
    @beartype
    def auto_scroll(self, value: Optional[bool]):
        self._set_attr("autoScroll", value)

    # controls
    @property
    def controls(self):
        return self.__controls

    @controls.setter
    @beartype
    def controls(self, value: Optional[List[Control]]):
        self.__controls = value if value is not None else []
