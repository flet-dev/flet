import datetime as dt
import json
from difflib import SequenceMatcher
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from flet_core.embed_json_encoder import EmbedJsonEncoder
from flet_core.protocol import Command
from flet_core.ref import Ref
from flet_core.types import ResponsiveNumber

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


if TYPE_CHECKING:
    from .page import Page

OptionalNumber = Union[None, int, float]


class Control:
    def __init__(
        self,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[str] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        super().__init__()
        self.__page: Optional[Page] = None
        self.__attrs = {}
        self.__previous_children = []
        self._id = None
        self.__uid: Optional[str] = None
        self.expand = expand
        self.col = col
        self.opacity = opacity
        self.tooltip = tooltip
        self.visible = visible
        self.disabled = disabled
        self.__data: Any = None
        self.data = data
        self.__event_handlers = {}
        if ref:
            ref.current = self

    def _is_isolated(self):
        return False

    def _build(self):
        pass

    def _before_build_command(self):
        self._set_attr_json("col", self.__col)

    def did_mount(self):
        pass

    async def did_mount_async(self):
        pass

    def will_unmount(self):
        pass

    async def will_unmount_async(self):
        pass

    def _get_children(self):
        return []

    def _get_control_name(self):
        raise Exception("_getControlName must be overridden in inherited class")

    def _add_event_handler(self, event_name, handler):
        self.__event_handlers[event_name] = handler

    def _get_event_handler(self, event_name):
        return self.__event_handlers.get(event_name)

    def _get_attr(self, name, def_value=None, data_type="string"):
        name = name.lower()
        if name not in self.__attrs:
            return def_value

        s_val = self.__attrs[name][0]
        if data_type == "bool" and s_val is not None and isinstance(s_val, str):
            return s_val.lower() == "true"
        elif data_type == "bool?" and isinstance(s_val, str):
            if s_val.lower() == "true":
                return True
            elif s_val.lower() == "false":
                return False
            else:
                return def_value
        elif data_type == "float" and s_val is not None and isinstance(s_val, str):
            return float(s_val)
        elif data_type == "int" and s_val is not None and isinstance(s_val, str):
            return int(s_val)
        else:
            return s_val

    def _set_attr(self, name, value, dirty=True):
        self._set_attr_internal(name, value, dirty)

    def _get_value_or_list_attr(self, name, delimiter):
        v = self._get_attr(name)
        if v and delimiter in v:
            return [x.strip() for x in v.split(delimiter)]
        return v

    def _set_value_or_list_attr(self, name, value, delimiter):
        if isinstance(value, List):
            value = delimiter.join([str(x) for x in value])
        self._set_attr(name, value)

    def _set_attr_internal(self, name, value, dirty=True):
        name = name.lower()
        orig_val = self.__attrs.get(name)

        if orig_val is None and value is None:
            return

        if value is None:
            value = ""

        if orig_val is None or orig_val[0] != value:
            self.__attrs[name] = (value, dirty)

    def _set_attr_json(self, name, value):
        ov = self._get_attr(name)
        nv = self._convert_attr_json(value)
        if ov != nv:
            self._set_attr(name, nv)

    def _convert_attr_json(self, value):
        return (
            json.dumps(value, cls=EmbedJsonEncoder, separators=(",", ":"))
            if value is not None
            else None
        )

    def _wrap_attr_dict(self, value):
        if value is None or isinstance(value, Dict):
            return value
        return {"": value}

    def __str__(self):
        attrs = {}
        for k, v in self.__attrs.items():
            attrs[k] = v[0]
        return f"{self._get_control_name()} {attrs}"

    # event_handlers
    @property
    def event_handlers(self):
        return self.__event_handlers

    # _previous_children
    @property
    def _previous_children(self):
        return self.__previous_children

    # _id
    @property
    def _id(self):
        return self._get_attr("id")

    @_id.setter
    def _id(self, value):
        self._set_attr("id", value)

    # page
    @property
    def page(self):
        return self.__page

    @page.setter
    def page(self, page):
        self.__page = page

    # uid
    @property
    def uid(self):
        return self.__uid

    # expand
    @property
    def expand(self) -> Union[None, bool, int]:
        return self.__expand

    @expand.setter
    def expand(self, value: Union[None, bool, int]):
        self.__expand = value
        if value and isinstance(value, bool):
            value = 1
        self._set_attr("expand", value if value else None)

    # col
    @property
    def col(self) -> Optional[ResponsiveNumber]:
        return self.__col

    @col.setter
    def col(self, value: Optional[ResponsiveNumber]):
        self.__col = value

    # opacity
    @property
    def opacity(self):
        return self._get_attr("opacity", data_type="float", def_value=1.0)

    @opacity.setter
    def opacity(self, value):
        self._set_attr("opacity", value)

    # tooltip
    @property
    def tooltip(self):
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value):
        self._set_attr("tooltip", value)

    # visible
    @property
    def visible(self) -> Optional[bool]:
        return self._get_attr("visible", data_type="bool", def_value=True)

    @visible.setter
    def visible(self, value: Optional[bool]):
        self._set_attr("visible", value)

    # disabled
    @property
    def disabled(self) -> Optional[bool]:
        return self._get_attr("disabled", data_type="bool", def_value=False)

    @disabled.setter
    def disabled(self, value: Optional[bool]):
        self._set_attr("disabled", value)

    # data
    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        self.__data = value

    # public methods
    def update(self):
        assert self.__page, "Control must be added to the page first."
        self.__page.update(self)

    async def update_async(self):
        assert self.__page, "Control must be added to the page first."
        await self.__page.update_async(self)

    def clean(self):
        assert self.__page, "Control must be added to the page first."
        self.__page._clean(self)

    async def clean_async(self):
        assert self.__page, "Control must be added to the page first."
        await self.__page._clean_async(self)

    def build_update_commands(
        self, index, commands, added_controls, removed_controls, isolated=False
    ):
        update_cmd = self._build_command(update=True)

        if len(update_cmd.attrs) > 0:
            update_cmd.name = "set"
            commands.append(update_cmd)

        if isolated:
            return

        # go through children
        previous_children = self.__previous_children
        current_children = self._get_children()

        hashes = {}
        previous_ints = []
        current_ints = []

        for ctrl in previous_children:
            hashes[hash(ctrl)] = ctrl
            previous_ints.append(hash(ctrl))

        for ctrl in current_children:
            hashes[hash(ctrl)] = ctrl
            current_ints.append(hash(ctrl))

        sm = SequenceMatcher(None, previous_ints, current_ints)

        n = 0
        for tag, a1, a2, b1, b2 in sm.get_opcodes():
            if tag == "delete" or tag == "replace":
                # deleted controls
                ids = []
                for h in previous_ints[a1:a2]:
                    ctrl = hashes[h]
                    # check if re-added control is being deleted
                    # which means it's a replace
                    i = 0
                    replaced = False
                    while i < len(commands):
                        cmd = commands[i]
                        if cmd.name == "add" and any(
                            c for c in cmd.commands if c.attrs.get("id") == ctrl.__uid
                        ):
                            # insert delete command before add
                            commands.insert(i, Command(0, "remove", [ctrl.__uid]))
                            replaced = True
                            break
                        i += 1
                    removed_controls.extend(
                        self._remove_control_recursively(index, ctrl)
                    )
                    if not replaced:
                        ids.append(ctrl.__uid)
                if len(ids) > 0:
                    commands.append(Command(0, "remove", ids))
                if tag == "replace":
                    # add
                    for h in current_ints[b1:b2]:
                        ctrl = hashes[h]
                        innerCmds = ctrl._build_add_commands(
                            index=index, added_controls=added_controls
                        )
                        assert self.__uid is not None
                        commands.append(
                            Command(
                                indent=0,
                                name="add",
                                attrs={"to": self.__uid, "at": str(n)},
                                commands=innerCmds,
                            )
                        )
                        n += 1
            elif tag == "equal":
                # unchanged control
                for h in previous_ints[a1:a2]:
                    ctrl = hashes[h]
                    ctrl.build_update_commands(
                        index,
                        commands,
                        added_controls,
                        removed_controls,
                        isolated=ctrl._is_isolated(),
                    )
                    n += 1
            elif tag == "insert":
                # add
                for h in current_ints[b1:b2]:
                    ctrl = hashes[h]
                    innerCmds = ctrl._build_add_commands(
                        index=index, added_controls=added_controls
                    )
                    assert self.__uid is not None
                    commands.append(
                        Command(
                            indent=0,
                            name="add",
                            attrs={"to": self.__uid, "at": str(n)},
                            commands=innerCmds,
                        )
                    )
                    n += 1

        self.__previous_children.clear()
        self.__previous_children.extend(current_children)

    def _remove_control_recursively(self, index, control):
        removed_controls = []

        if control.__uid in index:
            del index[control.__uid]

            for child in control._get_children():
                removed_controls.extend(self._remove_control_recursively(index, child))

            for child in control._previous_children:
                removed_controls.extend(self._remove_control_recursively(index, child))

            removed_controls.append(control)

        return removed_controls

    # private methods
    def _build_add_commands(self, indent=0, index=None, added_controls=None):
        self._build()

        # remove control from index
        if self.__uid and index is not None and self.__uid in index:
            del index[self.__uid]

        commands = []

        # main command
        command = self._build_command(False)
        command.indent = indent
        command.values.append(self._get_control_name())
        commands.append(command)

        if added_controls is not None:
            added_controls.append(self)

        # controls
        children = self._get_children()
        for control in children:
            childCmd = control._build_add_commands(
                indent=indent + 2, index=index, added_controls=added_controls
            )
            commands.extend(childCmd)

        self.__previous_children.clear()
        self.__previous_children.extend(children)

        return commands

    def _build_command(self, update=False):
        command = Command(0, None, [], {}, [])

        if update and not self.__uid:
            return command

        self._before_build_command()

        for attrName in sorted(self.__attrs):
            attrName = attrName.lower()
            dirty = self.__attrs[attrName][1]

            if (update and not dirty) or attrName == "id":
                continue

            val = self.__attrs[attrName][0]
            sval = ""
            if val is None:
                continue
            elif isinstance(val, bool):
                sval = str(val).lower()
            elif isinstance(val, dt.datetime) or isinstance(val, dt.date):
                sval = val.isoformat()
            else:
                sval = str(val)
            command.attrs[attrName] = sval
            self.__attrs[attrName] = (val, False)

        id = self.__attrs.get("id")
        if not update and self.__uid is not None:
            command.attrs["id"] = self.__uid
        elif not update and id is not None:
            command.attrs["id"] = id
        elif update and len(command.attrs) > 0:
            assert self.__uid is not None
            command.values.append(self.__uid)

        return command

    def _dispose(self):
        self.page = None
        self.__event_handlers.clear()
