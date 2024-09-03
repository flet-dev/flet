from typing import Any, Optional

from flet_core.alignment import Alignment
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import OffsetValue, PaddingValue


class Badge(Control):
    """
    A Material Design "badge".

    Badges are used to show notifications, counts, or status information on navigation items such as NavigationBar or NavigationRail destinations
    or a button's icon.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.title = "Badges in NavigationBar icons"
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationDestination(
                    icon_content=ft.Badge(
                        content=ft.Icon(ft.icons.EXPLORE),
                        small_size=10,
                    ),
                    label="Explore",
                ),
                ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
                ft.NavigationDestination(
                    icon_content=ft.Badge(content=ft.Icon(ft.icons.PHONE), text="10")
                ),
            ]
        )
        page.add(ft.Text("Body!"))


    ft.app(target=main)



    ```

    -----

    Online docs: https://flet.dev/docs/controls/badge
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        text: Optional[str] = None,
        offset: OffsetValue = None,
        alignment: Optional[Alignment] = None,
        bgcolor: Optional[str] = None,
        label_visible: Optional[bool] = None,
        large_size: OptionalNumber = None,
        padding: Optional[PaddingValue] = None,
        small_size: OptionalNumber = None,
        text_color: Optional[str] = None,
        text_style: Optional[TextStyle] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        self.text = text
        self.content = content
        self.offset = offset
        self.alignment = alignment
        self.bgcolor = bgcolor
        self.label_visible = label_visible
        self.large_size = large_size
        self.padding = padding
        self.small_size = small_size
        self.text_color = text_color
        self.text_style = text_style

    def _get_control_name(self):
        return "badge"

    def before_update(self):
        super().before_update()
        self._set_attr_json("offset", self.__offset)
        self._set_attr_json("alignment", self.__alignment)
        self._set_attr_json("padding", self.__padding)
        self._set_attr_json("textStyle", self.__text_style)

    def _get_children(self):
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            return [self.__content]
        return []

    # alignment
    @property
    def alignment(self) -> Optional[Alignment]:
        """:obj:`Alignment`, optional: Align the child control within the container.

        Alignment is an instance of `alignment.Alignment` class object with `x` and `y` properties
        representing the distance from the center of a rectangle.
        """
        return self.__alignment

    @alignment.setter
    def alignment(self, value: Optional[Alignment]):
        self.__alignment = value

    # text
    @property
    def text(self) -> Optional[str]:
        return self._get_attr("labelText")

    @text.setter
    def text(self, value: Optional[str]):
        self._set_attr("labelText", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # offset
    @property
    def offset(self) -> OffsetValue:
        return self.__offset

    @offset.setter
    def offset(self, value: OffsetValue):
        self.__offset = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgColor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgColor", value)

    # label_visible
    @property
    def label_visible(self) -> bool:
        return self._get_attr("isLabelVisible", data_type="bool", def_value=True)

    @label_visible.setter
    def label_visible(self, value: Optional[bool]):
        self._set_attr("isLabelVisible", value)

    # large_size
    @property
    def large_size(self) -> OptionalNumber:
        return self._get_attr("largeSize")

    @large_size.setter
    def large_size(self, value: OptionalNumber):
        self._set_attr("largeSize", value)

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # small_size
    @property
    def small_size(self) -> OptionalNumber:
        return self._get_attr("smallSize")

    @small_size.setter
    def small_size(self, value: OptionalNumber):
        self._set_attr("smallSize", value)

    # text_color
    @property
    def text_color(self) -> Optional[str]:
        return self._get_attr("textColor")

    @text_color.setter
    def text_color(self, value: Optional[str]):
        self._set_attr("textColor", value)

    # text_style
    @property
    def text_style(self) -> Optional[TextStyle]:
        return self.__text_style

    @text_style.setter
    def text_style(self, value: Optional[TextStyle]):
        self.__text_style = value
