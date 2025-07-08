from dataclasses import field
from typing import Any, Optional

import flet as ft
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.colors import Colors
from flet.controls.control import Control
from flet.controls.core.gesture_detector import GestureDetector
from flet.controls.core.text import Text
from flet.controls.events import DragUpdateEvent
from flet.controls.material.button import Button

# import flet as ft
# import flet.canvas as cv
from flet.controls.material.container import Container
from flet.controls.material.elevated_button import ElevatedButton
from flet.controls.page import Page
from flet.controls.painting import Paint, PaintLinearGradient
from flet.controls.ref import Ref
from flet.controls.services.service import Service
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

from .common import (
    LineChart,
    LineChartData,
    LineChartDataPoint,
    b_unpack,
    cmp_ops,
    make_diff,
    make_msg,
)


@control
class SuperElevatedButton(ElevatedButton):
    prop_2: Optional[str] = None

    def init(self):
        print("SuperElevatedButton.init()")
        assert self.page


@control("MyButton")
class MyButton(ElevatedButton):
    prop_1: Optional[str] = None


@control("MyService")
class MyService(Service):
    prop_1: Optional[str] = None
    prop_2: list[int] = field(default_factory=list)


@control("Span")
class Span(Control):
    text: Optional[str] = None
    cls: Optional[str] = None
    controls: list[Any] = field(default_factory=list)
    head_controls: list[Any] = field(default_factory=list)


@control("Div")
class Div(Control):
    cls: Optional[str] = None
    some_value: Any = None
    controls: list[Any] = field(default_factory=list)


def test_control_type():
    btn = ElevatedButton("some button")
    assert btn._c == "ElevatedButton"


def test_control_id():
    btn = ElevatedButton("some button")
    assert btn._i > 0


def test_inherited_control_has_the_same_type():
    btn = SuperElevatedButton(prop_2="2")
    assert btn._c == "ElevatedButton"


def test_inherited_control_with_overridden_type():
    btn = MyButton(prop_1="1")
    assert btn._c == "MyButton"


def test_control_ref():
    page_ref = Ref[Page]()
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn), ref=page_ref)

    assert page_ref.current == page


def test_simple_page():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))
    page.controls = [Div(cls="div_1", some_value="Text")]
    page.data = 100000
    page.bgcolor = Colors.GREEN
    page.fonts = {"font1": "font_url_1", "font2": "font_url_2"}
    page.on_login = lambda e: print("on login")
    page.services.append(MyService(prop_1="Hello", prop_2=[1, 2, 3]))

    # page and window have hard-coded IDs
    assert page._i == 1
    assert page.window and page.window._i == 2

    msg, _, _, added_controls, removed_controls = make_msg(page, {}, show_details=True)
    u_msg = b_unpack(msg)
    assert len(added_controls) == 14
    assert len(removed_controls) == 0

    assert page.parent is None
    assert page.controls[0].parent == page.views[0]
    assert page.clipboard
    assert page.clipboard.parent
    assert page.clipboard.page

    print(u_msg)

    assert isinstance(u_msg, list)
    assert u_msg[0] == [0]
    assert len(u_msg[1]) == 4
    p = u_msg[1][3]
    assert p["_i"] > 0
    assert p["on_login"]
    assert len(p["views"]) > 0
    assert "on_connect" not in p
    # assert u_msg == [
    #     [0],
    #     [
    #         0,
    #         0,
    #         0,
    #         {
    #             "_i": 1,
    #             "_c": "Page",
    #             "views": [
    #                 {
    #                     "_i": 17,
    #                     "_c": "View",
    #                     "controls": [
    #                         {
    #                             "_i": 29,
    #                             "_c": "Div",
    #                             "cls": "div_1",
    #                             "some_value": "Text",
    #                         }
    #                     ],
    #                     "bgcolor": "green",
    #                 }
    #             ],
    #             "_overlay": {"_i": 18, "_c": "Overlay"},
    #             "_dialogs": {"_i": 19, "_c": "Dialogs"},
    #             "window": {"_i": 2, "_c": "Window"},
    #             "browser_context_menu": {"_i": 21, "_c": "BrowserContextMenu"},
    #             "shared_preferences": {"_i": 22, "_c": "SharedPreferences"},
    #             "clipboard": {"_i": 23, "_c": "Clipboard"},
    #             "storage_paths": {"_i": 24, "_c": "StoragePaths"},
    #             "url_launcher": {"_i": 25, "_c": "UrlLauncher"},
    #             "_user_services": {
    #                 "_i": 26,
    #                 "_c": "ServiceRegistry",
    #                 "services": [
    #                     {
    #                         "_i": 30,
    #                         "_c": "MyService",
    #                         "prop_1": "Hello",
    #                         "prop_2": [1, 2, 3],
    #                     }
    #                 ],
    #             },
    #             "_page_services": {
    #                 "_i": 27,
    #                 "_c": "ServiceRegistry",
    #                 "services": [
    #                     {"_i": 21, "_c": "BrowserContextMenu"},
    #                     {"_i": 22, "_c": "SharedPreferences"},
    #                     {"_i": 23, "_c": "Clipboard"},
    #                     {"_i": 25, "_c": "UrlLauncher"},
    #                     {"_i": 24, "_c": "StoragePaths"},
    #                 ],
    #             },
    #             "fonts": {"font1": "font_url_1", "font2": "font_url_2"},
    #             "on_login": True,
    #         },
    #     ],
    # ]

    # update sub-tree
    page.on_login = None
    page.controls[0].some_value = "Another text"
    page.controls[0].controls = [
        SuperElevatedButton(
            "Button 😬",
            style=ButtonStyle(color=Colors.RED),
            on_click=lambda e: print(e),
            opacity=1,
            ref=None,
        ),
        SuperElevatedButton("Another Button"),
    ]
    del page.fonts["font2"]
    assert page.controls[0].controls[0].page is None

    page.services[0].prop_2 = [2, 6]

    # add 2 new buttons to a list
    _, patch, _, added_controls, removed_controls = make_msg(page, show_details=True)
    assert hasattr(page.views[0], "__changes")
    assert len(added_controls) == 2
    assert len(removed_controls) == 0
    assert len(patch) == 7
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["on_login"], "value": False},
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "some_value"],
                "value": "Another text",
            },
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "controls"],
                # "value": [SuperElevatedButton, SuperElevatedButton],
            },
            {"op": "remove", "path": ["fonts", "font2"], "value": "font_url_2"},
            {
                "op": "remove",
                "path": ["_user_services", "services", 0, "prop_2", 0],
                "value": 1,
            },
            {
                "op": "add",
                "path": ["_user_services", "services", 0, "prop_2", 1],
                "value": 6,
            },
            {
                "op": "remove",
                "path": ["_user_services", "services", 0, "prop_2", 2],
                "value": 3,
            },
        ],
    )
    assert len(patch[2]["value"]) == 2
    assert isinstance(patch[2]["value"][0], SuperElevatedButton)
    assert isinstance(patch[2]["value"][1], SuperElevatedButton)

    # replace control in a list
    page.controls[0].controls[0] = SuperElevatedButton("Foo")
    _, patch, _, added_controls, removed_controls = make_msg(page, show_details=True)
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    # for rc in removed_controls:
    #     print("\nREMOVED CONTROL:", rc)
    assert len(added_controls) == 1
    assert len(removed_controls) == 1
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "controls", 0],
                "value_type": SuperElevatedButton,
            }
        ],
    )

    # insert a new button to the start of a list
    page.controls[0].controls.insert(0, SuperElevatedButton("Bar"))
    page.controls[0].controls[1].content = "Baz"
    _, patch, _, added_controls, removed_controls = make_msg(page, show_details=True)
    assert len(added_controls) == 1
    assert len(removed_controls) == 0
    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["views", 0, "controls", 0, "controls", 0],
                "value_type": SuperElevatedButton,
            },
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "controls", 1, "content"],
                "value": "Baz",
            },
        ],
    )

    page.controls[0].controls.clear()
    _, patch, _, added_controls, removed_controls = make_msg(page, show_details=True)
    assert len(added_controls) == 0
    assert len(removed_controls) == 3
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "controls"],
                "value": [],
            }
        ],
    )


def test_floating_action_button():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))

    # initial update
    make_msg(page, {}, show_details=True)

    # second update
    counter = ft.Text("0", size=50, data=0)

    def btn_click(e):
        counter.data += 1
        counter.value = str(counter.data)
        counter.update()

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, on_click=btn_click
    )
    page.controls.append(
        ft.SafeArea(
            ft.Container(
                counter,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.YELLOW,
                expand=True,
            ),
            expand=True,
        ),
    )

    patch, _, added_controls, removed_controls = make_diff(page, show_details=True)
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["views", 0, "floating_action_button"],
                "value_type": ft.FloatingActionButton,
            },
            {"op": "replace", "path": ["views", 0, "controls"]},
        ],
    )
    assert len(patch[1]["value"]) == 1
    assert isinstance(patch[1]["value"][0], ft.SafeArea)


def test_changes_tracking():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))
    page.controls.append(
        btn := Button(Text("Click me!"), on_click=lambda e: print("clicked!"))
    )

    # initial update
    make_msg(page, {}, show_details=True)

    # second update
    btn.content = Text("A new button content")
    btn.width = 300
    btn.height = 100

    # t1 = Text("AAA")
    # t2 = Text("BBB")
    page.controls.append(Text("Line 2"))

    patch, _, added_controls, removed_controls = make_diff(page, show_details=True)
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "content"],
                "value_type": ft.Text,
            },
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "width"],
                "value": 300,
            },
            {
                "op": "replace",
                "path": ["views", 0, "controls", 0, "height"],
                "value": 100,
            },
            {"op": "add", "path": ["views", 0, "controls", 1], "value_type": ft.Text},
        ],
    )


def test_large_updates():
    import flet.canvas as cv

    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))

    def pan_update(e: DragUpdateEvent):
        pass

    page.controls.append(
        Container(
            cp := cv.Canvas(
                [
                    cv.Fill(
                        Paint(
                            gradient=PaintLinearGradient(
                                (0, 0), (600, 600), colors=[Colors.CYAN_50, Colors.GREY]
                            )
                        )
                    ),
                ],
                content=GestureDetector(
                    on_pan_update=pan_update,
                    drag_interval=30,
                ),
                expand=False,
            ),
            border_radius=5,
            width=float("inf"),
            expand=True,
        )
    )

    # initial update
    _, patch, _, added_controls, removed_controls = make_msg(
        page, {}, show_details=True
    )

    # second update
    for i in range(1, 1000):
        cp.shapes.append(
            cv.Line(i + 1, i + 100, i + 10, i + 20, paint=Paint(stroke_width=3))
        )

    make_msg(cp, show_details=False)

    cp.shapes[100].x1 = 12

    # third update
    for i in range(1, 20):
        cp.shapes.append(
            cv.Line(i + 1, i + 100, i + 10, i + 20, paint=Paint(stroke_width=3))
        )

    _, patch, _, added_controls, removed_controls = make_msg(cp, show_details=True)


def test_add_remove_lists():
    data = [[(0, 1), (1, 2), (2, 3)]]
    chart = LineChart(
        data_series=[
            LineChartData(
                points=[LineChartDataPoint(key=dp[0], x=dp[0], y=dp[1]) for dp in ds]
            )
            for ds in data
        ]
    )
    _, patch, _, _, _ = make_msg(chart, {})

    # add/remove
    chart.data_series[0].points.pop(0)
    chart.data_series[0].points.append(LineChartDataPoint(x=3, y=4))

    patch, _, _, _ = make_diff(chart, chart)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["data_series", 0, "points", 0]},
            {
                "op": "add",
                "path": ["data_series", 0, "points", 2],
                "value_type": LineChartDataPoint,
            },
        ],
    )


def test_reverse_list():
    col = ft.Column([ft.Text("Line 1"), ft.Text("Line 2"), ft.Text("Line 3")])
    _, patch, _, _, _ = make_msg(col, {})

    # reverse
    col.controls.reverse()
    patch, _, _, _ = make_diff(col)
    assert col.controls[0].value == "Line 3"
    assert col.controls[2].value == "Line 1"
    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {"op": "move", "from": ["controls", 1], "path": ["controls", 2]},
        ],
    )
