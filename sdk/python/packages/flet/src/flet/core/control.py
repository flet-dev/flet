import datetime as dt
import json
from difflib import SequenceMatcher
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Any,
    AnyStr,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from flet.core.badge import Badge, BadgeValue
from flet.core.embed_json_encoder import EmbedJsonEncoder
from flet.core.protocol import Command
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import (
    ControlState,
    OptionalControlEventCallable,
    OptionalNumber,
    ResponsiveNumber,
    SupportsStr,
)

if TYPE_CHECKING:
    from .page import Page

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

V = TypeVar("V", str, int, float, bool, Any)
DV = TypeVar("DV", bound=Optional[Any])


class Control:
    def __init__(
        self,
        ref: Optional[Ref] = None,
        expand: Union[None, bool, int] = None,
        expand_loose: Optional[bool] = None,
        col: Optional[ResponsiveNumber] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
    ) -> None:
        super().__init__()

        self.__page: Optional[Page] = None
        self.__attrs: Dict[str, Any] = {}
        self.__previous_children = []
        self._id = None
        self.__uid: Optional[str] = None

        if ref:
            ref.current = self
        self.expand = expand
        self.expand_loose = expand_loose
        self.col = col
        self.opacity = opacity
        self.tooltip = tooltip
        self.badge = badge
        self.visible = visible
        self.disabled = disabled
        self.__data: Any = None
        self.data = data
        self.rtl = rtl

        self.__event_handlers: Dict[str, OptionalControlEventCallable] = {}
        self.parent: Optional[Control] = None

    def is_isolated(self) -> bool:
        return False

    def build(self):
        pass

    def before_update(self):
        pass

    def _before_build_command(self) -> None:
        # checking if tooltip has getter/setter in inherited class
        if "tooltip" not in vars(self.__class__):
            self._set_attr_json("tooltip", self.tooltip)
        if isinstance(self.badge, (Badge, str)):
            self._set_attr_json("badge", self.badge)
        else:
            self._set_attr("badge", None)

        self._set_attr_json("col", self.__col)

    def did_mount(self):
        pass

    def will_unmount(self):
        pass

    def _get_children(self) -> "List[Control]":
        return []

    def _get_control_name(self) -> str:
        raise NotImplementedError(
            "_get_control_name must be overridden in inherited class"
        )

    def _add_event_handler(
        self, event_name: str, handler: OptionalControlEventCallable
    ) -> None:
        self.__event_handlers[event_name] = handler

    def _get_event_handler(self, event_name: str) -> OptionalControlEventCallable:
        return self.__event_handlers.get(event_name)

    def _get_attr(
        self,
        name: str,
        def_value: DV = None,
        data_type: Union[
            Literal["string", "int", "float", "bool", "bool?"], AnyStr
        ] = "string",
    ) -> Union[V, DV]:
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

    def _set_attr(self, name: str, value: V, dirty: bool = True) -> None:
        self._set_attr_internal(name, value, dirty)

    def _set_enum_attr(
        self,
        name: str,
        value: V,
        enum_type: Union[Type[Enum], Tuple[Type[Enum], ...]],
        dirty: bool = True,
    ) -> None:
        self._set_attr_internal(
            name, value.value if isinstance(value, enum_type) else value, dirty
        )

    def _get_value_or_list_attr(self, name: str, delimiter: str) -> Union[List[str], V]:
        v = self._get_attr(name)
        if v and delimiter in v:
            return [x.strip() for x in v.split(delimiter)]
        return v

    def _set_value_or_list_attr(
        self, name: str, value: Union[List[SupportsStr], V], delimiter: str
    ) -> None:
        if isinstance(value, List):
            value = delimiter.join([str(x) for x in value])
        self._set_attr(name, value)

    def _set_attr_internal(self, name: str, value: V, dirty: bool = True) -> None:
        name = name.lower()
        orig_val = self.__attrs.get(name)

        if value is None:
            if orig_val is None:
                return
            value = ""

        if orig_val is None or orig_val[0] != value:
            self.__attrs[name] = (value, dirty)

    def _set_attr_json(self, name: str, value: V, wrap_attr_dict: bool = False) -> None:
        ov = self._get_attr(name)
        nv = self._convert_attr_json(
            self._wrap_attr_dict(value) if wrap_attr_dict else value
        )
        if ov != nv:
            self._set_attr(name, nv)

    def _convert_attr_json(self, value: V) -> Optional[str]:
        return (
            json.dumps(value, cls=EmbedJsonEncoder, separators=(",", ":"))
            if value is not None
            else None
        )

    def _wrap_attr_dict(self, value: Optional[Union[Dict, Any]]) -> Optional[Dict]:
        if value is None or isinstance(value, Dict):
            return value
        return {ControlState.DEFAULT: value}

    # event_handlers
    @property
    def event_handlers(self) -> Dict[str, Any]:
        return self.__event_handlers

    # _previous_children
    @property
    def _previous_children(self):
        return self.__previous_children

    # _id
    @property
    def _id(self) -> str:
        return self._get_attr("id")

    @_id.setter
    def _id(self, value: str):
        self._set_attr("id", value)

    # page
    @property
    def page(self) -> "Optional[Page]":
        return self.__page

    @page.setter
    def page(self, page: "Optional[Page]"):
        self.__page = page

    # uid
    @property
    def uid(self) -> Optional[str]:
        return self.__uid

    # expand
    @property
    def expand(self) -> Optional[Union[bool, int]]:
        return self.__expand

    @expand.setter
    def expand(self, value: Optional[Union[bool, int]]):
        self.__expand = value
        if value and isinstance(value, bool):
            value = 1
        self._set_attr("expand", value if value else None)

    # expand_loose
    @property
    def expand_loose(self) -> bool:
        return self._get_attr("expandLoose", data_type="bool", def_value=False)

    @expand_loose.setter
    def expand_loose(self, value: Optional[bool]):
        self._set_attr("expandLoose", value)

    # rtl
    @property
    def rtl(self) -> bool:
        return self._get_attr("rtl", data_type="bool", def_value=False)

    @rtl.setter
    def rtl(self, value: Optional[bool]):
        self._set_attr("rtl", value)

    # col
    @property
    def col(self) -> Optional[ResponsiveNumber]:
        return self.__col

    @col.setter
    def col(self, value: Optional[ResponsiveNumber]):
        self.__col = value

    # opacity
    @property
    def opacity(self) -> float:
        return self._get_attr("opacity", data_type="float", def_value=1.0)

    @opacity.setter
    def opacity(self, value: OptionalNumber):
        assert (
            value is None or 0.0 <= value <= 1.0
        ), "opacity must be between 0.0 and 1.0"
        self._set_attr("opacity", value)

    # visible
    @property
    def visible(self) -> bool:
        return self._get_attr("visible", data_type="bool", def_value=True)

    @visible.setter
    def visible(self, value: Optional[bool]):
        self._set_attr("visible", value)

    # disabled
    @property
    def disabled(self) -> bool:
        return self._get_attr("disabled", data_type="bool", def_value=False)

    @disabled.setter
    def disabled(self, value: Optional[bool]):
        self._set_attr("disabled", value)

    # data
    @property
    def data(self) -> Optional[Any]:
        return self.__data

    @data.setter
    def data(self, value: Optional[Any]):
        self.__data = value

    # public methods
    def update(self) -> None:
        assert (
            self.__page
        ), f"{self.__class__.__qualname__} Control must be added to the page first"
        self.__page.update(self)

    def clean(self) -> None:
        assert (
            self.__page
        ), f"{self.__class__.__qualname__} Control must be added to the page"
        self.__page._clean(self)

    def invoke_method(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
        wait_timeout: Optional[float] = 5,
    ) -> Optional[str]:
        assert (
            self.__page
        ), f"{self.__class__.__qualname__} Control must be added to the page first"
        if arguments:
            # remove items with None values and convert other values to string
            arguments = {k: str(v) for k, v in arguments.items() if v is not None}
        return self.__page._invoke_method(
            control_id=self.uid,
            method_name=method_name,
            arguments=arguments,
            wait_for_result=wait_for_result,
            wait_timeout=wait_timeout,
        )

    def invoke_method_async(
        self,
        method_name: str,
        arguments: Optional[Dict[str, str]] = None,
        wait_for_result: bool = False,
        wait_timeout: Optional[float] = 5,
    ):
        assert (
            self.__page
        ), f"{self.__class__.__qualname__} Control must be added to the page first"
        if arguments:
            # remove items with None values and convert other values to string
            arguments = {k: str(v) for k, v in arguments.items() if v is not None}
        return self.__page._invoke_method_async(
            control_id=self.uid,
            method_name=method_name,
            arguments=arguments,
            wait_for_result=wait_for_result,
            wait_timeout=wait_timeout,
        )

    def copy_attrs(self, dest: Dict[str, Any]) -> None:
        for attr_name in sorted(self.__attrs):
            attr_name_lower = attr_name.lower()
            value, dirty = self.__attrs[attr_name_lower]

            if dirty or value is None:
                continue

            if isinstance(value, bool):
                sval = str(value).lower()
            elif isinstance(value, (dt.datetime, dt.date)):
                sval = value.isoformat()
            else:
                sval = str(value)

            dest[attr_name_lower] = sval

    def build_update_commands(
        self, index, commands, added_controls, removed_controls, isolated: bool = False
    ) -> None:
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
                        ctrl.parent = self  # set as parent
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
                        isolated=ctrl.is_isolated(),
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
                    ctrl.parent = self  # set as parent
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

    def _remove_control_recursively(self, index, control: "Control") -> "List[Control]":
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
    def _build_add_commands(
        self, indent: int = 0, index=None, added_controls=None
    ) -> List[Command]:
        if index:
            self.page = index["page"]
        self.build()

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
            control.parent = self  # set as parent
        self.__previous_children.clear()
        self.__previous_children.extend(children)

        return commands

    def _build_command(self, update: bool = False) -> Command:
        command = Command(0, None, [], {}, [])

        if update and not self.__uid:
            return command
        self._before_build_command()
        self.before_update()

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

    def _dispose(self) -> None:
        self.page = None
        self.__event_handlers.clear()

    # Magic methods
    def __str__(self) -> str:
        attrs = {}
        for k, v in self.__attrs.items():
            attrs[k] = v[0]
        return f"{self._get_control_name()} {attrs}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            + ", ".join(
                f"{k}={v[0]}" if not isinstance(v[0], str) else f"{k}='{v[0]}'"
                for k, v in self.__attrs.items()
            )
            + ")"
        )
