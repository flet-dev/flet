from typing import Any, Optional, Union

from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class CircleAvatar(ConstrainedControl):
    """
    A circle that represents a user.

    If `foreground_image_url` fails then `background_image_url` is used. If `background_image_url` fails too, `bgcolor` is used.

    Example:
    ```
    import flet as ft

    def main(page):
        # a "normal" avatar with background image
        a1 = ft.CircleAvatar(
            foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
            content=ft.Text("FF"),
        )
        # avatar with failing foreground image and fallback text
        a2 = ft.CircleAvatar(
            foreground_image_url="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
            content=ft.Text("FF"),
        )
        # avatar with icon, aka icon with inverse background
        a3 = ft.CircleAvatar(
            content=ft.Icon(ft.icons.ABC),
        )
        # avatar with icon and custom colors
        a4 = ft.CircleAvatar(
            content=ft.Icon(ft.icons.WARNING_ROUNDED),
            color=ft.colors.YELLOW_200,
            bgcolor=ft.colors.AMBER_700,
        )
        # avatar with online status
        a5 = ft.Stack(
            [
                ft.CircleAvatar(
                    foreground_image_url="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.colors.GREEN, radius=5),
                    alignment=ft.alignment.bottom_left,
                ),
            ],
            width=40,
            height=40,
        )
        page.add(a1, a2, a3, a4, a5)


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/circleavatar
    """

    def __init__(
        self,
        icon: Optional[str] = None,
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
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        foreground_image_url: Optional[str] = None,
        background_image_url: Optional[str] = None,
        radius: OptionalNumber = None,
        min_radius: OptionalNumber = None,
        max_radius: OptionalNumber = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        content: Optional[Control] = None,
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
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.foreground_image_url = foreground_image_url
        self.background_image_url = background_image_url
        self.radius = radius
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.color = color
        self.bgcolor = bgcolor
        self.content = content

    def _get_control_name(self):
        return "circleavatar"

    def _get_children(self):
        if self.__content is None:
            return []
        self.__content._set_attr_internal("n", "content")
        return [self.__content]

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
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value
