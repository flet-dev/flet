import warnings
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

    If `foreground_image_src` fails then `background_image_src` is used. If `background_image_src` fails too,
    then `bgcolor` is used.

    Example:
    ```
    import flet as ft

    def main(page):
        # a "normal" avatar with background image
        a1 = ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
            content=ft.Text("FF"),
        )
        # avatar with failing foreground image and fallback text
        a2 = ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
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
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
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
        content: Optional[Control] = None,
        foreground_image_url: Optional[str] = None,
        background_image_url: Optional[str] = None,
        foreground_image_src: Optional[str] = None,
        background_image_src: Optional[str] = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        radius: OptionalNumber = None,
        min_radius: OptionalNumber = None,
        max_radius: OptionalNumber = None,
        on_image_error=None,
        #
        # ConstrainedControl
        #
        key: Optional[str] = None,
        ref: Optional[Ref] = None,
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

        self.foreground_image_url = foreground_image_url
        self.background_image_url = background_image_url
        self.foreground_image_src = foreground_image_src
        self.background_image_src = background_image_src
        self.radius = radius
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.color = color
        self.bgcolor = bgcolor
        self.content = content
        self.on_image_error = on_image_error

    def _get_control_name(self):
        return "circleavatar"

    def _get_children(self):
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            return [self.__content]
        return []

    # foreground_image_url
    @property
    def foreground_image_url(self) -> Optional[str]:
        warnings.warn(
            f"foreground_image_url is deprecated since version 0.22.0 "
            f"and will be removed in version 1.0. Use foreground_image_src instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self._get_attr("foregroundImageUrl")

    @foreground_image_url.setter
    def foreground_image_url(self, value: Optional[str]):
        self._set_attr("foregroundImageUrl", value)
        if value is not None:
            warnings.warn(
                f"foreground_image_url is deprecated since version 0.22.0 "
                f"and will be removed in version 1.0. Use foreground_image_src instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # background_image_url
    @property
    def background_image_url(self) -> Optional[str]:
        warnings.warn(
            f"background_image_url is deprecated since version 0.22.0 "
            f"and will be removed in version 1.0. Use background_image_src instead.",
            category=DeprecationWarning,
            stacklevel=2,
        )
        return self._get_attr("backgroundImageUrl")

    @background_image_url.setter
    def background_image_url(self, value: Optional[str]):
        self._set_attr("backgroundImageUrl", value)
        if value is not None:
            warnings.warn(
                f"background_image_url is deprecated since version 0.22.0 "
                f"and will be removed in version 1.0. Use background_image_src instead.",
                category=DeprecationWarning,
                stacklevel=2,
            )

    # foreground_image_src
    @property
    def foreground_image_src(self) -> Optional[str]:
        return self._get_attr("foregroundImageSrc")

    @foreground_image_src.setter
    def foreground_image_src(self, value: Optional[str]):
        self._set_attr("foregroundImageSrc", value)

    # background_image_src
    @property
    def background_image_src(self) -> Optional[str]:
        return self._get_attr("backgroundImageSrc")

    @background_image_src.setter
    def background_image_src(self, value: Optional[str]):
        self._set_attr("backgroundImageSrc", value)

    # radius
    @property
    def radius(self) -> OptionalNumber:
        return self._get_attr("radius", data_type="float")

    @radius.setter
    def radius(self, value: OptionalNumber):
        assert value is None or value >= 0, "radius cannot be negative"
        self._set_attr("radius", value)

    # min_radius
    @property
    def min_radius(self) -> OptionalNumber:
        return self._get_attr("minRadius", data_type="float")

    @min_radius.setter
    def min_radius(self, value: OptionalNumber):
        assert value is None or value >= 0, "min_radius cannot be negative"
        self._set_attr("minRadius", value)

    # max_radius
    @property
    def max_radius(self) -> OptionalNumber:
        return self._get_attr("maxRadius", data_type="float")

    @max_radius.setter
    def max_radius(self, value: OptionalNumber):
        assert value is None or value >= 0, "max_radius cannot be negative"
        self._set_attr("maxRadius", value)

    # color
    @property
    def color(self) -> Optional[str]:
        return self._get_attr("color")

    @color.setter
    def color(self, value: Optional[str]):
        self._set_attr("color", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[str]:
        return self._get_attr("bgcolor")

    @bgcolor.setter
    def bgcolor(self, value: Optional[str]):
        self._set_attr("bgcolor", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # on_image_error
    @property
    def on_image_error(self):
        return self._get_event_handler("imageError")

    @on_image_error.setter
    def on_image_error(self, handler):
        self._add_event_handler("imageError", handler)
