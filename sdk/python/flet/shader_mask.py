from typing import Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.gradients import Gradient
from flet.ref import Ref

try:
    from typing import Literal
except:
    from typing_extensions import Literal

BlendMode = Literal[
    "clear",
    "color",
    "colorBurn",
    "colorDodge",
    "darken",
    "difference",
    "dst",
    "dstATop",
    "dstIn",
    "dstOut",
    "dstOver",
    "exclusion",
    "hardLight",
    "hue",
    "lighten",
    "luminosity",
    "modulate",
    "multiply",
    "overlay",
    "plus",
    "saturation",
    "screen",
    "softLight",
    "src",
    "srcATop",
    "srcIn",
    "srcOut",
    "srcOver",
    "values",
    "xor",
]


class ShaderMask(ConstrainedControl):
    def __init__(
        self,
        content: Control = None,
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
        blend_mode: BlendMode = None,
        shader: Gradient = None,
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

        self.content = content
        self.blend_mode = blend_mode
        self.shader = shader

    def _get_control_name(self):
        return "shadermask"

    def _before_build_command(self):
        self._set_attr_json("shader", self.__shader)

    def _get_children(self):
        children = []
        if self.__content != None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value

    # blend_mode
    @property
    def blend_mode(self):
        return self._get_attr("blendMode")

    @blend_mode.setter
    @beartype
    def blend_mode(self, value: Optional[BlendMode]):
        self._set_attr("blendMode", value)

    # shader
    @property
    def shader(self):
        return self.__shader

    @shader.setter
    @beartype
    def shader(self, value: Optional[Gradient]):
        self.__shader = value
