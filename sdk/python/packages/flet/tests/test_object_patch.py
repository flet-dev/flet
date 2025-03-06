import copy
import datetime
import weakref
from dataclasses import InitVar, dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional

import msgpack
from flet.core.adaptive_control import AdaptiveControl
from flet.core.buttons import ButtonStyle
from flet.core.colors import Colors
from flet.core.connection import Connection
from flet.core.control import Control, control, event
from flet.core.elevated_button import ElevatedButton
from flet.core.event import Event
from flet.core.object_patch import ObjectPatch
from flet.core.page import BrowserContextMenu, Page
from flet.core.protocol import encode_object_for_msgpack
from flet.core.ref import Ref

controls_index = weakref.WeakValueDictionary()


def update_page(new: Any, old: Any = None, show_details=True):
    if old is None:
        old = new
    start = datetime.datetime.now()

    # 1 -calculate diff
    patch = ObjectPatch.from_diff(
        old, new, in_place=True, controls_index=controls_index, control_cls=Control
    )

    # 2 - convert patch to hierarchy
    graph_patch = patch.to_graph()
    # print(graph_patch)

    # 3 - build msgpack message
    msg = msgpack.packb(graph_patch, default=encode_object_for_msgpack)

    end = datetime.datetime.now()

    if show_details:
        print("\nPatch:", graph_patch)
        print("\nMessage:", msg)
    else:
        print("\nMessage length:", len(msg))

    print("\ncontrols_index:", len(controls_index))
    print("\nTotal:", (end - start).total_seconds() * 1000)


@control
class SuperElevatedButton(ElevatedButton):
    prop_2: Optional[str] = None

    def build(self):
        print("SuperElevatedButton.page:", self.page)


@control("MyButton")
class MyButton(ElevatedButton):
    prop_1: Optional[str] = None


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
    assert btn.type == "ElevatedButton"


def test_inherited_control_has_the_same_type():
    btn = SuperElevatedButton(prop_2="2")
    assert btn.type == "ElevatedButton"


def test_inherited_control_with_overridden_type():
    btn = MyButton(prop_1="1")
    assert btn.type == "MyButton"


def test_control_ref():
    page_ref = Ref[Page]()

    page = Page(conn=Connection(), ref=page_ref)

    assert page_ref.current == page


def test_simple_page():
    page = Page(conn=Connection())
    page.controls = [Div(cls="div_1", some_value="Text")]
    page.data = 100000
    page.bgcolor = Colors.GREEN

    # assert page._url == url

    update_page(page, {})

    assert page.parent is None
    assert page.controls[0].parent == page.views[0]

    # update sub-tree
    page.controls[0].some_value = "Another text"
    page.controls[0].controls = [
        SuperElevatedButton(
            text="Button 😬",
            style=ButtonStyle(color=Colors.RED),
            on_click=lambda e: print(e),
            opacity=1,
            ref=None,
        )
    ]
    assert page.controls[0].controls[0].page is None

    update_page(page.controls[0])

    print(page.controls[0].controls[0].page)

    assert page.views[0]._prev_bgcolor == "green"


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
