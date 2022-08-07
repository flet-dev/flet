from typing import Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue

try:
    from typing import Literal
except:
    from typing_extensions import Literal

MarkdownExtensionSet = Literal[
    None, "none", "commonMark", "gitHubWeb", "gitHubFlavored"
]


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
        rotate: RotateValue = None,
        scale: ScaleValue = None,
        offset: OffsetValue = None,
        animate_opacity: AnimationValue = None,
        animate_size: AnimationValue = None,
        animate_position: AnimationValue = None,
        animate_rotation: AnimationValue = None,
        animate_scale: AnimationValue = None,
        animate_offset: AnimationValue = None,
        tooltip: str = None,
        visible: bool = None,
        disabled: bool = None,
        data: any = None,
        #
        # Specific
        #
        selectable: bool = None,
        extension_set: MarkdownExtensionSet = None,
        on_tap_link=None,
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
            rotate=rotate,
            scale=scale,
            offset=offset,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.value = value
        self.selectable = selectable
        self.extension_set = extension_set
        self.on_tap_link = on_tap_link

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

    # extension_set
    @property
    def extension_set(self):
        return self._get_attr("extensionSet")

    @extension_set.setter
    @beartype
    def extension_set(self, value: Optional[MarkdownExtensionSet]):
        self._set_attr("extensionSet", value)

    # on_tap_link
    @property
    def on_tap_link(self):
        return self._get_event_handler("tap_link")

    @on_tap_link.setter
    def on_tap_link(self, handler):
        self._add_event_handler("tap_link", handler)
