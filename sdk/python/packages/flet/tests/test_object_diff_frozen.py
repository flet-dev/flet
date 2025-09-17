from dataclasses import dataclass
from typing import Optional

import pytest

import flet as ft
from flet.components.component import Component
from flet.controls.base_control import BaseControl, control
from flet.controls.object_patch import ObjectPatch

from .common import (
    LineChart,
    LineChartData,
    LineChartDataPoint,
    cmp_ops,
    make_diff,
    make_msg,
)


def test_compare_roots():
    c1 = {}
    c2 = ft.Column()
    c2._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert len(patch) == 1
    assert cmp_ops(patch, [{"op": "replace", "path": [], "value_type": ft.Column}])


def test_compare_literals_removed():
    c1 = ft.Column([1, 2, 3, 4, 5, 6, 7, 8])
    c2 = ft.Column([1, 4, 5, 5])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["controls", 1], "value": 2},
            {"op": "replace", "path": ["controls", 1], "value": 5},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
            {"op": "remove", "path": ["controls", 4], "value": 6},
            {"op": "remove", "path": ["controls", 4], "value": 7},
            {"op": "remove", "path": ["controls", 4], "value": 8},
        ],
    )


def test_compare_literals_added():
    c1 = ft.Column([1, 2, 3, 4, 5])
    c2 = ft.Column([1, 4, 5, 6, 7, 8, 9])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["controls", 1], "value": 2},
            {"op": "remove", "path": ["controls", 1], "value": 3},
            {"op": "move", "from": ["controls", 1], "path": ["controls", 1]},
            {"op": "add", "path": ["controls", 2], "value": 6},
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
            {"op": "add", "path": ["controls", 4], "value": 7},
            {"op": "add", "path": ["controls", 5], "value": 8},
            {"op": "add", "path": ["controls", 6], "value": 9},
        ],
    )


def test_compare_literals_replaced():
    c1 = ft.Column([1, 2])
    c2 = ft.Column([3, 4, 5])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 0], "value": 3},
            {"op": "replace", "path": ["controls", 1], "value": 4},
            {"op": "add", "path": ["controls", 2], "value": 5},
        ],
    )


def test_compare_objects_replaced_no_keys():
    @dataclass
    class Item:
        x: int
        y: int

    c1 = ft.Column(
        [
            Item(3, 1),
            Item(4, 1),
        ],
    )
    c2 = ft.Column(
        [
            Item(1, 0),
            Item(2, 0),
            Item(3, 0),
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 0, "x"], "value": 1},
            {"op": "replace", "path": ["controls", 0, "y"], "value": 0},
            {"op": "replace", "path": ["controls", 1, "x"], "value": 2},
            {"op": "replace", "path": ["controls", 1, "y"], "value": 0},
            {"op": "add", "path": ["controls", 2], "value_type": Item},
        ],
    )


def test_compare_objects_replaced_with_control_keys():
    @dataclass
    class Item:
        key: int
        y: int

    c1 = ft.Column(
        [
            Item(3, 1),
            Item(4, 1),
        ],
    )
    c2 = ft.Column(
        [
            Item(1, 0),
            Item(2, 0),
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 0], "value_type": Item},
            {"op": "replace", "path": ["controls", 1], "value_type": Item},
        ],
    )
    assert patch[0]["value"].key == 1
    assert patch[0]["value"].y == 0
    assert patch[1]["value"].key == 2
    assert patch[1]["value"].y == 0


def test_compare_objects_updated_and_moved_with_control_keys():
    @control("Item")
    class Item(BaseControl):
        y: int

    c1 = ft.Column(
        [
            Item(key=2, y=0),
            Item(key=1, y=0),
        ],
    )
    c2 = ft.Column(
        [
            Item(key=1, y=1),
            Item(key=2, y=2),
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 0, "y"], "value": 1},
            {"op": "replace", "path": ["controls", 1, "y"], "value": 2},
            {"op": "move", "from": ["controls", 0], "path": ["controls", 1]},
        ],
    )


def test_compare_objects_added():
    @control("Item")
    class Item(BaseControl):
        y: int

    c1 = ft.Column(
        [
            Item(key=3, y=1),
            Item(key=4, y=1),
            Item(key=5, y=1),
            Item(key=6, y=1),
        ],
    )
    c2 = ft.Column(
        [
            Item(key=1, y=0),
            Item(key=2, y=0),
            Item(key=4, y=0),
            Item(key=3, y=0),
            Item(key=5, y=0),
            Item(key=6, y=0),
            Item(key=7, y=0),
            Item(key=8, y=0),
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "add", "path": ["controls", 0], "value_type": Item},
            {"op": "add", "path": ["controls", 1], "value_type": Item},
            {"op": "replace", "path": ["controls", 2, "y"], "value": 0},
            {"op": "replace", "path": ["controls", 3, "y"], "value": 0},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 3]},
            {"op": "replace", "path": ["controls", 4, "y"], "value": 0},
            {"op": "replace", "path": ["controls", 5, "y"], "value": 0},
            {"op": "add", "path": ["controls", 6], "value_type": Item},
            {"op": "add", "path": ["controls", 7], "value_type": Item},
        ],
    )


def test_compare_controls():
    def on_scroll(e):
        pass

    r1 = ft.Row(
        controls=[ft.Text("Hello"), ft.Text("World")],
        spacing=10,
        scale=ft.Scale(0.5, scale_x=0.1, scale_y=0.2),
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        on_scroll=on_scroll,
    )
    r2 = ft.Row(
        controls=[ft.Text("Hello"), ft.Text("World")],
        spacing=10,
        scale=ft.Scale(0.5, scale_x=0.1, scale_y=0.2),
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        on_scroll=on_scroll,
    )
    assert r1 == r2

    dp1 = LineChartDataPoint(x=10, y=20)
    dp2 = LineChartDataPoint(x=10, y=20)
    assert dp1 == dp2

    dp3 = dp2
    assert dp2 is dp3

    r3 = ft.Row(spacing=20)
    r4 = ft.Row(spacing=10)
    assert r3 != r4


def test_button_basic_diff():
    b1 = ft.Button(content="Hello")
    b2 = ft.Button(
        content="Click me",
        style=ft.ButtonStyle(color=ft.Colors.RED),
        scale=ft.Scale(0.2),
    )
    b1._frozen = True
    b2._frozen = True

    # initial iteration
    patch, _, _, _ = make_diff(b2, {})
    assert not hasattr(b2, "__prev_classes")
    assert isinstance(patch[0]["value"], ft.Button)

    # 2nd iteration
    patch, _, _, _ = make_diff(b2, b1)
    assert len(patch) == 3
    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["_internals", "style"],
                "value": ft.ButtonStyle(color=ft.Colors.RED, elevation=1),
            },
            {"op": "replace", "path": ["scale"], "value": ft.Scale(0.2)},
            {"op": "replace", "path": ["content"], "value": "Click me"},
        ],
    )

    # 3rd iteration
    b3 = ft.Button(content=ft.Text("Text_1"), style=None, scale=ft.Scale(0.1))
    b3._frozen = True
    patch, _, _, _ = make_diff(b3, b2)
    assert cmp_ops(
        patch,
        [
            {
                "op": "remove",
                "path": ["_internals", "style"],
                "value": ft.ButtonStyle(color=ft.Colors.RED, elevation=1),
            },
            {"op": "replace", "path": ["scale", "scale"], "value": 0.1},
            {"op": "replace", "path": ["content"], "value": ft.Text("Text_1")},
        ],
    )


def test_lists_with_key_diff():
    c1 = LineChart(
        data_series=[
            LineChartData(
                points=[
                    LineChartDataPoint(key=0, x=0, y=1),
                    LineChartDataPoint(key=1, x=1, y=2),
                    LineChartDataPoint(key=2, x=2, y=3),
                ]
            )
        ]
    )
    c2 = LineChart(
        data_series=[
            LineChartData(
                points=[
                    LineChartDataPoint(key=1, x=1, y=2),
                    LineChartDataPoint(key=2, x=2, y=2),
                    LineChartDataPoint(key=3, x=3, y=5),
                ]
            )
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert c2._frozen
    assert c2.data_series[0]._frozen
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["data_series", 0, "points", 0]},
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 1, "y"],
                "value": 2,
            },
            {
                "op": "add",
                "path": ["data_series", 0, "points", 2],
                "value_type": LineChartDataPoint,
            },
        ],
    )
    assert patch[2]["value"].x == 3
    assert patch[2]["value"].y == 5


def test_lists_with_no_key_diff():
    c1 = LineChart(
        data_series=[
            LineChartData(
                points=[
                    LineChartDataPoint(x=0, y=1),
                    LineChartDataPoint(x=1, y=2),
                    LineChartDataPoint(x=2, y=3),
                ]
            )
        ]
    )
    c2 = LineChart(
        data_series=[
            LineChartData(
                points=[
                    LineChartDataPoint(x=1, y=2),
                    LineChartDataPoint(x=2, y=2),
                    LineChartDataPoint(x=3, y=5),
                ]
            )
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert c2._frozen
    assert c2.data_series[0]._frozen
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 0, "x"],
                "value": 1,
            },
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 0, "y"],
                "value": 2,
            },
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 1, "x"],
                "value": 2,
            },
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 2, "x"],
                "value": 3,
            },
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 2, "y"],
                "value": 5,
            },
        ],
    )


def test_simple_lists_diff_1():
    c1 = LineChart(data_series=[LineChartData(points=[1, 2, 3])])
    c2 = LineChart(data_series=[LineChartData(points=[2, 3, 4])])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["data_series", 0, "points", 0], "value": 1},
            {"op": "add", "path": ["data_series", 0, "points", 2], "value": 4},
        ],
    )


def test_simple_lists_diff_2():
    c1 = LineChart(data_series=[LineChartData(points=[1, 2, 3, 4])])
    c2 = LineChart(data_series=[LineChartData(points=[1, 3, 4])])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["data_series", 0, "points", 1], "value": 2},
        ],
    )


def test_similar_lists_diff():
    c1 = LineChart(data_series=[LineChartData(points=[ft.Scale(0), ft.Scale(1)])])
    c2 = LineChart(data_series=[LineChartData(points=[ft.Scale(1), ft.Scale(2)])])
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 0, "scale"],
                "value": 1,
            },
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 1, "scale"],
                "value": 2,
            },
        ],
    )


def test_lists_in_place():
    c1 = LineChart(
        data_series=[
            LineChartData(
                points=[
                    LineChartDataPoint(x=0, y=1),
                    LineChartDataPoint(x=1, y=2),
                    LineChartDataPoint(x=2, y=3),
                ]
            )
        ]
    )
    _, patch, _, _, _ = make_msg(c1, {})

    # 1st change
    c1.data_series[0].points.pop(0)
    c1.data_series[0].points[1].y = 10
    c1.data_series[0].points.append(LineChartDataPoint(x=3, y=4))
    c1.data_series.append(
        LineChartData(
            points=[
                LineChartDataPoint(x=10, y=20),
            ]
        )
    )
    patch, msg, added_controls, removed_controls = make_diff(c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["data_series", 0, "points", 0]},
            {
                "op": "replace",
                "path": ["data_series", 0, "points", 1, "y"],
                "value": 10,
            },
            {
                "op": "add",
                "path": ["data_series", 0, "points", 2],
                "value_type": LineChartDataPoint,
            },
            {"op": "add", "path": ["data_series", 1], "value_type": LineChartData},
        ],
    )


def test_both_frozen_hosted_by_in_place():
    def chart(data):
        r = LineChart(
            data_series=[
                LineChartData(
                    points=[
                        LineChartDataPoint(key=dp[0], x=dp[0], y=dp[1]) for dp in ds
                    ]
                )
                for ds in data
            ]
        )
        r._frozen = True
        return r

    c = ft.Container(content=chart([[(0, 1), (1, 1), (2, 2)], [(10, 20), (20, 30)]]))
    assert not hasattr(c, "_frozen")
    _, patch, _, added_controls, removed_controls = make_msg(c, {})
    assert len(added_controls) == 9
    assert len(removed_controls) == 0
    assert hasattr(c, "__changes")
    assert not hasattr(c, "_frozen")

    c.alignment = ft.Alignment.BOTTOM_CENTER
    c.bgcolor = ft.Colors.AMBER
    ch = chart([[(1, 1), (2, 2), (3, 3)]])
    c.content = ch
    patch, _, added_controls, removed_controls = make_diff(c, c)
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    # for rc in removed_controls:
    #     print("\nREMOVED CONTROL:", rc)
    # 5 x Added controls: LineChart + LineChartData +
    # 3 x LineChartDataPoint (2 moved and 1 new)
    assert len(added_controls) == 5
    # 3 x Removed controls: LineChart + 2 x LineChartData + 5 x LineChartDataPoint
    assert len(removed_controls) == 8
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["alignment"], "value": ft.Alignment(x=0, y=1)},
            {"op": "replace", "path": ["bgcolor"], "value": ft.Colors.AMBER},
            {"op": "remove", "path": ["content", "data_series", 0, "points", 0]},
            {
                "op": "add",
                "path": ["content", "data_series", 0, "points", 2],
                "value_type": LineChartDataPoint,
            },
            {
                "op": "remove",
                "path": ["content", "data_series", 1],
                "value_type": LineChartData,
            },
        ],
    )
    assert hasattr(ch, "_frozen")
    with pytest.raises(Exception, match="Frozen controls cannot be updated."):
        ch.width = 100


def test_larger_control_updates():
    c1 = ft.Container(
        content=ft.Row([ft.Text("Text 1")]),
        bgcolor=ft.Colors.YELLOW,
        width=200,
        height=100,
        scale=ft.Scale(1.0),
    )
    c1._frozen = True
    c2 = ft.Container(
        content=ft.Row([ft.Text("Text 2")]),
        bgcolor=ft.Colors.RED,
        width=200,
        scale=ft.Scale(2.0),
    )
    c2._frozen = True
    patch, msg, added_controls, removed_controls = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["height"], "value": None},
            {"op": "replace", "path": ["scale", "scale"], "value": 2.0},
            {
                "op": "replace",
                "path": ["content", "controls", 0, "value"],
                "value": "Text 2",
            },
            {"op": "replace", "path": ["bgcolor"], "value": ft.Colors.RED},
        ],
    )


@dataclass
class User:
    id: int
    name: str
    age: int
    verified: bool


users = [
    User(1, "John Smith", 20, True),
    User(2, "Alice Wong", 32, True),
    User(3, "Bob Bar", 40, False),
]


def test_control_builder():
    @dataclass
    class State:
        msg: str

    state = State(msg="some text")

    dv = ft.StateView(state, builder=lambda state: ft.Text(state.msg))
    _, patch, _, added_controls, removed_controls = make_msg(dv, {})
    assert len(added_controls) == 2
    assert len(removed_controls) == 0
    assert cmp_ops(
        patch,
        [{"op": "replace", "path": [], "value_type": ft.StateView}],
    )
    assert isinstance(patch[0]["value"].content, ft.Text)
    assert hasattr(patch[0]["value"].content, "_frozen")
    assert patch[0]["value"].content.value == "some text"

    state.msg = "Hello, world!"
    patch, msg, added_controls, removed_controls = make_diff(dv, dv)
    assert len(patch) == 1
    assert cmp_ops(
        patch,
        [{"op": "replace", "path": ["content", "value"], "value": "Hello, world!"}],
    )


def test_nested_control_builders():
    @dataclass
    class AppState:
        count: int

    state = AppState(count=0)

    cb = ft.StateView(
        state,
        lambda state: ft.SafeArea(
            ft.Container(
                ft.StateView(
                    state,
                    lambda state: ft.Text(
                        value=f"{state.count}",
                        spans=(
                            [
                                ft.TextSpan(
                                    f"SPAN {state.count}",
                                    on_click=lambda: print("span clicked!"),
                                )
                            ]
                            if state.count > 0
                            else []
                        ),
                        size=50,
                    ),
                ),
                alignment=ft.Alignment.CENTER,
            ),
            expand=True,
        ),
        expand=True,
    )
    _, patch, _, added_controls, removed_controls = make_msg(cb, {})
    assert len(added_controls) == 5
    assert len(removed_controls) == 0
    assert not hasattr(patch[0]["value"], "_frozen")  # StateView
    assert hasattr(patch[0]["value"].content, "_frozen")  # SafeArea
    assert hasattr(patch[0]["value"].content.content, "_frozen")  # Center
    assert hasattr(
        patch[0]["value"].content.content.content, "_frozen"
    )  # StateView (nested)
    assert hasattr(patch[0]["value"].content.content.content.content, "_frozen")  # Text

    state.count = 10
    patch, msg, added_controls, removed_controls = make_diff(cb, cb)
    assert len(added_controls) == 5
    assert len(removed_controls) == 4
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["content", "content", "content", "content", "value"],
                "value": "10",
            },
            {
                "op": "replace",
                "path": ["content", "content", "content", "content", "spans"],
                "value_type": list,
            },
        ],
    )
    assert isinstance(patch[1]["value"][0], ft.TextSpan)
    assert patch[1]["value"][0].text == "SPAN 10"
    assert hasattr(patch[1]["value"][0], "_frozen")  # TextSpan

    state.count = 0
    patch, msg, added_controls, removed_controls = make_diff(cb, cb)
    assert len(added_controls) == 4
    assert len(removed_controls) == 5
    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["content", "content", "content", "content", "value"],
                "value": "0",
            },
            {
                "op": "replace",
                "path": ["content", "content", "content", "content", "spans"],
                "value": [],
            },
        ],
    )


def test_view_with_cache():
    @ft.cache(freeze=True)
    def user_details(user: User):
        return ft.Card(
            ft.Column(
                [
                    ft.Text(f"Name: {user.name}"),
                    ft.Text(f"Age: {user.age}"),
                    ft.Checkbox(label="Verified", value=user.verified),
                ]
            ),
            key=user.id,
        )

    @ft.cache(freeze=True)
    def users_list(users):
        return ft.Column([user_details(user) for user in users])

    page = ft.Row([users_list(users)])

    _, patch, _, added_controls, removed_controls = make_msg(page, {})
    assert len(added_controls) == 17
    assert len(removed_controls) == 0

    # add new user
    users.append(User(4, name="Someone Else", age=99, verified=False))
    page.controls[0] = users_list(users)
    patch, msg, added_controls, removed_controls = make_diff(page, page)
    assert len(added_controls) == 6
    assert len(removed_controls) == 1
    assert cmp_ops(
        patch,
        [{"op": "add", "path": ["controls", 0, "controls", 3], "value_type": ft.Card}],
    )

    # Card ids: 9, 14, 19, 26

    # remove user
    del users[1]
    page.controls[0] = users_list(users)

    # OLD: 9, 14, 19, 26
    # NEW: 9, 19, 26

    patch, msg, added_controls, removed_controls = make_diff(page, page)
    assert cmp_ops(
        patch,
        [{"op": "remove", "path": ["controls", 0, "controls", 1]}],
    )
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    # for rc in removed_controls:
    #     print("\nREMOVED CONTROL:", rc)
    assert len(added_controls) == 1
    assert len(removed_controls) == 6


def test_empty_view():
    @ft.cache
    def my_view():
        return None

    v = my_view()
    assert v is None


def test_login_logout_view():
    class AppState:
        logged_username: Optional[str] = None

        def login(self, _):
            self.logged_username = "John"

        def logout(self, _):
            self.logged_username = None

    state = AppState()

    @ft.cache
    def login_view(state: AppState):
        return (
            ft.Column(
                [
                    ft.Text(state.logged_username),
                    ft.Button("Logout", on_click=state.logout),
                ]
            )
            if state.logged_username
            else ft.Column(
                [
                    ft.Button("Login", on_click=state.login),
                ]
            )
        )

    ft.View("/", [login_view(state)])


def test_component_single_control_diff():
    comp = Component(fn=lambda: None, args=(), kwargs={})
    old = ft.Button("Hey there!")
    new = ft.Button("Hello, world!")
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old, new, control_cls=ft.BaseControl, parent=comp, path=["_b"], frozen=True
    )
    assert cmp_ops(
        patch.patch,
        [{"op": "replace", "path": ["_b", "content"], "value": "Hello, world!"}],
    )


def test_component_list_diff():
    comp = Component(fn=lambda: None, args=(), kwargs={})
    old = [ft.Column([ft.Button("Hey there!")])]
    new = [
        c1 := ft.Column([btn1 := ft.Button("Hello, world!")]),
        txt1 := ft.Text("New control"),
    ]
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old, new, control_cls=ft.BaseControl, parent=comp, path=["_b"], frozen=True
    )
    assert cmp_ops(
        patch.patch,
        [
            {
                "op": "replace",
                "path": ["_b", 0, "controls", 0, "content"],
                "value": "Hello, world!",
            },
            {"op": "add", "path": ["_b", 1], "value_type": ft.Text},
        ],
    )
    assert c1._frozen
    assert btn1._frozen
    assert txt1._frozen
    assert c1.parent == comp
    assert btn1.parent == c1
    assert txt1.parent == comp


def test_list_insertions_no_keys():
    col_1 = ft.Column(
        [
            ft.Text("Line 2", key=2),
            ft.Text("Line 4", key=4),
            ft.Text("Line 6", key=6),
            ft.Text("Line 8", key=8),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            ft.Text("Line 1", key=1),
            ft.Text("Line 2 (updated)", key=2),
            ft.Text("Line 3", key=3),
            ft.Text("Line 4 (updated)", key=4),
            ft.Text("Line 5", key=5),
            ft.Text("Line 6 (updated)", key=6),
            ft.Text("Line 7", key=7),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["controls", 0],
                "value": ft.Text(value="Line 1", key=1),
            },
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 2 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 2],
                "value": ft.Text(value="Line 3", key=3),
            },
            {
                "op": "remove",
                "path": ["controls", 5],
                "value": ft.Text(value="Line 8", key=8),
            },
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 4],
                "value": ft.Text(value="Line 5", key=5),
            },
            {
                "op": "replace",
                "path": ["controls", 5, "value"],
                "value": "Line 6 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 6],
                "value": ft.Text(value="Line 7", key=7),
            },
        ],
    )
