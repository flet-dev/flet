import datetime
from dataclasses import field
from typing import Any, Optional

import msgpack

import flet as ft

# import flet as ft
# import flet.canvas as cv
from flet.controls.object_patch import ObjectPatch
from flet.messaging.protocol import configure_encode_object_for_msgpack


@ft.control("LineChartDataPoint")
class LineChartDataPoint(ft.BaseControl):
    x: ft.Number
    y: ft.Number
    selected: bool = False


@ft.control("LineChartData")
class LineChartData(ft.BaseControl):
    points: list[LineChartDataPoint] = field(default_factory=list)
    curved: bool = False
    color: ft.ColorValue = ft.Colors.CYAN
    gradient: Optional[ft.Gradient] = None


@ft.control("LineChart")
class LineChart(ft.LayoutControl):
    data_series: list[LineChartData] = field(default_factory=list)
    animation: ft.AnimationValue = field(
        default_factory=lambda: ft.Animation(
            duration=ft.Duration(milliseconds=150), curve=ft.AnimationCurve.LINEAR
        )
    )
    interactive: bool = True

    def init(self):
        super().init()
        self._internals["skip_properties"] = ["tooltip"]


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

    patch_message = patch.to_message()

    end = datetime.datetime.now()

    if show_details:
        print(f"\n=== Patch in {(end - start).total_seconds() * 1000} ms ===")
        for op in patch.patch:
            print(op)
        print("\n=== Patch message:", patch_message)

    return patch.patch, patch_message, added_controls, removed_controls


def make_msg(new: Any, old: Any = None, show_details=True):
    patch, patch_message, added_controls, removed_controls = make_diff(
        new, old, show_details
    )

    # 3 - build msgpack message
    msg = msgpack.packb(
        patch_message, default=configure_encode_object_for_msgpack(ft.BaseControl)
    )

    if show_details:
        print("\nMessage:", msg)
    else:
        print("\nMessage length:", len(msg))

    return msg, patch, patch_message, added_controls, removed_controls


def cmp_op(op, cop):
    return not (
        (cop["op"] is not None and op["op"] != cop["op"])
        or (cop["path"] is not None and op["path"] != cop["path"])
        or ("from" in cop and cop["from"] is not None and op["from"] != cop["from"])
        or ("value" in cop and cop["value"] is not None and op["value"] != cop["value"])
        or (
            "value_type" in cop
            and cop["value_type"] is not None
            and not isinstance(op["value"], cop["value_type"])
        )
    )


def cmp_ops(ops, cops):
    assert len(ops) == len(cops)
    return all(cmp_op(ops[i], cops[i]) for i in range(0, len(ops)))
