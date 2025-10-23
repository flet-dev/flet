from dataclasses import dataclass

import pytest

import flet as ft
from flet.components.component import Component
from flet.controls.base_control import BaseControl, control
from flet.controls.object_patch import ObjectPatch

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
            Item(key=3, y=1),
            Item(key=4, y=1),
        ],
    )
    c2 = ft.Column(
        [
            Item(key=1, y=0),
            Item(key=2, y=0),
        ]
    )
    c1._frozen = True
    patch, _, _, _ = make_diff(c2, c1)
    assert cmp_ops(
        patch,
        [
            {"op": "remove", "path": ["controls", 0], "value": Item(key=3, y=1)},
            {"op": "replace", "path": ["controls", 0], "value": Item(key=1, y=0)},
            {"op": "add", "path": ["controls", 1], "value": Item(key=2, y=0)},
        ],
    )
    assert patch[1]["value"].key == 1
    assert patch[1]["value"].y == 0
    assert patch[2]["value"].key == 2
    assert patch[2]["value"].y == 0


def test_compare_objects_updated_and_moved_with_control_keys():
    @control("Item")
    class Item(BaseControl):
        y: int

        def __str__(self):
            return f"Item(key={self.key}, y={self.y})"

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
            {"op": "replace", "path": ["controls", 1, "y"], "value": 1},
            {"op": "move", "from": ["controls", 1], "path": ["controls", 0]},
            {"op": "replace", "path": ["controls", 1, "y"], "value": 2},
        ],
    )


def test_compare_objects_added():
    @control("Item")
    class Item(BaseControl):
        y: int

        def __str__(self):
            return f"Item(key={self.key}, y={self.y})"

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
            Item(key=4, y=40),
            Item(key=3, y=30),
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
            {"op": "add", "path": ["controls", 0], "value": Item(key=1, y=0)},
            {"op": "add", "path": ["controls", 1], "value": Item(key=2, y=0)},
            {"op": "replace", "path": ["controls", 3, "y"], "value": 40},
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
            {"op": "replace", "path": ["controls", 3, "y"], "value": 30},
            {"op": "replace", "path": ["controls", 4, "y"], "value": 0},
            {"op": "replace", "path": ["controls", 5, "y"], "value": 0},
            {"op": "add", "path": ["controls", 6], "value": Item(key=7, y=0)},
            {"op": "add", "path": ["controls", 7], "value": Item(key=8, y=0)},
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
            {
                "op": "remove",
                "path": ["data_series", 0, "points", 0],
                "value": LineChartDataPoint(key=0, x=0, y=1),
            },
            {"op": "replace", "path": ["data_series", 0, "points", 1, "y"], "value": 2},
            {
                "op": "add",
                "path": ["data_series", 0, "points", 2],
                "value": LineChartDataPoint(key=3, x=3, y=5),
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


def test_list_insertions_with_keys():
    col_1 = ft.Column(
        [
            MyText("Line 2", key=2),
            MyText("Line 4", key=4),
            MyText("Line 6", key=6),
            MyText("Line 8", key=8),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2 (updated)", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4 (updated)", key=4),
            MyText("Line 5", key=5),
            MyText("Line 6 (updated)", key=6),
            MyText("Line 7", key=7),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["controls", 0],
                "value": MyText(key=1, value="Line 1"),
            },
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 2 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 2],
                "value": MyText(key=3, value="Line 3"),
            },
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 4],
                "value": MyText(key=5, value="Line 5"),
            },
            {
                "op": "replace",
                "path": ["controls", 5, "value"],
                "value": "Line 6 (updated)",
            },
            {
                "op": "replace",
                "path": ["controls", 6],
                "value": MyText(key=7, value="Line 7"),
            },
        ],
    )


def test_list_move_1a():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2 (divider)", key=2),
            MyText("Line 3", key=3),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 3", key=3),
            MyText("Line 2", key=2),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Line 2"},
        ],
    )


def test_list_move_1b():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3 (divider)", key=3),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 3", key=3),
            MyText("Line 2", key=2),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Line 3"},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
        ],
    )


def test_list_move_1c():
    col_1 = ft.Column(
        [
            MyText("Line 1 (divider)", key=1),
            MyText("Line 2 (divider)", key=2),
            MyText("Line 3 (divider)", key=3),
            MyText("Line 4", key=4),
            MyText("Line 5", key=5),
            MyText("Line 6 (divider)", key=6),
            MyText("Line 7 (divider)", key=7),
            MyText("Line 8", key=8),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 8", key=8),
            MyText("Line 5", key=5),
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
            MyText("Line 6", key=6),
            MyText("Line 7", key=7),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 7], "path": ["controls", 0]},
            {"op": "move", "from": ["controls", 5], "path": ["controls", 1]},
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Line 1"},
            {"op": "replace", "path": ["controls", 3, "value"], "value": "Line 2"},
            {"op": "replace", "path": ["controls", 4, "value"], "value": "Line 3"},
            {"op": "replace", "path": ["controls", 6, "value"], "value": "Line 6"},
            {"op": "replace", "path": ["controls", 7, "value"], "value": "Line 7"},
        ],
    )


def test_list_move_1d():
    col_1 = ft.Column(
        [
            MyText("Line 1 (divider)", key=1),
            MyText("Line 2 (divider)", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 4", key=4),
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 3], "path": ["controls", 0]},
            {"op": "replace", "path": ["controls", 1, "value"], "value": "Line 1"},
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Line 2"},
        ],
    )


def test_list_move_2a():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2 (divider)", key=2),
            MyText("Line 3", key=3),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 3", key=3),
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Line 2"},
        ],
    )


def test_list_move_2():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
            MyText("Line 0", key=0),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2 (updated)", key=2),
            MyText("Line 4 (updated)", key=4),
            MyText("Line 3 (updated)", key=3),
            MyText("Line 0", key=0),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 2 (updated)",
            },
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 3 (updated)",
            },
        ],
    )


def test_list_move_3():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 3", key=3),
            MyText("Line 2", key=2),
            MyText("Line 1 (updated)", key=1),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
            {
                "op": "replace",
                "path": ["controls", 2, "value"],
                "value": "Line 1 (updated)",
            },
        ],
    )


def test_list_move_4():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 3", key=3),
            MyText("Line 2 (updated)", key=2),
            MyText("Line 1", key=1),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "move", "from": ["controls", 2], "path": ["controls", 0]},
            {
                "op": "replace",
                "path": ["controls", 2, "value"],
                "value": "Line 2 (updated)",
            },
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
        ],
    )


def test_list_move_5():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
            MyText("Line 5", key=5),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1 (updated)", key=1),
            MyText("Line 2", key=2),
            MyText("Line 4 (updated)", key=4),
            MyText("Line 3", key=3),
            MyText("Line 5", key=5),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["controls", 0, "value"],
                "value": "Line 1 (updated)",
            },
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
        ],
    )


def test_list_move_6():
    col_1 = ft.Column(
        [
            MyText("Line 0", key=0),
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1 (updated)", key=1),
            MyText("Line 2 (updated)", key=2),
            MyText("Line 3 (updated)", key=3),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "remove",
                "path": ["controls", 0],
                "value": MyText(key=0, value="Line 0"),
            },
            {
                "op": "replace",
                "path": ["controls", 0, "value"],
                "value": "Line 1 (updated)",
            },
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 2 (updated)",
            },
            {
                "op": "add",
                "path": ["controls", 2],
                "value": MyText(key=3, value="Line 3 (updated)"),
            },
        ],
    )


def test_list_move_7():
    col_1 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
            MyText("Line 5", key=5),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 4 (updated)", key=4),
            MyText("Line 3", key=3),
            MyText("Line 2", key=2),
            MyText("Line 5", key=5),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {"op": "move", "from": ["controls", 3], "path": ["controls", 1]},
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
        ],
    )


def test_list_move_8_no_keys():
    col_1 = ft.Column(
        [
            MyText("Line 1"),
            MyText("Line 2"),
            MyText("Line 3"),
            MyText("Line 4"),
            MyText("Line 5"),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1"),
            MyText("Line 4 (updated)"),
            MyText("Line 3"),
            MyText("Line 2"),
            MyText("Line 5"),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "replace",
                "path": ["controls", 1, "value"],
                "value": "Line 4 (updated)",
            },
            {"op": "replace", "path": ["controls", 3, "value"], "value": "Line 2"},
        ],
    )


def test_list_move_9():
    col_1 = ft.Column(
        [
            MyText("Line 3", key=3),
            MyText("Line 4", key=4),
            MyText("Line 5", key=5),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Line 1", key=1),
            MyText("Line 2", key=2),
            MyText("Line 4 (updated)", key=4),
            MyText("Line 3 (updated)", key=3),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "add",
                "path": ["controls", 0],
                "value": MyText(key=1, value="Line 1"),
            },
            {
                "op": "add",
                "path": ["controls", 1],
                "value": MyText(key=2, value="Line 2"),
            },
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 4 (updated)",
            },
            {"op": "move", "from": ["controls", 3], "path": ["controls", 2]},
            {
                "op": "replace",
                "path": ["controls", 3, "value"],
                "value": "Line 3 (updated)",
            },
            {
                "op": "remove",
                "path": ["controls", 4],
                "value": MyText(key=5, value="Line 5"),
            },
        ],
    )


def test_list_move_10():
    col_1 = ft.Column(
        [
            MyText("Group 1", key=1),
            MyText("Group 2 (divider)", key=2),
            MyText("Group 3 (divider)", key=3),
            # MyText("Group 4 (divider)", key=4),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Group 1", key=1),
            # MyText("Group 4", key=4),
            MyText("Group 3", key=3),
            MyText("Group 2", key=2),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Group 3"},
            {"op": "move", "from": ["controls", 2], "path": ["controls", 1]},
            {"op": "replace", "path": ["controls", 2, "value"], "value": "Group 2"},
        ],
    )


def test_list_move_11():
    col_1 = ft.Column(
        [
            # MyText("Group -4", key=-4),
            # MyText("Group -3", key=-3),
            # MyText("Group -2", key=-2),
            # MyText("Group -1", key=-1),
            MyText("Group 0", key=0),
            MyText("Group 1 (divider)", key=1),
            MyText("Group 2 (divider)", key=2),
        ]
    )
    col_1._frozen = True
    col_2 = ft.Column(
        [
            MyText("Group 1", key=1),
            MyText("Group 2", key=2),
            MyText("Group 3", key=3),
            # MyText("Group 4", key=4),
        ]
    )
    patch, msg, added_controls, removed_controls = make_diff(col_2, col_1)

    assert cmp_ops(
        patch,
        [
            {
                "op": "remove",
                "path": ["controls", 0],
                "value": MyText(key=0, value="Group 0"),
            },
            {"op": "replace", "path": ["controls", 0, "value"], "value": "Group 1"},
            {"op": "replace", "path": ["controls", 1, "value"], "value": "Group 2"},
            {
                "op": "add",
                "path": ["controls", 2],
                "value": MyText(key=3, value="Group 3"),
            },
        ],
    )


def test_fields_start_with_on():
    t1 = MyText("Text 1")
    t2 = MyText(
        "Text 2",
        color_scheme=ft.ColorScheme(on_surface_variant=ft.Colors.RED),
        on_select=lambda e: print("Selected"),
    )
    t1._frozen = True

    msg, _, _, _, _ = make_msg(t2, t1, show_details=False)
    u_msg = b_unpack(msg)

    expected = [
        [0],
        [0, 0, "value", "Text 2"],
        [0, 0, "color_scheme", {"on_surface_variant": "red"}],
        [0, 0, "on_select", True],
    ]

    assert isinstance(u_msg, list)
    assert u_msg == expected


def test_fields_start_with_on_update():
    t1 = MyText(
        "Text 1",
        color_scheme=ft.ColorScheme(on_surface_variant=ft.Colors.RED),
        on_select=lambda e: print("Selected"),
    )
    t2 = MyText(
        "Text 2",
        color_scheme=ft.ColorScheme(on_surface_variant=ft.Colors.BLUE),
    )
    t1._frozen = True

    msg, _, _, _, _ = make_msg(t2, t1, show_details=False)
    u_msg = b_unpack(msg)

    expected = [
        [0, {"color_scheme": [1]}],
        [0, 0, "value", "Text 2"],
        [0, 1, "on_surface_variant", "blue"],
        [0, 0, "on_select", False],
    ]

    assert isinstance(u_msg, list)
    assert u_msg == expected
