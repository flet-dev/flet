from dataclasses import dataclass, field
from typing import List, Optional

from flet.controls.control import Control, control
from flet.controls.control_event import ControlEvent
from flet.controls.types import OptionalEventCallable, OptionalNumber

__all__ = ["AutoComplete", "AutoCompleteSuggestion", "AutoCompleteSelectEvent"]


@dataclass
class AutoCompleteSuggestion:
    key: str = field(default=None)
    value: str = field(default=None)


@dataclass
class AutoCompleteSelectEvent(ControlEvent):
    selection: AutoCompleteSuggestion


@control("AutoComplete")
class AutoComplete(Control):
    """
    Helps the user make a selection by entering some text and choosing from among a list of displayed options.

    -----

    Online docs: https://flet.dev/docs/controls/autocomplete
    """

    suggestions: Optional[List[AutoCompleteSuggestion]] = field(default_factory=list)
    suggestions_max_height: OptionalNumber = None
    on_select: OptionalEventCallable[AutoCompleteSelectEvent] = None
