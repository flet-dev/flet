import pytest
from flet.core.padding import Padding
from flet.core.page import PageMediaData
from flet.utils import from_dict


def test_page_media_data():
    pm = from_dict(
        PageMediaData,
        {
            "target": 1,
            "name": "on_media",
            "data": None,
            "control": None,
            "page": None,
            "padding": {"left": 1, "top": 2, "right": 3, "bottom": 4},
            "view_padding": {"left": 1, "top": 2, "right": 3, "bottom": 4},
            "view_insets": {"left": 1, "top": 2, "right": 3, "bottom": 4},
        },
    )
    print(pm)
