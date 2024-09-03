import json
from dataclasses import dataclass, field
from typing import Any, Optional, List

from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref
from flet_core.types import OptionalEventCallable


@dataclass
class AutoCompleteSuggestion:
    key: str = field(default=None)
    value: str = field(default=None)


class AutoComplete(Control):
    """
    Helps the user make a selection by entering some text and choosing from among a list of displayed options.

    -----

    Online docs: https://flet.dev/docs/controls/autocomplete
    """

    def __init__(
        self,
        suggestions: Optional[List[AutoCompleteSuggestion]] = None,
        suggestions_max_height: OptionalNumber = None,
        on_select: OptionalEventCallable["AutoCompleteSelectEvent"] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):

        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            visible=visible,
            data=data,
        )

        self.__on_select = EventHandler(lambda e: AutoCompleteSelectEvent(e))
        self._add_event_handler("select", self.__on_select.get_handler())

        self.suggestions = suggestions
        self.suggestions_max_height = suggestions_max_height
        self.on_select = on_select

    def _get_control_name(self):
        return "autocomplete"

    def before_update(self):
        self._set_attr_json("suggestions", self.__suggestions)

    # selected_index
    @property
    def selected_index(self) -> Optional[int]:
        return self._get_attr("selectedIndex", data_type="int")

    # suggestions_max_height
    @property
    def suggestions_max_height(self) -> float:
        return self._get_attr(
            "suggestionsMaxHeight", data_type="float", def_value=200.0
        )

    @suggestions_max_height.setter
    def suggestions_max_height(self, value: OptionalNumber):
        assert value is None or value >= 0, "suggestions_max_height cannot be negative"
        self._set_attr("suggestionsMaxHeight", value)

    # suggestions
    @property
    def suggestions(self) -> Optional[List[AutoCompleteSuggestion]]:
        return self.__suggestions

    @suggestions.setter
    def suggestions(self, value: Optional[List[str]]):
        self.__suggestions = value or []

    # on_select
    @property
    def on_select(self) -> OptionalEventCallable["AutoCompleteSelectEvent"]:
        return self.__on_select.handler

    @on_select.setter
    def on_select(self, handler: OptionalEventCallable["AutoCompleteSelectEvent"]):
        self.__on_select.handler = handler


class AutoCompleteSelectEvent(ControlEvent):
    def __init__(self, e: ControlEvent):
        super().__init__(e.target, e.name, e.data, e.control, e.page)
        d = json.loads(e.data)
        self.selection: AutoCompleteSuggestion = AutoCompleteSuggestion(
            key=d.get("key"), value=d.get("value")
        )
