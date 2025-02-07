import copy
import datetime
import weakref
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, List, Optional

import msgpack
from flet.core.object_patch import ObjectPatch


def encode_dataclasses(obj):
    if is_dataclass(obj):
        r = {}
        for field in fields(obj):
            v = getattr(obj, field.name)
            if isinstance(v, list):
                v = v[:]
            elif isinstance(v, dict):
                v = v.copy()
            elif field.name.startswith("on_"):
                v = v is not None
            setattr(obj, f"_prev_{field.name}", v)
            if v is not None:
                r[field.name] = v
        return r
    elif isinstance(obj, Enum):
        return obj.value
    return obj


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
    msg = msgpack.packb(graph_patch, default=encode_dataclasses)

    end = datetime.datetime.now()

    if show_details:
        print("\nPatch:", graph_patch)
        print("\nMessage:", msg)
    else:
        print("\nMessage length:", len(msg))

    print("\ncontrols_index:", len(controls_index))
    print("\nTotal:", (end - start).total_seconds() * 1000)


@dataclass
class Event:
    target: str
    name: str
    data: object


@dataclass
class Control:
    id: int = field(init=False)

    def __post_init__(self):
        self.__class__.__hash__ = Control.__hash__
        self.id = self.__hash__()

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def parent(self) -> Optional["Control"]:
        parent_ref = getattr(self, "_parent", None)
        return parent_ref() if parent_ref else None

    @property
    def page(self) -> Optional["Page"]:
        parent = self
        while parent:
            if isinstance(parent, Page):
                return parent
            parent = parent.parent
        return None


@dataclass
class Page(Control):
    url: str
    controls: List[Any] = field(default_factory=list)
    prop_1: Optional[str] = None
    prop_2: Optional[str] = None
    prop_3: Optional[int] = None


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


@dataclass
class ButtonStyle:
    bold: bool = False
    italic: bool = False
    color: Optional[Color] = None


@dataclass
class Button(Control):
    text: Optional[str] = None
    styles: Optional[dict[str, ButtonStyle]] = None
    on_click: Any = None


@dataclass
class Span(Control):
    text: Optional[str] = None
    cls: Optional[str] = None
    controls: List[Any] = field(default_factory=list)
    head_controls: List[Any] = field(default_factory=list)


@dataclass
class Div(Control):
    cls: Optional[str] = None
    some_value: Any = None
    controls: List[Any] = field(default_factory=list)


if __name__ != "__main__":
    exit()

# test event assignment
event_handler_type = Event

ed = {"target": "ctrl_1", "name": "click", "data": None}

e = event_handler_type(**ed)
assert e.name == "click"

# initial update
# ==================
page = Page(
    url="http://aaa.com", controls=[Div(cls="div_1", some_value="Text")], prop_1="aaa"
)

update_page(page, {})
print("page PARENT:", page.parent)
print("page.controls[0] PARENT:", page.controls[0].parent)

# update sub-tree
page.controls[0].some_value = "Another text"
page.controls[0].controls = [
    Button(
        text="Button 😬",
        styles={
            "style_1": ButtonStyle(True, True, color=Color.RED),
            "style_2": ButtonStyle(False, True),
        },
    )
]
print("PAGE:", page.controls[0].controls[0].page)
update_page(page.controls[0])

# exit()

# check _prev
print("\nPrev:", page._prev_url)

# 2nd update
# ==================
page.url = "http://bbb.com"
page.prop_1 = None
page.controls[0].some_value = "Some value"
# del page.controls[0]
page.controls.append(Span(cls="span_1"))
page.controls.append(Span(cls="span_2"))
page.controls.append(Span(cls="span_3"))

btn = page.controls[0].controls[0]
print("PAGE:", btn.page)
btn.text = "Supper button"
btn.styles["style_1"].bold = False
del btn.styles["style_2"]
btn.styles["style_A"] = ButtonStyle(True, True, color=Color.GREEN)
update_page(page)

# exit()

# 3rd update
# ==================
ctrl = page.controls.pop()
page.controls[0].controls.append(ctrl)
update_page(page)

# exit()

# 4th update
# ==================
for i in range(1, 1000):
    page.controls.append(
        Div(cls=f"div_{i}", controls=[Span(cls=f"span_{i}", text=f"Span {i}")])
    )

update_page(page, show_details=False)

# exit()

# 5th update
# ==================
page.controls[3].controls.insert(0, Button(text="Click me"))
page.controls[4].controls[0].text = "Hello world"
page.controls[20].controls.pop()
page.controls.pop()
for i in range(100, 300):
    page.controls[i].controls[0].text = f"Hello world {i}"

update_page(page, show_details=False)
