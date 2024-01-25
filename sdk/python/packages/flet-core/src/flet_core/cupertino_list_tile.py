from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CupertinoListTile(ConstrainedControl):
    """
    A single fixed-height row that typically contains some text as well as a leading or trailing icon.

    Example:

    ```
    import flet as ft

    def main(page):
        page.title = "ListTile Example"
        page.add(
            ft.Card(
                content=ft.Container(
                    width=500,
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text("One-line list tile"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.SETTINGS),
                                title=ft.Text("One-line selected list tile"),
                                selected=True,
                            ),
                        ],
                        spacing=0,
                    ),
                    padding=ft.padding.symmetric(vertical=10),
                )
            )
        )

    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/listtile
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        # content_padding: PaddingValue = None,
        bgcolor: Optional[str] = None,
        bgcolor_activated: Optional[str] = None,
        leading: Optional[Control] = None,
        padding: PaddingValue = None,
        title: Optional[Control] = None,
        subtitle: Optional[Control] = None,
        trailing: Optional[Control] = None,
        # is_three_line: Optional[bool] = None,
        # selected: Optional[bool] = None,
        # dense: Optional[bool] = None,
        # autofocus: Optional[bool] = None,
        # toggle_inputs: Optional[bool] = None,
        url: Optional[str] = None,
        url_target: Optional[str] = None,
        additional_info: Optional[Control] = None,
        leading_size: OptionalNumber = None,
        leading_to_title: OptionalNumber = None,
        on_click=None,
        # on_long_press=None,
    ):
        ConstrainedControl.__init__(
            self,
            ref=ref,
            key=key,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        # self.content_padding = content_padding
        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.bgcolor = bgcolor
        self.bgcolor_activated = bgcolor_activated
        # self.is_three_line = is_three_line
        # self.selected = selected
        # self.dense = dense
        # self.autofocus = autofocus
        # self.toggle_inputs = toggle_inputs
        self.url = url
        self.url_target = url_target
        self.additional_info = additional_info
        self.leading_size = leading_size
        self.leading_to_title = leading_to_title
        self.padding = padding
        self.on_click = on_click
        # self.on_long_press = on_long_press

    def _get_control_name(self):
        return "cupertinolisttile"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("contentPadding", self.__padding)

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        if self.__subtitle:
            self.__subtitle._set_attr_internal("n", "subtitle")
            children.append(self.__subtitle)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        if self.__additional_info:
            self.__additional_info._set_attr_internal("n", "additionalInfo")
            children.append(self.__additional_info)
        return children

    # # content_padding
    # @property
    # def content_padding(self) -> PaddingValue:
    #     return self.__content_padding

    # @content_padding.setter
    # def content_padding(self, value: PaddingValue):
    #     self.__content_padding = value

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # subtitle
    @property
    def subtitle(self) -> Optional[Control]:
        return self.__subtitle

    @subtitle.setter
    def subtitle(self, value: Optional[Control]):
        self.__subtitle = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # additional_info
    @property
    def additional_info(self) -> Optional[Control]:
        return self.__additional_info

    @additional_info.setter
    def additional_info(self, value: Optional[Control]):
        self.__additional_info = value

    # bgcolor
    @property
    def bgcolor(self):
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value):
        self._set_attr("bgcolor", value)

    # bgcolor_activated
    @property
    def bgcolor_activated(self):
        return self._get_attr("bgcolorActivated")

    @bgcolor_activated.setter
    def bgcolor_activated(self, value):
        self._set_attr("bgcolorActivated", value)

    # leading_size
    @property
    def leading_size(self):
        return self._get_attr("leadingSize")

    @leading_size.setter
    def leading_size(self, value):
        self._set_attr("leadingSize", value)

    # leading_to_title
    @property
    def leading_to_title(self):
        return self._get_attr("leadingToTitle")

    @leading_to_title.setter
    def leading_to_title(self, value):
        self._set_attr("leadingToTitle", value)

    # # is_three_line
    # @property
    # def is_three_line(self) -> Optional[bool]:
    #     return self._get_attr("isThreeLine", data_type="bool", def_value=False)

    # @is_three_line.setter
    # def is_three_line(self, value: Optional[bool]):
    #     self._set_attr("isThreeLine", value)

    # url
    @property
    def url(self):
        return self._get_attr("url")

    @url.setter
    def url(self, value):
        self._set_attr("url", value)

    # url_target
    @property
    def url_target(self):
        return self._get_attr("urlTarget")

    @url_target.setter
    def url_target(self, value):
        self._set_attr("urlTarget", value)

    # on_click
    @property
    def on_click(self):
        return self._get_event_handler("click")

    @on_click.setter
    def on_click(self, handler):
        self._add_event_handler("click", handler)
        if handler is not None:
            self._set_attr("onclick", True)
        else:
            self._set_attr("onclick", None)

    # # on_long_press
    # @property
    # def on_long_press(self):
    #     return self._get_event_handler("long_press")

    # @on_long_press.setter
    # def on_long_press(self, handler):
    #     self._add_event_handler("long_press", handler)
    #     self._set_attr("onLongPress", True if handler is not None else None)
