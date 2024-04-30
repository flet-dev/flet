import dataclasses
import json
from typing import Any, Optional, List

from flet_core.control import Control, OptionalNumber
from flet_core.control_event import ControlEvent
from flet_core.event_handler import EventHandler
from flet_core.ref import Ref


@dataclasses.dataclass
class AutoCompleteSuggestion:
    key: str = dataclasses.field(default=None)
    value: str = dataclasses.field(default=None)


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
        on_select=None,
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

        def convert_event_data(e):
            print(e.data)
            d = json.loads(e.data)
            return AutoCompleteSelectEvent(**d)

        self.__on_select = EventHandler(convert_event_data)
        self._add_event_handler("select", self.__on_select.get_handler())

        self.suggestions = suggestions
        self.suggestions_max_height = suggestions_max_height
        self.on_select = on_select

    def _get_control_name(self):
        return "autocomplete"

    def before_update(self):
        self._set_attr_json("suggestions", self.__suggestions)

    # suggestions_max_height
    @property
    def suggestions_max_height(self) -> OptionalNumber:
        return self._get_attr(
            "suggestionsMaxHeight", data_type="float", def_value=200.0
        )

    @suggestions_max_height.setter
    def suggestions_max_height(self, value: OptionalNumber):
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
    def on_select(self):
        return self._get_event_handler("select")

    @on_select.setter
    def on_select(self, handler):
        self.__on_select.subscribe(handler)


class AutoCompleteSelectEvent(ControlEvent):
    def __init__(self, key: str, value: str) -> None:
        self.selection: AutoCompleteSuggestion = AutoCompleteSuggestion(
            key=key, value=value
        )
