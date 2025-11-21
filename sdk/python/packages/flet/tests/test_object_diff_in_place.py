from dataclasses import field
from typing import Any, Optional

from pytest import raises

import flet as ft
from flet.components.component import Component
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
    MyText,
    b_unpack,
    cmp_ops,
    make_diff,
    make_msg,
)


@control
class SuperButton(Button):
    prop_2: Optional[str] = None

    def init(self):
        pass

    def build(self):
        print("SuperButton.build()")
        assert self.page


@control("MyButton")
class MyButton(Button):
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
    btn = Button("some button")
    assert btn._c == "Button"


def test_control_id():
    btn = Button("some button")
    assert btn._i > 0


def test_inherited_control_has_the_same_type():
    btn = SuperButton(prop_2="2")
    assert btn._c == "Button"


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
    page._user_services._services.append(MyService(prop_1="Hello", prop_2=[1, 2, 3]))

    # page and window have hard-coded IDs
    assert page._i == 1
    assert page.window and page.window._i == 2

    msg, _, _, added_controls, removed_controls = make_msg(page, {}, show_details=True)
    u_msg = b_unpack(msg)
    assert len(added_controls) == 13
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
        SuperButton(
            "Button 😬",
            style=ButtonStyle(color=Colors.RED),
            on_click=lambda e: print(e),
            opacity=1,
            ref=None,
        ),
        SuperButton("Another Button"),
    ]
    del page.fonts["font2"]
    with raises(RuntimeError):
        assert page.controls[0].controls[0].page is None

    page._user_services._services[0].prop_2 = [2, 6]

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
                # "value": [SuperButton, SuperButton],
            },
            {"op": "remove", "path": ["fonts", "font2"], "value": "font_url_2"},
            {
                "op": "remove",
                "path": ["_user_services", "_services", 0, "prop_2", 0],
                "value": 1,
            },
            {
                "op": "add",
                "path": ["_user_services", "_services", 0, "prop_2", 1],
                "value": 6,
            },
            {
                "op": "remove",
                "path": ["_user_services", "_services", 0, "prop_2", 2],
                "value": 3,
            },
        ],
    )
    assert len(patch[2]["value"]) == 2
    assert isinstance(patch[2]["value"][0], SuperButton)
    assert isinstance(patch[2]["value"][1], SuperButton)

    # replace control in a list
    page.controls[0].controls[0] = SuperButton("Foo")
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
                "value": SuperButton("Foo"),
            },
        ],
    )

    # insert a new button to the start of a list
    page.controls[0].controls.insert(0, SuperButton("Bar"))
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
                "value_type": SuperButton,
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
            expand=True,
            content=ft.Container(
                content=counter,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.YELLOW,
                expand=True,
            ),
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
                "value": ft.Text("A new button content"),
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
            {
                "op": "add",
                "path": ["views", 0, "controls", 1],
                "value": ft.Text("Line 2"),
            },
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
    assert col.controls[1].value == "Line 2"
    assert col.controls[2].value == "Line 1"
    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
        ],
    )


def test_overriding_controls_with_component():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))

    # initial update
    make_msg(page, {}, show_details=True)

    # replace .controls with a component
    page.controls = Component(
        fn=lambda: ft.Text("Hello from component"), args=(), kwargs={}
    )

    patch, _, added_controls, removed_controls = make_diff(page, show_details=True)
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["views", 0, "controls"],
                "value_type": Component,
            },
        ],
    )

    # second update
    page.title = "Something"
    page.theme_mode = ft.ThemeMode.DARK
    patch, _, added_controls, removed_controls = make_diff(page, show_details=True)
    print(patch)

    # 3rd update
    page.title = "Bar"
    page.theme_mode = ft.ThemeMode.DARK
    patch, _, added_controls, removed_controls = make_diff(page, show_details=True)
    print(patch)


def test_list_insertions():
    col = ft.Column(
        [
            ft.Text("Line 2"),
            ft.Text("Line 4"),
            ft.Text("Line 6"),
            ft.Text("Line 8"),
        ]
    )
    _, patch, _, _, _ = make_msg(col, {})

    # 1st update
    col.controls[0] = ft.Text("Line 2 (updated)")
    col.controls[1] = ft.Text("Line 4 (updated)")
    col.controls[2] = ft.Text("Line 6 (updated)")

    patch, _, _, _ = make_diff(col)
    assert cmp_ops(
        patch,
        [
            {
                "op": "remove",
                "path": ["controls", 0],
                "value": ft.Text("Line 2"),
            },
            {
                "op": "remove",
                "path": ["controls", 0],
                "value": ft.Text("Line 4"),
            },
            {
                "op": "replace",
                "path": ["controls", 0],
                "value": ft.Text("Line 2 (updated)"),
            },
            {
                "op": "add",
                "path": ["controls", 1],
                "value": ft.Text("Line 4 (updated)"),
            },
            {
                "op": "add",
                "path": ["controls", 2],
                "value": ft.Text("Line 6 (updated)"),
            },
        ],
    )

    # 2nd update
    col.controls.insert(0, ft.Text("Line 1"))
    col.controls.insert(2, ft.Text("Line 3"))
    col.controls.insert(4, ft.Text("Line 5"))
    col.controls.insert(6, ft.Text("Line 7"))
    col.controls[3].value = "Line 4 (updated again)"

    patch, _, _, _ = make_diff(col)
    assert cmp_ops(
        patch,
        [
            {"op": "add", "path": ["controls", 0], "value": ft.Text("Line 1")},
            {"op": "add", "path": ["controls", 2], "value": ft.Text("Line 3")},
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated again)",
            },
            {"op": "add", "path": ["controls", 4], "value": ft.Text("Line 5")},
            {"op": "add", "path": ["controls", 6], "value": ft.Text("Line 7")},
        ],
    )


def test_list_move_1_no_keys():
    line_1 = MyText("Line 1")
    line_2 = MyText("Line 2")
    line_3 = MyText("Line 3")
    line_4 = MyText("Line 4")
    line_5 = MyText("Line 5")

    col_1 = [
        line_1,
        line_2,
        line_3,
        line_4,
        line_5,
    ]

    col_2 = [
        MyText("Line 0"),
        line_4,
        line_3,
        line_5,
        MyText("Line 6"),
    ]

    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": [0], "value": MyText("Line 1")},
            {"op": "replace", "path": [0], "value": MyText("Line 0")},
            {"op": "move", "from": [2], "path": [1]},
            {"op": "add", "path": [4], "value": MyText("Line 6")},
        ],
    )


def test_fields_start_with_on():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))
    page.controls = [Div(cls="div_1", some_value="Text")]
    page.on_login = lambda e: print("on login")
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(on_surface_variant=ft.Colors.RED),
    )

    msg, _, _, _, _ = make_msg(page, {}, show_details=True)
    u_msg = b_unpack(msg)

    print(u_msg)

    # page
    p = u_msg[1][3]
    # print("\n\n", p)
    assert p["on_login"]
    assert p["theme"]["color_scheme"]["on_surface_variant"] == "red"

    # update
    page.on_login = None
    page.theme.color_scheme.on_surface_variant = ft.Colors.BLUE

    msg, _, _, _, _ = make_msg(page, show_details=True)
    u_msg = b_unpack(msg)
    # print("\n\n", u_msg[1])
    assert u_msg[1][2] == "on_login"
    assert not u_msg[1][3]
    assert u_msg[2][2] == "on_surface_variant"
    assert u_msg[2][3] == "blue"


def test_list_with_keys_can_be_updated():
    col = ft.Column(
        [
            ft.Text("Line 1", key=ft.ScrollKey(1)),
            ft.Text("Line 2", key=ft.ScrollKey(2)),
        ]
    )
    _, patch, _, _, _ = make_msg(col, {})

    # 1st update
    col.controls.append(ft.Text("Line 3", key=ft.ScrollKey(3)))

    patch, _, _, _ = make_diff(col)
    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["controls", 2],
                "value": Text("Line 3", key=ft.ScrollKey(3)),
            }
        ],
    )

    col.controls[2].value = "Line 3 (updated)"


def test_list_without_keys_children_must_be_updated():
    col = ft.Column(
        [
            ft.Text("Line 1"),
            ft.Text("Line 2"),
            ft.Text("Line 3"),
            ft.Text("Line 4"),
        ]
    )
    _, patch, _, _, _ = make_msg(col, {})

    # 1st update
    col.controls.insert(0, col.controls.pop(2))
    col.controls[0].value = "Line 3 (updated)"
    col.controls[1].value = "Line 1 (updated)"
    col.controls[2].value = "Line 2 (updated)"

    patch, _, _, _ = make_diff(col)
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["controls", 2, "value"],
                "value": "Line 3 (updated)",
            },
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 1 (updated)",
            },
            {
                "op": "replace",
                "path": ["controls", 2, "value"],
                "value": "Line 2 (updated)",
            },
        ],
    )
