from __future__ import annotations

from typing import Optional

from beartype import beartype

from flet.control import Control

try:
    from typing import Literal
except:
    from typing_extensions import Literal


SelectionMode = Literal[None, "single", "multiple"]
Sortable = Literal[None, "string", "number", False]
Sorted = Literal[None, False, "asc", "desc"]


class Grid(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        selection_mode: SelectionMode = None,
        compact=None,
        header_visible=None,
        shimmer_lines=None,
        preserve_selection=None,
        columns=None,
        items=None,
        on_select=None,
        onitem_invoke=None,
        width=None,
        height=None,
        padding=None,
        margin=None,
        visible=None,
        disabled=None,
    ):
        Control.__init__(
            self,
            id=id,
            ref=ref,
            width=width,
            height=height,
            padding=padding,
            margin=margin,
            visible=visible,
            disabled=disabled,
        )

        self.selection_mode = selection_mode
        self.compact = compact
        self.header_visible = header_visible
        self.shimmer_lines = shimmer_lines
        self.preserve_selection = preserve_selection
        self._on_select_handler = None
        self.on_select = on_select
        self.onitem_invoke = onitem_invoke
        self._columns = Columns(columns=columns)
        self._items = Items(items=items)
        self._selected_items = []

    def _get_control_name(self):
        return "grid"

    # columns
    @property
    def columns(self):
        return self._columns.columns

    @columns.setter
    def columns(self, value):
        self._columns.columns = value

    # items
    @property
    def items(self):
        return self._items.items

    @items.setter
    def items(self, value):
        self._items.items = value

    # on_select
    @property
    def on_select(self):
        return self._on_select_handler

    @on_select.setter
    def on_select(self, handler):
        self._on_select_handler = handler
        self._add_event_handler("select", self._on_select_internal)

    # selected_items
    @property
    def selected_items(self):
        return self._selected_items

    @selected_items.setter
    def selected_items(self, value):
        self._selected_items = value
        indices = [
            str(idx)
            for selected_item in value
            for idx, item in enumerate(self._items.items)
            if item == selected_item
        ]
        self._set_attr("selectedindices", " ".join(indices))

    # onitem_invoke
    @property
    def onitem_invoke(self):
        return self._get_event_handler("itemInvoke")

    @onitem_invoke.setter
    def onitem_invoke(self, handler):
        self._add_event_handler("itemInvoke", handler)

    # selection_mode
    @property
    def selection_mode(self):
        return self._get_attr("selection")

    @selection_mode.setter
    @beartype
    def selection_mode(self, value: SelectionMode):
        self._set_attr("selection", value)

    # compact
    @property
    def compact(self):
        return self._get_attr("compact", data_type="bool", def_value=False)

    @compact.setter
    @beartype
    def compact(self, value: Optional[bool]):
        self._set_attr("compact", value)

    # header_visible
    @property
    def header_visible(self):
        return self._get_attr("headerVisible", data_type="bool", def_value=True)

    @header_visible.setter
    @beartype
    def header_visible(self, value: Optional[bool]):
        self._set_attr("headerVisible", value)

    # preserve_selection
    @property
    def preserve_selection(self):
        return self._get_attr("preserveSelection", data_type="bool", def_value=False)

    @preserve_selection.setter
    @beartype
    def preserve_selection(self, value: Optional[bool]):
        self._set_attr("preserveSelection", value)

    # shimmer_lines
    @property
    def shimmer_lines(self):
        return self._get_attr("shimmerLines")

    @shimmer_lines.setter
    @beartype
    def shimmer_lines(self, value: Optional[int]):
        self._set_attr("shimmerLines", value)

    def _on_select_internal(self, e):
        self._selected_items = [self.page.get_control(id).obj for id in e.data.split()]

        if self._on_select_handler != None:
            self._on_select_handler(e)

    def _get_children(self):
        return [self._columns, self._items]


class Columns(Control):
    def __init__(self, id=None, ref=None, columns=None):
        Control.__init__(self, id=id, ref=ref)

        self.columns = columns

    def _get_control_name(self):
        return "columns"

    def _get_children(self):
        return self.columns


class Items(Control):
    def __init__(self, id=None, ref=None, items=None):
        Control.__init__(self, id=id, ref=ref)

        self.__map = {}
        self.__items = []
        self.items = items

    # items
    @property
    def items(self):
        return self.__items

    @items.setter
    @beartype
    def items(self, value: Optional[list]):
        self.__items = value or []

    def _get_control_name(self):
        return "items"

    def _get_children(self):
        items = []
        for obj in self.__items:
            key = obj
            if isinstance(obj, dict):
                key = tuple(obj.items())
            item = self.__map.setdefault(key, Item(obj))
            item._fetch_attrs()
            items.append(item)

        del_objs = [key for key, item in self.__map.items() if item not in items]
        for key in del_objs:
            del self.__map[key]

        return items


class Column(Control):
    def __init__(
        self,
        id=None,
        ref=None,
        name=None,
        icon=None,
        icon_only=None,
        field_name=None,
        sortable: Sortable = None,
        sort_field=None,
        sorted: Sorted = None,
        resizable=None,
        min_width=None,
        max_width=None,
        on_click=None,
        template_controls=None,
    ):
        Control.__init__(self, id=id, ref=ref)

        self.name = name
        self.icon = icon
        self.icon_only = icon_only
        self.field_name = field_name
        self.sortable = sortable
        self.sort_field = sort_field
        self.sorted = sorted
        self.resizable = resizable
        self.min_width = min_width
        self.max_width = max_width
        self.on_click = on_click

        self.template_controls = template_controls or []

    def _get_control_name(self):
        return "column"

    # name
    @property
    def name(self):
        return self._get_attr("name")

    @name.setter
    def name(self, value):
        self._set_attr("name", value)

    # icon
    @property
    def icon(self):
        return self._get_attr("icon")

    @icon.setter
    def icon(self, value):
        self._set_attr("icon", value)

    # icon_only
    @property
    def icon_only(self):
        return self._get_attr("iconOnly", data_type="bool", def_value=False)

    @icon_only.setter
    @beartype
    def icon_only(self, value: Optional[bool]):
        self._set_attr("iconOnly", value)

    # field_name
    @property
    def field_name(self):
        return self._get_attr("fieldName")

    @field_name.setter
    def field_name(self, value):
        self._set_attr("fieldName", value)

    # sortable
    @property
    def sortable(self):
        return self._get_attr("sortable")

    @sortable.setter
    @beartype
    def sortable(self, value: Sortable):
        self._set_attr("sortable", value)

    # sort_field
    @property
    def sort_field(self):
        return self._get_attr("sortField")

    @sort_field.setter
    def sort_field(self, value):
        self._set_attr("sortField", value)

    # sorted
    @property
    def sorted(self):
        return self._get_attr("sorted")

    @sorted.setter
    @beartype
    def sorted(self, value: Sorted):
        self._set_attr("sorted", value)

    # resizable
    @property
    def resizable(self):
        return self._get_attr("resizable", data_type="bool", def_value=False)

    @resizable.setter
    @beartype
    def resizable(self, value: Optional[bool]):
        self._set_attr("resizable", value)

    # min_width
    @property
    def min_width(self):
        return self._get_attr("minWidth")

    @min_width.setter
    @beartype
    def min_width(self, value: Optional[int]):
        self._set_attr("minWidth", value)

    # max_width
    @property
    def max_width(self):
        return self._get_attr("maxWidth")

    @max_width.setter
    @beartype
    def max_width(
        self, value: Optional[int]
    ):  # could these not be floats? Union[None, int, float]
        self._set_attr("maxWidth", value)

    # on_click
    @property
    def on_click(self):
        return self._get_attr("on_click")

    @on_click.setter
    def on_click(self, value):  # beartype currently has an issue with typing.Callable
        self._set_attr("on_click", value)

    def _get_children(self):
        return self.template_controls


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
