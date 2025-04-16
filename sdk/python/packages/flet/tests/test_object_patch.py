import datetime
import weakref
from dataclasses import field
from typing import Any, List, Optional

import msgpack
from flet.controls.base_control import BaseControl, control
from flet.controls.buttons import ButtonStyle
from flet.controls.colors import Colors
from flet.controls.control import Control

# import flet as ft
# import flet.canvas as cv
from flet.controls.core.container import Container
from flet.controls.core.gesture_detector import DragUpdateEvent, GestureDetector
from flet.controls.core.text import Text
from flet.controls.material.button import Button
from flet.controls.material.elevated_button import ElevatedButton
from flet.controls.object_patch import ObjectPatch
from flet.controls.page import Page
from flet.controls.painting import Paint, PaintLinearGradient
from flet.controls.ref import Ref
from flet.controls.service import Service
from flet.messaging.connection import Connection
from flet.messaging.protocol import configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub

controls_index = weakref.WeakValueDictionary()


def b_pack(data):
    return msgpack.packb(data, default=configure_encode_object_for_msgpack(BaseControl))


def b_unpack(packed_data):
    return msgpack.unpackb(packed_data)


def update_page(new: Any, old: Any = None, show_details=True):
    if old is None:
        old = new
    start = datetime.datetime.now()

    # 1 -calculate diff
    patch, added_controls, removed_controls = ObjectPatch.from_diff(
        old, new, in_place=True, controls_index=controls_index, control_cls=BaseControl
    )

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_graph()
    # print(graph_patch)

    # 3 - build msgpack message
    msg = msgpack.packb(
        graph_patch, default=configure_encode_object_for_msgpack(BaseControl)
    )

    end = datetime.datetime.now()

    if show_details:
        # print("\nPatch:", patch)
        print("\nGraph patch:", graph_patch)
        print("\nMessage:", msg)
    else:
        print("\nMessage length:", len(msg))

    print("\ncontrols_index:", len(controls_index))
    print("\nTotal:", (end - start).total_seconds() * 1000)

    return msg


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
    prop_2: List[int] = field(default_factory=list)


@control("Span")
class Span(Control):
    text: Optional[str] = None
    cls: Optional[str] = None
    controls: List[Any] = field(default_factory=list)
    head_controls: List[Any] = field(default_factory=list)


@control("Div")
class Div(Control):
    cls: Optional[str] = None
    some_value: Any = None
    controls: List[Any] = field(default_factory=list)


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
    page.on_close = lambda e: print("on close")
    page.services.append(MyService(prop_1="Hello", prop_2=[1, 2, 3]))

    # page and window have hard-coded IDs
    assert page._i == 1
    assert page.window and page.window._i == 2

    msg = update_page(page, {}, show_details=True)
    u_msg = b_unpack(msg)

    assert page.parent is None
    assert page.controls[0].parent == page.views[0]
    assert page.clipboard
    assert page.clipboard.parent
    assert page.clipboard.page

    print(u_msg)

    assert isinstance(u_msg, dict)
    assert "" in u_msg
    assert u_msg[""]["_i"] > 0
    assert u_msg[""]["on_close"]
    assert len(u_msg[""]["views"]) > 0
    assert "on_connect" not in u_msg[""]

    # update sub-tree
    page.on_close = None
    page.controls[0].some_value = "Another text"
    page.controls[0].controls = [
        SuperElevatedButton(
            "Button 😬",
            style=ButtonStyle(color=Colors.RED),
            on_click=lambda e: print(e),
            opacity=1,
            ref=None,
        )
    ]
    del page.fonts["font2"]
    assert page.controls[0].controls[0].page is None

    page.services[0].prop_2 = [2, 6]

    update_page(page, show_details=True)
    assert hasattr(page.views[0], "__changes")


def test_changes_tracking():
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    page = Page(sess=Session(conn))
    page.controls.append(
        btn := Button(Text("Click me!"), on_click=lambda e: print("clicked!"))
    )

    # initial update
    msg = update_page(page, {}, show_details=True)

    # second update
    btn.content = Text("A new button content")
    btn.width = 300
    btn.height = 100

    # t1 = Text("AAA")
    # t2 = Text("BBB")
    page.controls.append(Text("Line 2"))

    msg = update_page(page, show_details=True)


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
    msg = update_page(page, {}, show_details=True)

    # second update
    for i in range(1, 1000):
        cp.shapes.append(
            cv.Line(i + 1, i + 100, i + 10, i + 20, paint=Paint(stroke_width=3))
        )

    msg = update_page(cp, show_details=False)

    cp.shapes[100].x1 = 12

    # third update
    for i in range(1, 20):
        cp.shapes.append(
            cv.Line(i + 1, i + 100, i + 10, i + 20, paint=Paint(stroke_width=3))
        )

    msg = update_page(cp, show_details=True)


# exit()


# # initial update
# # ==================
# page_ref = Ref[Page]()

# page = Page(
#     url="http://aaa.com",
#     controls=[Div(cls="div_1", some_value="Text")],
#     prop_1="aaa",
#     data=100000,
#     ref=page_ref,
# )

# print("Page ref:", page_ref.current)

# update_page(page, {})
# print("page PARENT:", page.parent)
# print("page.controls[0] PARENT:", page.controls[0].parent)

# # update sub-tree
# page.controls[0].some_value = "Another text"
# page.controls[0].controls = [
#     SuperElevatedButton(
#         text="Button 😬",
#         style=ButtonStyle(color=Colors.RED),
#         on_click=lambda e: print(e),
#         opacity=1,
#         ref=None,
#     )
# ]
# print("PAGE:", page.controls[0].controls[0].page)
# update_page(page.controls[0])

# # exit()

# # check _prev
# print("\nPrev:", page._prev_prop_1)

# # 2nd update
# # ==================
# # page.url = "http://bbb.com"
# page.prop_1 = None
# page.controls[0].some_value = "Some value"
# # del page.controls[0]
# page.controls.append(Span(cls="span_1"))
# page.controls.append(Span(cls="span_2"))
# page.controls.append(Span(cls="span_3"))

# btn = page.controls[0].controls[0]
# print("PAGE:", btn.page)
# btn.text = "Supper button"
# btn.style = ButtonStyle(color=Colors.GREEN)
# btn.on_click = None
# update_page(page)

# # exit()

# # 3rd update
# # ==================
# ctrl = page.controls.pop()
# page.controls[0].controls.append(ctrl)
# update_page(page)

# # exit()

# # 4th update
# # ==================
# for i in range(1, 1000):
#     page.controls.append(
#         Div(cls=f"div_{i}", controls=[Span(cls=f"span_{i}", text=f"Span {i}")])
#     )

# update_page(page, show_details=False)

# # exit()

# # 5th update
# # ==================
# page.controls[3].controls.insert(0, ElevatedButton(text="Click me"))
# page.controls[4].controls[0].text = "Hello world"
# page.controls[20].controls.pop()
# page.controls.pop()
# for i in range(100, 300):
#     page.controls[i].controls[0].text = f"Hello world {i}"

# update_page(page, show_details=False)
