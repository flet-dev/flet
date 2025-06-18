from dataclasses import dataclass, field

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, OptionalEventHandler
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

    Online docs: https://flet.dev/docs/controls/autocomplete
    """

    suggestions: list[AutoCompleteSuggestion] = field(default_factory=list)
    """
    A list of [`AutoCompleteSuggestion`](https://flet.dev/docs/reference/types/autocompletesuggestion)
    controls representing the suggestions to be displayed.

    **Note:**

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

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber)
    and defaults to `200`.
    """

    on_select: OptionalEventHandler[AutoCompleteSelectEvent] = None
    """
    Fires when a suggestion is selected.

    Event handler is of type [`AutoCompleteSelectEvent`](https://flet.dev/docs/reference/types/autocompleteselectevent).
    """

    @property
    def selected_index(self):
        return self._selected_index
