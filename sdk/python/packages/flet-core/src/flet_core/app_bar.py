from typing import List, Optional

from flet_core.adaptive_control import AdaptiveControl
from flet_core.buttons import OutlinedBorder
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import ClipBehavior


class AppBar(AdaptiveControl):
    """
    A material design app bar.

    Example:
    ```
    import flet as ft

    def main(page: ft.Page):
        def check_item_clicked(e):
            e.control.checked = not e.control.checked
            page.update()

        page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Example"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item", checked=False, on_click=check_item_clicked
                        ),
                    ]
                ),
            ],
        )
        page.add(ft.Text("Body!"))

    ft.app(target=main)

    ```

    -----

    Online docs: https://flet.dev/docs/controls/appbar
    """

    def __init__(
        self,
        leading: Optional[Control] = None,
        leading_width: OptionalNumber = None,
        automatically_imply_leading: Optional[bool] = None,
        title: Optional[Control] = None,
        center_title: Optional[bool] = None,
        toolbar_height: OptionalNumber = None,
        color: Optional[str] = None,
        bgcolor: Optional[str] = None,
        elevation: OptionalNumber = None,
        elevation_on_scroll: OptionalNumber = None,
        shadow_color: Optional[str] = None,
        surface_tint_color: Optional[str] = None,
        clip_behavior: Optional[ClipBehavior] = None,
        force_material_transparency: Optional[bool] = None,
        is_secondary: Optional[bool] = None,
        title_spacing: OptionalNumber = None,
        exclude_header_semantics: Optional[bool] = None,
        actions: Optional[List[Control]] = None,
        toolbar_opacity: OptionalNumber = None,
        title_text_style: Optional[TextStyle] = None,
        toolbar_text_style: Optional[TextStyle] = None,
        shape: Optional[OutlinedBorder] = None,
        #
        # AdaptiveControl
        #
        ref: Optional[Ref] = None,
        adaptive: Optional[bool] = None,
    ):
        Control.__init__(self, ref=ref)

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.__leading: Optional[Control] = None
        self.__title: Optional[Control] = None
        self.__actions: List[Control] = []

        self.leading = leading
        self.leading_width = leading_width
        self.automatically_imply_leading = automatically_imply_leading
        self.title = title
        self.center_title = center_title
        self.toolbar_height = toolbar_height
        self.color = color
        self.bgcolor = bgcolor
        self.elevation = elevation
        self.actions = actions
        self.elevation_on_scroll = elevation_on_scroll
        self.shadow_color = shadow_color
        self.surface_tint_color = surface_tint_color
        self.clip_behavior = clip_behavior
        self.force_material_transparency = force_material_transparency
        self.is_secondary = is_secondary
        self.title_spacing = title_spacing
        self.exclude_header_semantics = exclude_header_semantics
        self.toolbar_opacity = toolbar_opacity
        self.title_text_style = title_text_style
        self.toolbar_text_style = toolbar_text_style
        self.shape = shape

    def _get_control_name(self):
        return "appbar"

    def before_update(self):
        super().before_update()
        if isinstance(self.__title_text_style, TextStyle):
            self._set_attr_json("titleTextStyle", self.__title_text_style)
        if isinstance(self.__toolbar_text_style, TextStyle):
            self._set_attr_json("toolbarTextStyle", self.__toolbar_text_style)
        if isinstance(self.__shape, OutlinedBorder):
            self._set_attr_json("shape", self.__shape)

    def _get_children(self):
        children = []
        if self.__leading:
            self.__leading._set_attr_internal("n", "leading")
            children.append(self.__leading)
        if self.__title:
            self.__title._set_attr_internal("n", "title")
            children.append(self.__title)
        for action in self.__actions:
            action._set_attr_internal("n", "action")
            children.append(action)
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

    # leading_width
    @property
    def leading_width(self) -> OptionalNumber:
        return self._get_attr("leadingWidth")

    @leading_width.setter
    def leading_width(self, value: OptionalNumber):
        self._set_attr("leadingWidth", value)

    # title_spacing
    @property
    def title_spacing(self) -> OptionalNumber:
        return self._get_attr("titleSpacing", data_type="float")

    @title_spacing.setter
    def title_spacing(self, value: OptionalNumber):
        self._set_attr("titleSpacing", value)

    # toolbar_opacity
    @property
    def toolbar_opacity(self) -> OptionalNumber:
        return self._get_attr("toolbarOpacity", data_type="float", def_value=1.0)

    @toolbar_opacity.setter
    def toolbar_opacity(self, value: OptionalNumber):
        self._set_attr("toolbarOpacity", value)

    # shape
    @property
    def shape(self) -> Optional[OutlinedBorder]:
        return self.__shape

    @shape.setter
    def shape(self, value: Optional[OutlinedBorder]):
        self.__shape = value

    # title_text_style
    @property
    def title_text_style(self) -> Optional[TextStyle]:
        return self.__title_text_style

    @title_text_style.setter
    def title_text_style(self, value: Optional[TextStyle]):
        self.__title_text_style = value

    # toolbar_text_style
    @property
    def toolbar_text_style(self) -> Optional[TextStyle]:
        return self.__toolbar_text_style

    @toolbar_text_style.setter
    def toolbar_text_style(self, value: Optional[TextStyle]):
        self.__toolbar_text_style = value

    # automatically_imply_leading
    @property
    def automatically_imply_leading(self) -> Optional[bool]:
        return self._get_attr(
            "automaticallyImplyLeading", data_type="bool", def_value=True
        )

    @automatically_imply_leading.setter
    def automatically_imply_leading(self, value: Optional[bool]):
        self._set_attr("automaticallyImplyLeading", value)

    # title
    @property
    def title(self) -> Optional[Control]:
        return self.__title

    @title.setter
    def title(self, value: Optional[Control]):
        self.__title = value

    # center_title
    @property
    def center_title(self) -> Optional[bool]:
        return self._get_attr("centerTitle", data_type="bool", def_value=False)

    @center_title.setter
    def center_title(self, value: Optional[bool]):
        self._set_attr("centerTitle", value)

    # toolbar_height
    @property
    def toolbar_height(self) -> OptionalNumber:
        return self._get_attr("toolbarHeight")

    @toolbar_height.setter
    def toolbar_height(self, value: OptionalNumber):
        self._set_attr("toolbarHeight", value)

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

    # shadow_color
    @property
    def shadow_color(self) -> Optional[str]:
        return self._get_attr("shadowColor")

    @shadow_color.setter
    def shadow_color(self, value: Optional[str]):
        self._set_attr("shadowColor", value)

    # surface_tint_color
    @property
    def surface_tint_color(self) -> Optional[str]:
        return self._get_attr("surfaceTintColor")

    @surface_tint_color.setter
    def surface_tint_color(self, value: Optional[str]):
        self._set_attr("surfaceTintColor", value)

    # is_secondary
    @property
    def is_secondary(self) -> Optional[bool]:
        return self._get_attr("isSecondary", data_type="bool", def_value=False)

    @is_secondary.setter
    def is_secondary(self, value: Optional[bool]):
        self._set_attr("isSecondary", value)

    # exclude_header_semantics
    @property
    def exclude_header_semantics(self) -> Optional[bool]:
        return self._get_attr(
            "excludeHeaderSemantics", data_type="bool", def_value=False
        )

    @exclude_header_semantics.setter
    def exclude_header_semantics(self, value: Optional[bool]):
        self._set_attr("excludeHeaderSemantics", value)

    # force_material_transparency
    @property
    def force_material_transparency(self) -> Optional[bool]:
        return self._get_attr(
            "forceMaterialTransparency", data_type="bool", def_value=False
        )

    @force_material_transparency.setter
    def force_material_transparency(self, value: Optional[bool]):
        self._set_attr("forceMaterialTransparency", value)

    # elevation
    @property
    def elevation(self) -> OptionalNumber:
        return self._get_attr("elevation")

    @elevation.setter
    def elevation(self, value: OptionalNumber):
        self._set_attr("elevation", value)

    # elevation_on_scroll
    @property
    def elevation_on_scroll(self) -> OptionalNumber:
        return self._get_attr("elevationOnScroll")

    @elevation_on_scroll.setter
    def elevation_on_scroll(self, value: OptionalNumber):
        self._set_attr("elevationOnScroll", value)

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self._get_attr("clipBehavior")

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self._set_attr(
            "clipBehavior",
            value.value if isinstance(value, ClipBehavior) else value,
        )

    # actions
    @property
    def actions(self) -> Optional[List[Control]]:
        return self.__actions

    @actions.setter
    def actions(self, value: Optional[List[Control]]):
        self.__actions = value if value is not None else []
