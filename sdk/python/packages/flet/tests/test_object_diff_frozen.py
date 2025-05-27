import datetime
from dataclasses import dataclass
from typing import Any

import flet as ft
import msgpack
import pytest

# import flet as ft
# import flet.canvas as cv
from flet.controls.object_patch import ObjectPatch
from flet.messaging.protocol import configure_encode_object_for_msgpack


def b_pack(data):
    return msgpack.packb(
        data, default=configure_encode_object_for_msgpack(ft.BaseControl)
    )


def b_unpack(packed_data):
    return msgpack.unpackb(packed_data)


def make_diff(new: Any, old: Any = None, show_details=True):
    if old is None:
        old = new
    start = datetime.datetime.now()

    # 1 -calculate diff
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old, new, control_cls=ft.BaseControl
    )

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_graph()
    # print(graph_patch)

    end = datetime.datetime.now()

    if show_details:
        print(f"\nPatch in {(end - start).total_seconds() * 1000} ms: {graph_patch}")

    return graph_patch, added_controls, removed_controls


def make_msg(new: Any, old: Any = None, show_details=True):
    graph_patch, added_controls, removed_controls = make_diff(new, old, show_details)

    # 3 - build msgpack message
    msg = msgpack.packb(
        graph_patch, default=configure_encode_object_for_msgpack(ft.BaseControl)
    )

    if show_details:
        print("\nMessage:", msg)
    else:
        print("\nMessage length:", len(msg))

    return msg, added_controls, removed_controls


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

    dp1 = ft.LineChartDataPoint(x=10, y=20)
    dp2 = ft.LineChartDataPoint(x=10, y=20)
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
    patch, _, _ = make_diff(b2, {})
    assert not hasattr(b2, "__prev_classes")
    assert isinstance(patch[""], ft.Button)

    # 2nd iteration
    patch, _, _ = make_diff(b2, b1)
    assert len(patch) == 3
    assert patch["content"] == "Click me"
    assert isinstance(patch["style"], ft.ButtonStyle)

    # 3rd iteration
    b3 = ft.Button(content=ft.Text("Text_1"), style=None, scale=ft.Scale(0.1))
    b3._frozen = True
    patch, _, _ = make_diff(b3, b2)
    assert len(patch) == 3
    assert patch["scale"]["scale"] == 0.1
    assert isinstance(patch["content"], ft.Text)
    assert patch["style"] is None


def test_lists_with_key_diff():
    c1 = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(list_key=0, x=0, y=1),
                    ft.LineChartDataPoint(list_key=1, x=1, y=2),
                    ft.LineChartDataPoint(list_key=2, x=2, y=3),
                ]
            )
        ]
    )
    c2 = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(list_key=1, x=1, y=2),
                    ft.LineChartDataPoint(list_key=2, x=2, y=2),
                    ft.LineChartDataPoint(list_key=3, x=3, y=5),
                ]
            )
        ]
    )
    c1._frozen = True
    patch, _, _ = make_diff(c2, c1)
    assert c2._frozen
    assert c2.data_series[0]._frozen
    assert patch["data_series"][0]["data_points"]["$d"] == [0]
    assert isinstance(
        patch["data_series"][0]["data_points"][2]["$a"], ft.LineChartDataPoint
    )


def test_lists_with_no_key_diff():
    c1 = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(x=0, y=1),
                    ft.LineChartDataPoint(x=1, y=2),
                    ft.LineChartDataPoint(x=2, y=3),
                ]
            )
        ]
    )
    c2 = ft.LineChart(
        data_series=[
            ft.LineChartData(
                data_points=[
                    ft.LineChartDataPoint(x=1, y=2),
                    ft.LineChartDataPoint(x=2, y=2),
                    ft.LineChartDataPoint(x=3, y=5),
                ]
            )
        ]
    )
    c1._frozen = True
    patch, _, _ = make_diff(c2, c1)
    assert c2._frozen
    assert c2.data_series[0]._frozen
    assert patch["data_series"][0]["data_points"][0]["x"] == 1
    assert patch["data_series"][0]["data_points"][0]["y"] == 2
    assert patch["data_series"][0]["data_points"][1]["x"] == 2
    assert patch["data_series"][0]["data_points"][2]["x"] == 3
    assert patch["data_series"][0]["data_points"][2]["y"] == 5


def test_simple_lists_diff():
    c1 = ft.LineChart(data_series=[ft.LineChartData(data_points=[1, 2, 3])])
    c2 = ft.LineChart(data_series=[ft.LineChartData(data_points=[2, 3, 4])])
    c1._frozen = True
    patch, _, _ = make_diff(c2, c1)
    assert patch["data_series"][0]["data_points"]["$d"] == [0]
    assert patch["data_series"][0]["data_points"][2]["$a"] == 4


def test_simple_lists_diff_2():
    c1 = ft.LineChart(data_series=[ft.LineChartData(data_points=[1, 2, 3, 4])])
    c2 = ft.LineChart(data_series=[ft.LineChartData(data_points=[1, 3, 4])])
    c1._frozen = True
    patch, _, _ = make_diff(c2, c1)
    # assert patch["data_series"][0]["data_points"]["$d"] == [0]
    # assert patch["data_series"][0]["data_points"][2]["$a"] == 4


def test_similar_lists_diff():
    c1 = ft.LineChart(
        data_series=[ft.LineChartData(data_points=[ft.Scale(0), ft.Scale(1)])]
    )
    c2 = ft.LineChart(
        data_series=[ft.LineChartData(data_points=[ft.Scale(1), ft.Scale(2)])]
    )
    c1._frozen = True
    patch, _, _ = make_diff(c2, c1)
    assert patch["data_series"][0]["data_points"][0]["scale"] == 1
    assert patch["data_series"][0]["data_points"][1]["scale"] == 2


def test_both_frozen_hosted_by_in_place():
    def chart(data):
        r = ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=[
                        ft.LineChartDataPoint(list_key=dp[0], x=dp[0], y=dp[1])
                        for dp in ds
                    ]
                )
                for ds in data
            ]
        )
        r._frozen = True
        return r

    c = ft.Container(content=chart([[(0, 1), (1, 1), (2, 2)], [(10, 20), (20, 30)]]))
    assert not hasattr(c, "_frozen")
    patch, added_controls, removed_controls = make_msg(c, {})
    assert len(added_controls) == 9
    assert len(removed_controls) == 0
    assert hasattr(c, "__changes")
    assert not hasattr(c, "_frozen")

    c.alignment = ft.Alignment.bottom_center()
    c.bgcolor = ft.Colors.AMBER
    ch = chart([[(1, 1), (2, 2), (3, 3)]])
    c.content = ch
    patch, added_controls, removed_controls = make_msg(c, c)
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    # for rc in removed_controls:
    #     print("\nREMOVED CONTROL:", rc)
    assert len(added_controls) == 0
    assert len(removed_controls) == 4
    assert hasattr(ch, "_frozen")
    with pytest.raises(Exception, match="Controls inside data view cannot be updated."):
        ch.width = 100


def test_data_view_with_cache():
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

    @ft.data_view
    def user_details(user: User):
        return ft.Card(
            ft.Column(
                [
                    ft.Text(f"Name: {user.name}"),
                    ft.Text(f"Age: {user.age}"),
                    ft.Checkbox(label="Verified", value=user.verified),
                ]
            ),
            list_key=user.id,
        )

    @ft.data_view
    def users_list(users):
        return ft.Column([user_details(user) for user in users])

    page = ft.Row([users_list(users)])

    patch, added_controls, removed_controls = make_msg(page, {})
    assert len(added_controls) == 17
    assert len(removed_controls) == 0

    # add new user
    users.append(User(4, name="Someone Else", age=99, verified=False))
    page.controls[0] = users_list(users)
    patch, added_controls, removed_controls = make_msg(page, page)
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    assert len(added_controls) == 5
    assert len(removed_controls) == 0

    # remove user
    del users[1]
    page.controls[0] = users_list(users)
    patch, added_controls, removed_controls = make_msg(page, page)
    assert len(added_controls) == 0
    assert len(removed_controls) == 5
    # for ac in added_controls:
    #     print("\nADDED CONTROL:", ac)
    # for rc in removed_controls:
    #     print("\nREMOVED CONTROL:", rc)
