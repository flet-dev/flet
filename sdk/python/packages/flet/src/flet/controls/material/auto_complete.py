from dataclasses import dataclass, field
from typing import Optional

from flet import LayoutControl
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler, Event, EventHandler
from flet.controls.types import Number

__all__ = ["AutoComplete", "AutoCompleteSelectEvent", "AutoCompleteSuggestion"]


@dataclass
class AutoCompleteSuggestion:
    """
    Represents a suggestion item for the [`AutoComplete`][flet.] control.
    """

    key: str
    """A unique identifier or value used for filtering and selection."""

    value: str
    """The display text shown to the user."""


@dataclass
class AutoCompleteSelectEvent(Event["AutoComplete"]):
    """Event representing the selection of a suggestion in the AutoComplete control."""

    index: int
    """
    The index of the selected suggestion from the corresponding
    [`AutoComplete.suggestions`][flet.] list.
    """

    selection: AutoCompleteSuggestion
    """The selected suggestion."""


@control("AutoComplete")
class AutoComplete(LayoutControl):
    """
    Helps the user make a selection by entering some text and choosing from among a
    list of displayed options.
    """

    value: str = ""
    """
    Current text displayed in the input field.

    This value reflects user input even if it does not match any provided suggestion.
    """

    suggestions: list[AutoCompleteSuggestion] = field(default_factory=list)
    """
    A list of [`AutoCompleteSuggestion`][flet.]
    controls representing the suggestions to be displayed.

    Note:
        - A valid [`AutoCompleteSuggestion`][flet.] must have at least a
            [`key`][flet.AutoCompleteSuggestion.] or
            [`value`][flet.AutoCompleteSuggestion.] specified, else it will be
            ignored. If only `key` is provided, `value` will be set to `key` as
            fallback and vice versa.
        - The internal filtration process of the suggestions (based on their `key`s)
            with respect to the user's input is case-insensitive because the
            comparison is done in lowercase.
    """

    suggestions_max_height: Number = 200
    """
    The maximum - visual - height of the suggestions list.
    """

    on_select: Optional[EventHandler[AutoCompleteSelectEvent]] = None
    """
    Called when a suggestion is selected.
    """

    on_change: Optional[ControlEventHandler["AutoComplete"]] = None
    """
    Called when the input text changes.
    """

    @property
    def selected_index(self) -> Optional[int]:
        """
        The index of the (last) selected suggestion.

        It is `None` until a suggestion has been selected from the UI.

        Note:
            This property is read-only.
        """
        return getattr(self, "_selected_index", None)
