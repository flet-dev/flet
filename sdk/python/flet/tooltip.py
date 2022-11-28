from typing import Any, Optional, Union

from beartype import beartype

from flet.border import Border
from flet.control import Control, OptionalNumber
from flet.gradients import Gradient
from flet.ref import Ref
from flet.text_style import TextStyle
from flet.types import (
    BorderRadiusValue,
    BoxShape,
    MarginValue,
    PaddingValue,
    TextAlign,
    TextAlignString,
)


class Tooltip(Control):
    """
    Tooltips provide text labels which help explain the function of a button or other user interface action. Wrap the button in a Tooltip control and provide a message which will be shown when the control is long pressed.

    Example:
    ```
    import math

    import flet as ft
    from flet import alignment

    def main(page: ft.Page):
        page.title = "Tooltip Example"
        page.add(
            ft.Tooltip(
                message="This is tooltip",
                content=ft.Text("Hover to see tooltip"),
                padding=20,
                border_radius=10,
                text_style=ft.TextStyle(size=20, color=ft.colors.WHITE),
                gradient=ft.LinearGradient(
                    begin=alignment.top_left,
                    end=alignment.Alignment(0.8, 1),
                    colors=[
                        "0xff1f005c",
                        "0xff5b0060",
                        "0xff870160",
                        "0xffac255e",
                        "0xffca485c",
                        "0xffe16b5c",
                        "0xfff39060",
                        "0xffffb56b",
                    ],
                    tile_mode=ft.GradientTileMode.MIRROR,
                    rotation=math.pi / 3,
                ),
            )
        )


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/tooltip
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        content: Optional[Control] = None,
        enable_feedback: Optional[bool] = None,
        height: OptionalNumber = None,
        vertical_offset: OptionalNumber = None,
        margin: MarginValue = None,
        padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        gradient: Optional[Gradient] = None,
        border: Optional[Border] = None,
        border_radius: BorderRadiusValue = None,
        shape: Optional[BoxShape] = None,
        message: Optional[str] = None,
        text_style: Optional[TextStyle] = None,
        text_align: TextAlign = TextAlign.NONE,
        prefer_below: Optional[bool] = None,
        show_duration: Optional[int] = None,
        wait_duration: Optional[int] = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.enable_feedback = enable_feedback
        self.height = height
        self.vertical_offset = vertical_offset
        self.margin = margin
        self.padding = padding
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.border = border
        self.border_radius = border_radius
        self.shape = shape
        self.message = message
        self.text_style = text_style
        self.text_align = text_align
        self.prefere_below = prefer_below
        self.show_duration = show_duration
        self.wait_duration = wait_duration

    def _get_control_name(self):
        return "tooltip"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("margin", self.__margin)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("textStyle", self.__text_style)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("border", self.__border)
        self._set_attr_json("gradient", self.__gradient)

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # enable_feedback
    @property
    def enable_feedback(self) -> Optional[bool]:
        return self._get_attr("enableFeedback", data_type="bool", def_value=False)

    @enable_feedback.setter
    @beartype
    def enable_feedback(self, value: Optional[bool]):
        self._set_attr("enableFeedback", value)

    # margin
    @property
    def margin(self) -> MarginValue:
        return self.__margin

    @margin.setter
    @beartype
    def margin(self, value: MarginValue):
        self.__margin = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    @beartype
    def padding(self, value: PaddingValue):
        self.__padding = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgColor", value)

    # gradient
    @property
    def gradient(self) -> Optional[Gradient]:
        return self.__gradient

    @gradient.setter
    @beartype
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    @beartype
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    @beartype
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # shape
    @property
    def shape(self):
        return self._get_attr("shape")

    @shape.setter
    @beartype
    def shape(self, value: Optional[BoxShape]):
        self._set_attr("shape", value.value if value is not None else None)

    # message
    @property
    def message(self) -> Optional[str]:
        return self._get_attr("message")

    @message.setter
    @beartype
    def message(self, value: Optional[str]):
        self._set_attr("message", value)

    # text_align
    @property
    def text_align(self) -> TextAlign:
        return self.__text_align

    @text_align.setter
    def text_align(self, value: TextAlign):
        self.__text_align = value
        if isinstance(value, TextAlign):
            self._set_attr("textAlign", value.value)
        else:
            self.__set_text_align(value)

    @beartype
    def __set_text_align(self, value: TextAlignString):
        self._set_attr("textAlign", value)

    # text_style
    @property
    def text_style(self):
        return self.__text_style

    @text_style.setter
    @beartype
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value

    # prefere_below
    @property
    def prefere_below(self) -> Optional[bool]:
        return self._get_attr("prefereBelow", data_type="bool", def_value=False)

    @prefere_below.setter
    @beartype
    def prefere_below(self, value: Optional[bool]):
        self._set_attr("prefereBelow", value)

    # height
    @property
    def height(self) -> OptionalNumber:
        return self._get_attr("height")

    @height.setter
    @beartype
    def height(self, value: OptionalNumber):
        self._set_attr("height", value)

    # vertical_offset
    @property
    def vertical_offset(self) -> OptionalNumber:
        return self._get_attr("verticalOffset")

    @vertical_offset.setter
    @beartype
    def vertical_offset(self, value: OptionalNumber):
        self._set_attr("verticalOffset", value)

    # show_duration
    @property
    def show_duration(self) -> Optional[int]:
        return self._get_attr("showDuration")

    @show_duration.setter
    @beartype
    def show_duration(self, value: Optional[int]):
        self._set_attr("showDuration", value)

    # wait_duration
    @property
    def wait_duration(self) -> Optional[int]:
        return self._get_attr("waitDuration")

    @wait_duration.setter
    @beartype
    def wait_duration(self, value: Optional[int]):
        self._set_attr("waitDuration", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    @beartype
    def content(self, value: Optional[Control]):
        self.__content = value
