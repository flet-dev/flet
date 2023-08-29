import json
from typing import Any, Dict, List, Optional, Union

from flet_core.border import Border, BorderSide
from flet_core.constrained_control import ConstrainedControl
from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.gesture_detector import TapEvent
from flet_core.gradients import Gradient
from flet_core.ref import Ref
from flet_core.text_style import TextStyle
from flet_core.types import (
    AnimationValue,
    BorderRadiusValue,
    MaterialState,
    OffsetValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)


class DataColumnSortEvent(ControlEvent):
    def __init__(self, i, a) -> None:
        self.column_index: int = i
        self.ascending: bool = a


class DataColumn(Control):
    def __init__(
        self,
        label: Control,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        # specific
        numeric: Optional[bool] = None,
        tooltip: Optional[str] = None,
        on_sort=None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.__on_sort = EventHandler(
            lambda e: DataColumnSortEvent(**json.loads(e.data))
        )
        self._add_event_handler("sort", self.__on_sort.get_handler())

        self.label = label
        self.numeric = numeric
        self.tooltip = tooltip
        self.on_sort = on_sort

    def _get_control_name(self):
        return "c"

    def _get_children(self):
        children = []
        if self.__label:
            self.__label._set_attr_internal("n", "l")
            children.append(self.__label)
        return children

    # label
    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        self.__label = value

    # numeric
    @property
    def numeric(self) -> Optional[bool]:
        return self._get_attr("numeric", data_type="bool", def_value=False)

    @numeric.setter
    def numeric(self, value: Optional[bool]):
        self._set_attr("numeric", value)

    # tooltip
    @property
    def tooltip(self):
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value):
        self._set_attr("tooltip", value)

    # on_sort
    @property
    def on_sort(self):
        return self.__on_sort

    @on_sort.setter
    def on_sort(self, handler):
        self.__on_sort.subscribe(handler)
        self._set_attr("onSort", True if handler is not None else None)


class DataCell(Control):
    def __init__(
        self,
        content: Control,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        # specific
        on_double_tap=None,
        on_long_press=None,
        on_tap=None,
        on_tap_cancel=None,
        on_tap_down=None,
        placeholder: Optional[bool] = None,
        show_edit_icon: Optional[bool] = None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.__on_tap_down = EventHandler(lambda e: TapEvent(**json.loads(e.data)))
        self._add_event_handler("tap_down", self.__on_tap_down.get_handler())

        self.content = content
        self.on_double_tap = on_double_tap
        self.on_long_press = on_long_press
        self.on_tap = on_tap
        self.on_tap_cancel = on_tap_cancel
        self.on_tap_down = on_tap_down
        self.placeholder = placeholder
        self.show_edit_icon = show_edit_icon

    def _get_control_name(self):
        return "c"

    def _get_children(self):
        return [self.__content]

    # content
    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        self.__content = value

    # placeholder
    @property
    def placeholder(self) -> Optional[bool]:
        return self._get_attr("placeholder", data_type="bool", def_value=False)

    @placeholder.setter
    def placeholder(self, value: Optional[bool]):
        self._set_attr("placeholder", value)

    # show_edit_icon
    @property
    def show_edit_icon(self) -> Optional[bool]:
        return self._get_attr("showEditIcon", data_type="bool", def_value=False)

    @show_edit_icon.setter
    def show_edit_icon(self, value: Optional[bool]):
        self._set_attr("showEditIcon", value)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_tap_cancel
    @property
    def on_tap_cancel(self):
        return self._get_event_handler("tap_cancel")

    @on_tap_cancel.setter
    def on_tap_cancel(self, handler):
        self._add_event_handler("tap_cancel", handler)
        self._set_attr("onTapCancel", True if handler is not None else None)

    # on_tap_down
    @property
    def on_tap_down(self):
        return self.__on_tap_down

    @on_tap_down.setter
    def on_tap_down(self, handler):
        self.__on_tap_down.subscribe(handler)
        self._set_attr("onTapDown", True if handler is not None else None)


class DataRow(Control):
    def __init__(
        self,
        cells: Optional[List[Control]] = None,
        ref=None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        # specific
        color: Union[None, str, Dict[MaterialState, str]] = None,
        selected: Optional[bool] = None,
        on_long_press=None,
        on_select_changed=None,
    ):
        Control.__init__(self, ref=ref, visible=visible, disabled=disabled, data=data)

        self.cells = cells
        self.color = color
        self.selected = selected
        self.on_long_press = on_long_press
        self.on_select_changed = on_select_changed

    def _get_control_name(self):
        return "r"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("color", self.__color)

    def _get_children(self):
        return self.__cells

    # cells
    @property
    def cells(self):
        return self.__cells

    @cells.setter
    def cells(self, value):
        self.__cells = value if value is not None else []

    # color
    @property
    def color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__color

    @color.setter
    def color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__color = value

    # selected
    @property
    def selected(self) -> Optional[bool]:
        return self._get_attr("selected", data_type="bool", def_value=False)

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_select_changed
    @property
    def on_select_changed(self):
        return self._get_event_handler("select_changed")

    @on_select_changed.setter
    def on_select_changed(self, handler):
        self._add_event_handler("select_changed", handler)
        self._set_attr("onSelectChanged", True if handler is not None else None)


class DataTable(ConstrainedControl):
    def __init__(
        self,
        columns: Optional[List[DataColumn]] = None,
        rows: Optional[List[DataRow]] = None,
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
        # DataTable-specific
        #
        border: Optional[Border] = None,
        border_radius: BorderRadiusValue = None,
        horizontal_lines: Optional[BorderSide] = None,
        vertical_lines: Optional[BorderSide] = None,
        checkbox_horizontal_margin: OptionalNumber = None,
        column_spacing: OptionalNumber = None,
        data_row_color: Union[None, str, Dict[MaterialState, str]] = None,
        data_row_min_height: OptionalNumber = None,
        data_row_max_height: OptionalNumber = None,
        data_text_style: Optional[TextStyle] = None,
        bgcolor: Optional[str] = None,
        gradient: Optional[Gradient] = None,
        divider_thickness: OptionalNumber = None,
        heading_row_color: Union[None, str, Dict[MaterialState, str]] = None,
        heading_row_height: OptionalNumber = None,
        heading_text_style: Optional[TextStyle] = None,
        horizontal_margin: OptionalNumber = None,
        show_bottom_border: Optional[bool] = None,
        show_checkbox_column: Optional[bool] = None,
        sort_ascending: Optional[bool] = None,
        sort_column_index: Optional[int] = None,
        on_select_all=None,
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

        self.columns = columns
        self.rows = rows
        self.border = border
        self.border_radius = border_radius
        self.horizontal_lines = horizontal_lines
        self.vertical_lines = vertical_lines
        self.bgcolor = bgcolor
        self.gradient = gradient
        self.divider_thickness = divider_thickness
        self.checkbox_horizontal_margin = checkbox_horizontal_margin
        self.column_spacing = column_spacing
        self.data_row_color = data_row_color
        self.data_row_min_height = data_row_min_height
        self.data_row_max_height = data_row_max_height
        self.data_text_style = data_text_style
        self.heading_row_color = heading_row_color
        self.heading_row_height = heading_row_height
        self.heading_text_style = heading_text_style
        self.horizontal_margin = horizontal_margin
        self.show_bottom_border = show_bottom_border
        self.show_checkbox_column = show_checkbox_column
        self.sort_ascending = sort_ascending
        self.sort_column_index = sort_column_index
        self.on_select_all = on_select_all

    def _get_control_name(self):
        return "datatable"

    def _before_build_command(self):
        super()._before_build_command()
        self._set_attr_json("border", self.__border)
        self._set_attr_json("gradient", self.__gradient)
        self._set_attr_json("borderRadius", self.__border_radius)
        self._set_attr_json("horizontalLines", self.__horizontal_lines)
        self._set_attr_json("verticalLines", self.__vertical_lines)
        self._set_attr_json("dataRowColor", self.__data_row_color)
        self._set_attr_json("headingRowColor", self.__heading_row_color)
        self._set_attr_json("dataTextStyle", self.__data_text_style)
        self._set_attr_json("headingTextStyle", self.__heading_text_style)

    def _get_children(self):
        children = []
        children.extend(self.__columns)
        children.extend(self.__rows)
        return children

    # columns
    @property
    def columns(self):
        return self.__columns

    @columns.setter
    def columns(self, value: Optional[List[DataColumn]]):
        self.__columns = value if value is not None else []

    # rows
    @property
    def rows(self):
        return self.__rows

    @rows.setter
    def rows(self, value: Optional[List[DataRow]]):
        self.__rows = value if value is not None else []

    # border
    @property
    def border(self) -> Optional[Border]:
        return self.__border

    @border.setter
    def border(self, value: Optional[Border]):
        self.__border = value

    # border_radius
    @property
    def border_radius(self) -> BorderRadiusValue:
        return self.__border_radius

    @border_radius.setter
    def border_radius(self, value: BorderRadiusValue):
        self.__border_radius = value

    # horizontal_lines
    @property
    def horizontal_lines(self) -> Optional[BorderSide]:
        return self.__horizontal_lines

    @horizontal_lines.setter
    def horizontal_lines(self, value: Optional[BorderSide]):
        self.__horizontal_lines = value

    # vertical_lines
    @property
    def vertical_lines(self) -> Optional[BorderSide]:
        return self.__vertical_lines

    @vertical_lines.setter
    def vertical_lines(self, value: Optional[BorderSide]):
        self.__vertical_lines = value

    # checkbox_horizontal_margin
    @property
    def checkbox_horizontal_margin(self) -> OptionalNumber:
        return self._get_attr("checkboxHorizontalMargin")

    @checkbox_horizontal_margin.setter
    def checkbox_horizontal_margin(self, value: OptionalNumber):
        self._set_attr("checkboxHorizontalMargin", value)

    # column_spacing
    @property
    def column_spacing(self) -> OptionalNumber:
        return self._get_attr("columnSpacing")

    @column_spacing.setter
    def column_spacing(self, value: OptionalNumber):
        self._set_attr("columnSpacing", value)

    # divider_thickness
    @property
    def divider_thickness(self) -> OptionalNumber:
        return self._get_attr("dividerThickness", data_type="float", def_value=1.0)

    @divider_thickness.setter
    def divider_thickness(self, value: OptionalNumber):
        self._set_attr("dividerThickness", value)

    # horizontal_margin
    @property
    def horizontal_margin(self) -> OptionalNumber:
        return self._get_attr("horizontalMargin")

    @horizontal_margin.setter
    def horizontal_margin(self, value: OptionalNumber):
        self._set_attr("horizontalMargin", value)

    # data_row_color
    @property
    def data_row_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__data_row_color

    @data_row_color.setter
    def data_row_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__data_row_color = value

    # data_row_min_height
    @property
    def data_row_min_height(self) -> OptionalNumber:
        return self._get_attr("dataRowMinHeight")

    @data_row_min_height.setter
    def data_row_min_height(self, value: OptionalNumber):
        self._set_attr("dataRowMinHeight", value)

    # data_row_max_height
    @property
    def data_row_max_height(self) -> OptionalNumber:
        return self._get_attr("dataRowMaxHeight")

    @data_row_max_height.setter
    def data_row_max_height(self, value: OptionalNumber):
        self._set_attr("dataRowMaxHeight", value)

    # data_text_style
    @property
    def data_text_style(self):
        return self.__data_text_style

    @data_text_style.setter
    def data_text_style(self, value: Optional[TextStyle]):
        self.__data_text_style = value

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
    def gradient(self, value: Optional[Gradient]):
        self.__gradient = value

    # heading_row_color
    @property
    def heading_row_color(self) -> Union[None, str, Dict[MaterialState, str]]:
        return self.__heading_row_color

    @heading_row_color.setter
    def heading_row_color(self, value: Union[None, str, Dict[MaterialState, str]]):
        self.__heading_row_color = value

    # heading_row_height
    @property
    def heading_row_height(self) -> OptionalNumber:
        return self._get_attr("headingRowHeight")

    @heading_row_height.setter
    def heading_row_height(self, value: OptionalNumber):
        self._set_attr("headingRowHeight", value)

    # heading_text_style
    @property
    def heading_text_style(self):
        return self.__heading_text_style

    @heading_text_style.setter
    def heading_text_style(self, value: Optional[TextStyle]):
        self.__heading_text_style = value

    # show_bottom_border
    @property
    def show_bottom_border(self) -> Optional[bool]:
        return self._get_attr("showBottomBorder", data_type="bool", def_value=False)

    @show_bottom_border.setter
    def show_bottom_border(self, value: Optional[bool]):
        self._set_attr("showBottomBorder", value)

    # show_checkbox_column
    @property
    def show_checkbox_column(self) -> Optional[bool]:
        return self._get_attr("showCheckboxColumn", data_type="bool", def_value=False)

    @show_checkbox_column.setter
    def show_checkbox_column(self, value: Optional[bool]):
        self._set_attr("showCheckboxColumn", value)

    # sort_ascending
    @property
    def sort_ascending(self) -> Optional[bool]:
        return self._get_attr("sortAscending", data_type="bool", def_value=False)

    @sort_ascending.setter
    def sort_ascending(self, value: Optional[bool]):
        self._set_attr("sortAscending", value)

    # sort_column_index
    @property
    def sort_column_index(self) -> Optional[int]:
        return self._get_attr("sortColumnIndex")

    @sort_column_index.setter
    def sort_column_index(self, value: Optional[int]):
        self._set_attr("sortColumnIndex", value)

    # on_select_all
    @property
    def on_select_all(self):
        return self._get_event_handler("select_all")

    @on_select_all.setter
    def on_select_all(self, handler):
        self._add_event_handler("select_all", handler)
        self._set_attr("onSelectAll", True if handler is not None else None)


class Item(Control):
    def __init__(self, obj):
        Control.__init__(self)
        assert obj, "obj cannot be empty"
        self.obj = obj

    def _set_attr(self, name, value, dirty=True):
        if value is None:
            return

        orig_val = self._get_attr(name)
        if orig_val is not None:
            if isinstance(orig_val, bool):
                value = str(value).lower() == "true"
            elif isinstance(orig_val, float):
                value = float(str(value))

        self._set_attr_internal(name, value, dirty=False)
        if isinstance(self.obj, dict):
            self.obj[name] = value
        else:
            setattr(self.obj, name, value)

    def _fetch_attrs(self):
        # reflection
        obj = self.obj if isinstance(self.obj, dict) else vars(self.obj)

        for name, val in obj.items():
            data_type = (
                type(val).__name__ if isinstance(val, (bool, float)) else "string"
            )
            orig_val = self._get_attr(name, data_type=data_type)

            if val != orig_val:
                self._set_attr_internal(name, val, dirty=True)

    def _get_control_name(self):
        return "item"
