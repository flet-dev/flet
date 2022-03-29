from dataclasses import dataclass
from dataclasses import field
from datetime import date
from datetime import datetime
from datetime import time
from enum import Enum

from beartype.typing import List
from flet import Button
from flet import Checkbox
from flet import ChoiceGroup
from flet import ComboBox
from flet import Dropdown
from flet import Form
from flet import Message
from flet import SpinButton
from flet import Stack
from flet import Textbox
from flet.form import ListControl


class SelectionData(str, Enum):
    A = "a"
    B = "b"
    C = "c"


class MoreSelectionData(str, Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"


@dataclass
class ContainedObject:
    contained_value: str = "a"


@dataclass
class TopLevelData:
    string: str = "a"
    integer: int = 1
    floating_point: float = 0.1
    boolean: bool = True
    date_time: datetime = datetime(2022, 2, 2, 2, 2, 2)
    just_date: date = date(2022, 2, 2)
    just_time: time = time(2, 2, 2)
    selection: SelectionData = SelectionData.A
    dropdown_for_more_than_three_values: MoreSelectionData = MoreSelectionData.A
    multiple_selection: List[SelectionData] = field(default_factory=lambda: [SelectionData.A, SelectionData.B])
    list_of_fields: List[str] = field(default_factory=lambda: ["a", "b", "c"])
    contained_object: ContainedObject = field(default_factory=ContainedObject)
    list_of_contained_objects: List[ContainedObject] = field(default_factory=lambda: [ContainedObject()])


def test_form_empty(control_type_tree):
    form = Form(TopLevelData())

    assert control_type_tree(form) == {
        Form: [
            {Stack: [{Stack: ["String"]}, {Stack: [Textbox, Message]}]},
            {Stack: [{Stack: ["Integer"]}, {Stack: [SpinButton, Message]}]},
            {Stack: [{Stack: ["Floating point"]}, {Stack: [SpinButton, Message]}]},
            {Stack: [{Stack: ["Boolean"]}, {Stack: [Checkbox, Message]}]},
            {Stack: [{Stack: ["Date time"]}, {Stack: [Textbox, Message]}]},
            {Stack: [{Stack: ["Just date"]}, {Stack: [Textbox, Message]}]},
            {Stack: [{Stack: ["Just time"]}, {Stack: [Textbox, Message]}]},
            {Stack: [{Stack: ["Selection"]}, {Stack: [ChoiceGroup, Message]}]},
            {Stack: [{Stack: ["Dropdown for more than three values"]}, {Stack: [Dropdown, Message]}]},
            {Stack: [{Stack: ["Multiple selection"]}, {Stack: [ComboBox, Message]}]},
            {
                Stack: [
                    {Stack: ["List of fields", Button]},
                    {
                        Stack: [
                            {
                                ListControl: [
                                    {Stack: [Textbox, Button]},
                                    {Stack: [Textbox, Button]},
                                    {Stack: [Textbox, Button]},
                                ]
                            },
                            Message,
                        ]
                    },
                ]
            },
            {
                Stack: [
                    {Stack: ["Contained object"]},
                    {Stack: [{Stack: [{Stack: [{Stack: ["Contained value"]}, {Stack: [Textbox, Message]}]}]}]},  # str
                ]
            },
            {
                Stack: [
                    {Stack: ["List of contained objects", Button]},
                    {
                        Stack: [
                            {
                                ListControl: [
                                    {Stack: [Button, Button, Button]},
                                    Stack,
                                ]
                            },
                            Message,
                        ]
                    },
                ]
            },
            {Stack: [Message, Button]},  # Submit button
        ]
    }
