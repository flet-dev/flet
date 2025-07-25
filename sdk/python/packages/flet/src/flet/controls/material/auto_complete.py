from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.types import Number

__all__ = ["AutoComplete", "AutoCompleteSuggestion", "AutoCompleteSelectEvent"]


@dataclass
class AutoCompleteSuggestion:
    key: str
    value: str


@dataclass
class AutoCompleteSelectEvent(Event["AutoComplete"]):
    selection: AutoCompleteSuggestion


@control("AutoComplete")
class AutoComplete(Control):
    """
    Helps the user make a selection by entering some text and choosing from among a
    list of displayed options.
    """

    suggestions: list[AutoCompleteSuggestion] = field(default_factory=list)
    """
    A list of [`AutoCompleteSuggestion`][flet.AutoCompleteSuggestion]
    controls representing the suggestions to be displayed.

    Note:
        - The internal filtration process of the suggestions (based on their `key`s) with
          respect to the user's input is case-insensitive because the comparison is done
          in lowercase.
        - A valid `AutoCompleteSuggestion` must have at least a `key` or `value` specified,
          else it will be ignored. If only `key` is provided, `value` will be set to `key`
          as fallback and vice versa.
    """

    suggestions_max_height: Number = 200
    """
    The maximum - visual - height of the suggestions list.
    """

    on_select: Optional[EventHandler[AutoCompleteSelectEvent]] = None
    """
    Called when a suggestion is selected.
    """

    @property
    def selected_index(self):
        # TODO: check availability of _selected_index + a default if not yet available
        return self._selected_index
