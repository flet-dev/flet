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
        An iOS-style list tile. The CupertinoListTile is a Cupertino equivalent of Material ListTile.

        Example:

        ```
    import flet as ft


    def main(page: ft.Page):
        def tile_clicked(e):
            print("Tile Clicked!")

        page.add(
            ft.CupertinoListTile(
                notched=True,
                additional_info=ft.Text("Wed Jan 25"),
                bgcolor_activated=ft.colors.AMBER_ACCENT,
                leading=ft.Icon(name=ft.cupertino_icons.GAME_CONTROLLER),
                title=ft.Text("CupertinoListTile not notched"),
                subtitle=ft.Text("Subtitle"),
                trailing=ft.Icon(name=ft.cupertino_icons.ALARM),
                on_click=tile_clicked,
            ),

        )

    ft.app(target=main)
        ```

        -----

        Online docs: https://flet.dev/docs/controls/cupertinolisttile
    """

    def __init__(
        self,
        title: Optional[Control] = None,
        subtitle: Optional[Control] = None,
        leading: Optional[Control] = None,
        trailing: Optional[Control] = None,
        bgcolor: Optional[str] = None,
        bgcolor_activated: Optional[str] = None,
        padding: PaddingValue = None,
        url: Optional[str] = None,
        url_target: Optional[str] = None,
        toggle_inputs: Optional[bool] = None,
        additional_info: Optional[Control] = None,
        leading_size: OptionalNumber = None,
        leading_to_title: OptionalNumber = None,
        notched: Optional[bool] = None,
        on_click=None,
        #
        # ConstrainedControl
        #
        ref: Optional[Ref] = None,
        key: Optional[str] = None,
        width: OptionalNumber = None,
        height: OptionalNumber = None,
        left: OptionalNumber = None,
        top: OptionalNumber = None,
        right: OptionalNumber = None,
        bottom: OptionalNumber = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
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
            expand_loose=expand_loose,
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

        self.leading = leading
        self.title = title
        self.subtitle = subtitle
        self.trailing = trailing
        self.bgcolor = bgcolor
        self.bgcolor_activated = bgcolor_activated
        self.url = url
        self.url_target = url_target
        self.toggle_inputs = toggle_inputs
        self.additional_info = additional_info
        self.leading_size = leading_size
        self.leading_to_title = leading_to_title
        self.padding = padding
        self.notched = notched
        self.on_click = on_click

    def _get_control_name(self):
        return "cupertinolisttile"

    def before_update(self):
        super().before_update()
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

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        self.__leading = value

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

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

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

    # padding
    @property
    def padding(self) -> PaddingValue:
        return self.__padding

    @padding.setter
    def padding(self, value: PaddingValue):
        self.__padding = value

    # notched
    @property
    def notched(self) -> Optional[bool]:
        return self._get_attr("notched", data_type="bool", def_value=False)

    @notched.setter
    def notched(self, value: Optional[bool]):
        self._set_attr("notched", value)

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

    # toggle_inputs
    @property
    def toggle_inputs(self) -> Optional[bool]:
        return self._get_attr("toggleInputs", data_type="bool", def_value=False)

    @toggle_inputs.setter
    def toggle_inputs(self, value: Optional[bool]):
        self._set_attr("toggleInputs", value)

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
