from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import pytest

import flet as ft
from flet.controls.base_page import PageMediaData
from flet.controls.padding import Padding
from flet.utils import from_dict


def test_page_media_data():
    pm = from_dict(
        PageMediaData,
        {
            "padding": {"left": 1, "top": 2, "right": 3, "bottom": 4},
            "view_padding": {"left": 1, "top": 2, "right": 3, "bottom": 4},
            "view_insets": {"left": 1, "top": 2, "right": 3, "bottom": 4},
            "device_pixel_ratio": 1,
            "orientation": "portrait",
        },
    )

    assert isinstance(pm, PageMediaData)
    assert isinstance(pm.padding, Padding)
    assert isinstance(pm.view_insets, Padding)
    assert isinstance(pm.view_padding, Padding)
    assert pm.padding._prev_left == 1
    assert pm.view_insets._prev_top == 2


def test_simple():
    class Status(Enum):
        ACTIVE = "active"
        INACTIVE = "inactive"

    @dataclass
    class Address:
        city: str
        zip: str

    @dataclass
    class User:
        name: str
        age: Optional[int]
        status: Status
        address: Optional[Address]
        tags: list[str]
        metadata: dict[str, int]

    user_data = {
        "name": "Alice",
        "age": 30,
        "status": "active",
        "address": {"city": "Springfield", "zip": "12345"},
        "tags": ["admin", "beta"],
        "metadata": {"logins": 10, "likes": 42},
    }

    user = from_dict(User, user_data)
    assert isinstance(user, User)
    assert isinstance(user.address, Address)
    assert isinstance(user.status, Status)
    assert user._prev_name == "Alice"
    assert user._prev_age == 30
    assert user.address._prev_city == "Springfield"
    assert user._prev_status == Status.ACTIVE


@pytest.mark.parametrize(
    "annotation", [Union[ft.Offset, str, None], ft.Offset | str | None]
)
def test_optional_union_decodes_nested_dataclass(annotation):
    @dataclass
    class Payload:
        position: annotation

    position = from_dict(Payload, {"position": {"x": 1, "y": 2}}).position
    assert isinstance(position, ft.Offset)
    assert (position.x, position.y) == (1, 2)
    assert from_dict(Payload, {"position": "center"}).position == "center"
    assert from_dict(Payload, {"position": None}).position is None


def test_optional_union_decodes_nested_containers():
    @dataclass
    class Payload:
        positions: list[ft.Offset] | dict[str, ft.Offset] | None

    point = {"x": 1, "y": 2}
    assert from_dict(Payload, {"positions": [point]}).positions[0].x == 1
    assert from_dict(Payload, {"positions": {"start": point}}).positions["start"].y == 2


def test_ambiguous_optional_union_preserves_first_type():
    @dataclass
    class Payload:
        position: Union[ft.Offset, dict[str, float], None]
        coordinates: Union[dict[str, float], ft.Offset, None]

    point = {"x": 1, "y": 2}
    payload = from_dict(Payload, {"position": point, "coordinates": point})
    assert isinstance(payload.position, ft.Offset)
    assert payload.coordinates == point


@pytest.mark.parametrize(
    "event_type", [ft.KeyboardEvent, ft.KeyDownEvent, ft.KeyUpEvent, ft.KeyRepeatEvent]
)
def test_keyboard_event_key_decoding(event_type):
    data = {"name": "key", "control": None}
    if event_type is ft.KeyboardEvent:
        data.update(shift=False, ctrl=False, alt=False, meta=False)

    legacy = from_dict(event_type, {**data, "key": "Arrow Right"})
    assert legacy.key is ft.KeyboardKey.ARROW_RIGHT
    assert legacy.physical_key is None

    azerty = from_dict(event_type, {**data, "key": "Z", "physical_key": 0x0007001A})
    assert azerty.key is ft.KeyboardKey.Z
    assert azerty.physical_key is ft.PhysicalKeyboardKey.W
    unknown = from_dict(event_type, {**data, "key": "Ü", "physical_key": 0xFFFF0001})
    assert type(unknown.key) is str
    assert unknown.key == "Ü"
    assert type(unknown.physical_key) is int
    assert unknown.physical_key == 0xFFFF0001
