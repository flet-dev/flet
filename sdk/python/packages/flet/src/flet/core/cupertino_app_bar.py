from typing import Any, Optional

from flet.core.border import Border
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.types import Brightness, ColorEnums, ColorValue, PaddingValue
from flet.utils.deprecated import deprecated_property


class CupertinoAppBar(Control):
    """
    An iOS-styled application bar.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        page.theme_mode = ft.ThemeMode.LIGHT

        page.appbar = ft.CupertinoAppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            bgcolor=ft.colors.SURFACE_VARIANT,
            trailing=ft.Icon(ft.icons.WB_SUNNY_OUTLINED),
            middle=ft.Text("AppBar Example"),
        )
        page.add(ft.Text("Body!"))


    ft.app(target=main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/cupertinoappbar
    """

    def __init__(
        self,
        leading: Optional[Control] = None,
        middle: Optional[Control] = None,
        title: Optional[Control] = None,
        trailing: Optional[Control] = None,
        bgcolor: Optional[ColorValue] = None,
        automatically_imply_leading: Optional[bool] = None,
        automatically_imply_middle: Optional[bool] = None,
        automatically_imply_title: Optional[bool] = None,
        border: Optional[Border] = None,
        padding: Optional[PaddingValue] = None,
        transition_between_routes: Optional[bool] = None,
        previous_page_title: Optional[str] = None,
        brightness: Optional[Brightness] = None,
        automatic_background_visibility: Optional[bool] = None,
        enable_background_filter_blur: Optional[bool] = None,
        large: Optional[bool] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
    ):
        Control.__init__(
            self, ref=ref, visible=visible, disabled=disabled, data=data, rtl=rtl
        )

        self.leading = leading
        self.middle = middle
        self.title = title
        self.automatically_imply_leading = automatically_imply_leading
        self.automatically_imply_middle = automatically_imply_middle
        self.automatically_imply_title = automatically_imply_title
        self.border = border
        self.padding = padding
        self.trailing = trailing
        self.transition_between_routes = transition_between_routes
        self.previous_page_title = previous_page_title
        self.bgcolor = bgcolor
        self.brightness = brightness
        self.automatic_background_visibility = automatic_background_visibility
        self.enable_background_filter_blur = enable_background_filter_blur
        self.large = large

    def _get_control_name(self):
        return "cupertinoappbar"

    def before_update(self):
        super().before_update()
        self._set_attr_json("border", self.__border)
        self._set_attr_json("padding", self.__padding)

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title or self.__middle:
            t = self.__title or self.__middle
            t._set_attr_internal("n", "title")
            children.append(t)
        if self.__trailing:
            self.__trailing._set_attr_internal("n", "trailing")
            children.append(self.__trailing)
        return children

    # leading
    @property
    def leading(self) -> Optional[Control]:
        return self.__leading

    @leading.setter
    def leading(self, value: Optional[Control]):
        """
        A Control to display before the toolbar's title.

        Typically the leading control is an Icon or an IconButton.
        """
        self.__leading = value

    # middle
    @property
    def middle(self) -> Optional[Control]:
        deprecated_property(
            name="middle",
            version="0.27.0",
            delete_version="0.30.0",
            reason="Use title instead.",
        )
        return self.__middle

    @middle.setter
    def middle(self, value: Optional[Control]):
        self.__middle = value
        if value is not None:
            deprecated_property(
                name="middle",
                version="0.27.0",
                delete_version="0.30.0",
                reason="Use title instead.",
            )

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__padding = value

    # automatically_imply_leading
    @property
    def automatically_imply_leading(self) -> bool:
        return self._get_attr(
            "automaticallyImplyLeading", data_type="bool", def_value=True
        )

    @automatically_imply_leading.setter
    def automatically_imply_leading(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyLeading", value)

    # automatically_imply_middle
    @property
    def automatically_imply_middle(self) -> bool:
        deprecated_property(
            name="automatically_imply_middle",
            version="0.27.0",
            delete_version="0.30.0",
            reason="Use automatically_imply_title instead.",
        )
        return self._get_attr(
            "automaticallyImplyMiddle", data_type="bool", def_value=True
        )

    @automatically_imply_middle.setter
    def automatically_imply_middle(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyMiddle", value)
        if value is not None:
            deprecated_property(
                name="automatically_imply_middle",
                version="0.27.0",
                delete_version="0.30.0",
                reason="Use automatically_imply_title instead.",
            )

    # automatically_imply_title
    @property
    def automatically_imply_title(self) -> bool:
        return self._get_attr(
            "automaticallyImplyTitle", data_type="bool", def_value=True
        )

    @automatically_imply_title.setter
    def automatically_imply_title(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyTitle", value)

    # large
    @property
    def large(self) -> bool:
        return self._get_attr("large", data_type="bool", def_value=False)

    @large.setter
    def large(self, value: Optional[bool]):
        self._set_attr("large", value)

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # trailing
    @property
    def trailing(self) -> Optional[Control]:
        return self.__trailing

    @trailing.setter
    def trailing(self, value: Optional[Control]):
        self.__trailing = value

    # transition_between_routes
    @property
    def transition_between_routes(self) -> bool:
        return self._get_attr(
            "transitionBetweenRoutes", data_type="bool", def_value=True
        )

    @transition_between_routes.setter
    def transition_between_routes(self, value: Optional[bool]):
        self._set_attr("transitionBetweenRoutes", value)

    # previous_page_title
    @property
    def previous_page_title(self):
        return self._get_attr("previousPageTitle")

    @previous_page_title.setter
    def previous_page_title(self, value):
        self._set_attr("previousPageTitle", value)

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__bgcolor = value
        self._set_enum_attr("bgcolor", value, ColorEnums)

    # brightness
    @property
    def brightness(self) -> Optional[Brightness]:
        return self.__brightness

    @brightness.setter
    def brightness(self, value: Optional[Brightness]):
        self.__brightness = value
        self._set_enum_attr("brightness", value, Brightness)

    # automatic_background_visibility
    @property
    def automatic_background_visibility(self) -> Optional[bool]:
        return self._get_attr(
            "automaticBackgroundVisibility", data_type="bool", def_value=True
        )

    @automatic_background_visibility.setter
    def automatic_background_visibility(self, value: Optional[bool]):
        self._set_attr("automaticBackgroundVisibility", value)

    # enable_background_filter_blur
    @property
    def enable_background_filter_blur(self) -> Optional[bool]:
        return self._get_attr("backgroundFilterBlur", data_type="bool", def_value=True)

    @enable_background_filter_blur.setter
    def enable_background_filter_blur(self, value: Optional[bool]):
        self._set_attr("backgroundFilterBlur", value)
