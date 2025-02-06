import copy
import datetime
import weakref
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum
from typing import Any, List, Optional

import msgpack
from flet.core.diff_patch import ObjectPatch

# - create weakref control index (using hashes) for partial tree updates and event routing
# - controls should have weak ref to a parent control or page
# - override __setattr__ to effectively track changes
# - added dataclasses should not pass "None" fields


def encode_dataclasses(obj):
    if is_dataclass(obj):
        r = {}
        for field in fields(obj):
            v = getattr(obj, field.name)
            if isinstance(v, list):
                v = v[:]
            elif isinstance(v, dict):
                v = v.copy()
            setattr(obj, f"_prev_{field.name}", v)
            r[field.name] = v
        return r
    elif isinstance(obj, Enum):
        return obj.value
    return obj


controls_index = weakref.WeakValueDictionary()


def update_ui(new: Any, old: Any = None, show_details=True):
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

    print("controls_index:", len(controls_index))
    print("\nTotal:", (end - start).total_seconds() * 1000)


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


@dataclass
class Page(Control):
    url: str
    controls: List[Any] = field(default_factory=list)


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
    id: Optional[str] = None
    text: Optional[str] = None
    styles: Optional[dict[str, ButtonStyle]] = None


@dataclass
class Span(Control):
    id: Optional[str] = None
    text: Optional[str] = None
    cls: Optional[str] = None
    controls: List[Any] = field(default_factory=list)
    head_controls: List[Any] = field(default_factory=list)


@dataclass
class Div(Control):
    id: Optional[str] = None
    cls: Optional[str] = None
    some_value: Any = None
    controls: List[Any] = field(default_factory=list)


if __name__ != "__main__":
    exit()

# initial update
# ==================
ui = Page(url="http://aaa.com", controls=[Div(cls="div_1", some_value="Text")])

update_ui(ui, {})
print("ui PARENT:", ui.parent)
print("ui.controls[0] PARENT:", ui.controls[0].parent)

# update sub-tree
ui.controls[0].some_value = "Another text"
ui.controls[0].controls = [
    Button(
        text="Button 😬",
        styles={
            "style_1": ButtonStyle(True, True, color=Color.RED),
            "style_2": ButtonStyle(False, True),
        },
    )
]
update_ui(ui.controls[0])

# exit()

# check _prev
print("\nPrev:", ui._prev_url)

# 2nd update
# ==================
ui.url = "http://bbb.com"
ui.controls[0].some_value = "Some value"
# del ui.controls[0]
ui.controls.append(Span(id="span_1"))
ui.controls.append(Span(id="span_2"))
ui.controls.append(Span(id="span_3"))

btn = ui.controls[0].controls[0]
btn.text = "Supper button"
btn.styles["style_1"].bold = False
del btn.styles["style_2"]
btn.styles["style_A"] = ButtonStyle(True, True, color=Color.GREEN)
update_ui(ui)

# exit()

# 3rd update
# ==================
ctrl = ui.controls.pop()
ui.controls[0].controls.append(ctrl)
update_ui(ui)

# exit()

# 4th update
# ==================
for i in range(1, 1000):
    ui.controls.append(
        Div(cls=f"div_{i}", controls=[Span(id=f"span_{i}", text=f"Span {i}")])
    )

update_ui(ui, show_details=False)

# exit()

# 5th update
# ==================
ui.controls[3].controls.insert(0, Button(text="Click me"))
ui.controls[4].controls[0].text = "Hello world"
ui.controls[20].controls.pop()
ui.controls.pop()
for i in range(100, 300):
    ui.controls[i].controls[0].text = f"Hello world {i}"

update_ui(ui, show_details=False)
