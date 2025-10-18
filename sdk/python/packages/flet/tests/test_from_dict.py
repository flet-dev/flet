from dataclasses import dataclass
from enum import Enum
from typing import Optional

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
