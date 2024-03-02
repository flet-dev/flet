from typing import Any, Optional

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref


class Semantics(Control):
    """
    A control that annotates the control tree with a description of the meaning of the widgets.

    Used by accessibility tools, search engines, and other semantic analysis software to determine the meaning of the application.

    -----

    Online docs: https://flet.dev/docs/controls/semantics
    """

    def __init__(
        self,
        content: Optional[Control] = None,
        label: Optional[str] = None,
        expanded: Optional[bool] = None,
        hidden: Optional[bool] = None,
        selected: Optional[bool] = None,
        button: Optional[bool] = None,
        obscured: Optional[bool] = None,
        multiline: Optional[bool] = None,
        focusable: Optional[bool] = None,
        read_only: Optional[bool] = None,
        focus: Optional[bool] = None,
        slider: Optional[bool] = None,
        tooltip: Optional[str] = None,
        toggled: Optional[bool] = None,
        max_value_length: OptionalNumber = None,
        checked: Optional[bool] = None,
        value: Optional[str] = None,
        increased_value: Optional[str] = None,
        decreased_value: Optional[str] = None,
        hint_text: Optional[str] = None,
        on_tap_hint_text: Optional[str] = None,
        on_long_press_hint_text: Optional[str] = None,
        container: Optional[bool] = None,
        live_region: Optional[bool] = None,
        textfield: Optional[bool] = None,
        link: Optional[bool] = None,
        header: Optional[bool] = None,
        image: Optional[bool] = None,
        on_tap=None,
        on_double_tap=None,
        on_increase=None,
        on_decrease=None,
        on_dismiss=None,
        on_scroll_left=None,
        on_scroll_right=None,
        on_scroll_up=None,
        on_scroll_down=None,
        on_copy=None,
        on_cut=None,
        on_paste=None,
        on_long_press=None,
        on_move_cursor_forward_by_character=None,
        on_move_cursor_backward_by_character=None,
        on_did_gain_accessibility_focus=None,
        on_did_lose_accessibility_focus=None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
        )

        self.content = content
        self.label = label
        self.expanded = expanded
        self.hidden = hidden
        self.selected = selected
        self.button = button
        self.obscured = obscured
        self.multiline = multiline
        self.focusable = focusable
        self.read_only = read_only
        self.focus = focus
        self.slider = slider
        self.tooltip = tooltip
        self.toggled = toggled
        self.max_value_length = max_value_length
        self.checked = checked
        self.value = value
        self.increased_value = increased_value
        self.decreased_value = decreased_value
        self.hint_text = hint_text
        self.on_tap_hint_text = on_tap_hint_text
        self.on_long_press_hint_text = on_long_press_hint_text
        self.container = container
        self.live_region = live_region
        self.textfield = textfield
        self.link = link
        self.header = header
        self.image = image
        self.on_tap = on_tap
        self.on_double_tap = on_double_tap
        self.on_increase = on_increase
        self.on_decrease = on_decrease
        self.on_dismiss = on_dismiss
        self.on_scroll_left = on_scroll_left
        self.on_scroll_right = on_scroll_right
        self.on_scroll_up = on_scroll_up
        self.on_scroll_down = on_scroll_down
        self.on_copy = on_copy
        self.on_cut = on_cut
        self.on_paste = on_paste
        self.on_long_press = on_long_press
        self.on_move_cursor_forward_by_character = on_move_cursor_forward_by_character
        self.on_move_cursor_backward_by_character = on_move_cursor_backward_by_character
        self.on_did_gain_accessibility_focus = on_did_gain_accessibility_focus
        self.on_did_lose_accessibility_focus = on_did_lose_accessibility_focus

    def _get_control_name(self):
        return "semantics"

    def _get_children(self):
        children = []
        if self.__content is not None:
            self.__content._set_attr_internal("n", "content")
            children.append(self.__content)
        return children

    # label
    @property
    def label(self):
        return self._get_attr("label")

    @label.setter
    def label(self, value):
        self._set_attr("label", value)

    # content
    @property
    def content(self) -> Optional[Control]:
        return self.__content

    @content.setter
    def content(self, value: Optional[Control]):
        self.__content = value

    # expanded
    @property
    def expanded(self):
        return self._get_attr("expanded")

    @expanded.setter
    def expanded(self, value: Optional[bool]):
        self._set_attr("expanded", value)

    # hidden
    @property
    def hidden(self):
        return self._get_attr("hidden")

    @hidden.setter
    def hidden(self, value: Optional[bool]):
        self._set_attr("hidden", value)

    # textfield
    @property
    def textfield(self):
        return self._get_attr("textfield")

    @textfield.setter
    def textfield(self, value: Optional[bool]):
        self._set_attr("textfield", value)

    # link
    @property
    def link(self):
        return self._get_attr("link")

    @link.setter
    def link(self, value: Optional[bool]):
        self._set_attr("link", value)

    # image
    @property
    def image(self):
        return self._get_attr("image")

    @image.setter
    def image(self, value: Optional[bool]):
        self._set_attr("image", value)

    # header
    @property
    def header(self):
        return self._get_attr("header")

    @header.setter
    def header(self, value: Optional[bool]):
        self._set_attr("header", value)

    # selected
    @property
    def selected(self):
        return self._get_attr("selected")

    @selected.setter
    def selected(self, value: Optional[bool]):
        self._set_attr("selected", value)

    # button
    @property
    def button(self):
        return self._get_attr("button")

    @button.setter
    def button(self, value: Optional[bool]):
        self._set_attr("button", value)

    # obscured
    @property
    def obscured(self):
        return self._get_attr("obscured")

    @obscured.setter
    def obscured(self, value: Optional[bool]):
        self._set_attr("obscured", value)

    # multiline
    @property
    def multiline(self):
        return self._get_attr("multiline")

    @multiline.setter
    def multiline(self, value: Optional[bool]):
        self._set_attr("multiline", value)

    # focusable
    @property
    def focusable(self):
        return self._get_attr("focusable")

    @focusable.setter
    def focusable(self, value: Optional[bool]):
        self._set_attr("focusable", value)

    # read_only
    @property
    def read_only(self):
        return self._get_attr("readOnly")

    @read_only.setter
    def read_only(self, value):
        self._set_attr("readOnly", value)

    # focused
    @property
    def focused(self):
        return self._get_attr("focus")

    @focused.setter
    def focused(self, value: Optional[bool]):
        self._set_attr("focused", value)

    # slider
    @property
    def slider(self):
        return self._get_attr("slider")

    @slider.setter
    def slider(self, value: Optional[bool]):
        self._set_attr("slider", value)

    # tooltip
    @property
    def tooltip(self):
        return self._get_attr("tooltip")

    @tooltip.setter
    def tooltip(self, value: Optional[str]):
        self._set_attr("tooltip", value)

    # toggled
    @property
    def toggled(self):
        return self._get_attr("toggled")

    @toggled.setter
    def toggled(self, value: Optional[bool]):
        self._set_attr("toggled", value)

    # max_value_length
    @property
    def max_value_length(self):
        return self._get_attr("maxValueLength")

    @max_value_length.setter
    def max_value_length(self, value: OptionalNumber):
        self._set_attr("maxValueLength", value)

    # checked
    @property
    def checked(self):
        return self._get_attr("checked")

    @checked.setter
    def checked(self, value: Optional[bool]):
        self._set_attr("checked", value)

    # value
    @property
    def value(self):
        return self._get_attr("value")

    @value.setter
    def value(self, value: Optional[str]):
        self._set_attr("value", value)

    # increased_value
    @property
    def increased_value(self):
        return self._get_attr("increasedValue")

    @increased_value.setter
    def increased_value(self, value: Optional[str]):
        self._set_attr("increasedValue", value)

    # decreased_value
    @property
    def decreased_value(self):
        return self._get_attr("decreasedValue")

    @decreased_value.setter
    def decreased_value(self, value: Optional[str]):
        self._set_attr("decreasedValue", value)

    # hint_text
    @property
    def hint_text(self):
        return self._get_attr("hintText")

    @hint_text.setter
    def hint_text(self, value: Optional[bool]):
        self._set_attr("hintText", value)

    # on_long_press_hint_text
    @property
    def on_long_press_hint_text(self):
        return self._get_attr("onLongPressHintText")

    @on_long_press_hint_text.setter
    def on_long_press_hint_text(self, value: Optional[bool]):
        self._set_attr("onLongPressHintText", value)

    # on_tap_hint_text
    @property
    def on_tap_hint_text(self):
        return self._get_attr("onTapHintText")

    @on_tap_hint_text.setter
    def on_tap_hint_text(self, value: Optional[bool]):
        self._set_attr("onTapHintText", value)

    # container
    @property
    def container(self):
        return self._get_attr("container")

    @container.setter
    def container(self, value: Optional[bool]):
        self._set_attr("container", value)

    # live_region
    @property
    def live_region(self):
        return self._get_attr("liveRegion")

    @live_region.setter
    def live_region(self, value: Optional[bool]):
        self._set_attr("liveRegion", value)

    # on_tap
    @property
    def on_tap(self):
        return self._get_event_handler("tap")

    @on_tap.setter
    def on_tap(self, handler):
        self._add_event_handler("tap", handler)
        self._set_attr("onTap", True if handler is not None else None)

    # on_double_tap
    @property
    def on_double_tap(self):
        return self._get_event_handler("double_tap")

    @on_double_tap.setter
    def on_double_tap(self, handler):
        self._add_event_handler("double_tap", handler)
        self._set_attr("onDoubleTap", True if handler is not None else None)

    # on_increase
    @property
    def on_increase(self):
        return self._get_event_handler("increase")

    @on_increase.setter
    def on_increase(self, handler):
        self._add_event_handler("increase", handler)
        self._set_attr("onIncrease", True if handler is not None else None)

    # on_decrease
    @property
    def on_decrease(self):
        return self._get_event_handler("decrease")

    @on_decrease.setter
    def on_decrease(self, handler):
        self._add_event_handler("decrease", handler)
        self._set_attr("onDecrease", True if handler is not None else None)

    # on_dismiss
    @property
    def on_dismiss(self):
        return self._get_event_handler("dismiss")

    @on_dismiss.setter
    def on_dismiss(self, handler):
        self._add_event_handler("dismiss", handler)
        self._set_attr("onDismiss", True if handler is not None else None)

    # on_scroll_left
    @property
    def on_scroll_left(self):
        return self._get_event_handler("scroll_left")

    @on_scroll_left.setter
    def on_scroll_left(self, handler):
        self._add_event_handler("scroll_left", handler)
        self._set_attr("onScrollLeft", True if handler is not None else None)

    # on_scroll_right
    @property
    def on_scroll_right(self):
        return self._get_event_handler("scroll_right")

    @on_scroll_right.setter
    def on_scroll_right(self, handler):
        self._add_event_handler("scroll_right", handler)
        self._set_attr("onScrollRight", True if handler is not None else None)

    # on_scroll_up
    @property
    def on_scroll_up(self):
        return self._get_event_handler("scroll_up")

    @on_scroll_up.setter
    def on_scroll_up(self, handler):
        self._add_event_handler("scroll_up", handler)
        self._set_attr("onScrollUp", True if handler is not None else None)

    # on_scroll_down
    @property
    def on_scroll_down(self):
        return self._get_event_handler("scroll_down")

    @on_scroll_down.setter
    def on_scroll_down(self, handler):
        self._add_event_handler("scroll_down", handler)
        self._set_attr("onScrollDown", True if handler is not None else None)

    # on_copy
    @property
    def on_copy(self):
        return self._get_event_handler("copy")

    @on_copy.setter
    def on_copy(self, handler):
        self._add_event_handler("copy", handler)
        self._set_attr("onCopy", True if handler is not None else None)

    # on_cut
    @property
    def on_cut(self):
        return self._get_event_handler("cut")

    @on_cut.setter
    def on_cut(self, handler):
        self._add_event_handler("cut", handler)
        self._set_attr("onCut", True if handler is not None else None)

    # on_paste
    @property
    def on_paste(self):
        return self._get_event_handler("paste")

    @on_paste.setter
    def on_paste(self, handler):
        self._add_event_handler("paste", handler)
        self._set_attr("onPaste", True if handler is not None else None)

    # on_long_press
    @property
    def on_long_press(self):
        return self._get_event_handler("long_press")

    @on_long_press.setter
    def on_long_press(self, handler):
        self._add_event_handler("long_press", handler)
        self._set_attr("onLongPress", True if handler is not None else None)

    # on_move_cursor_forward_by_character
    @property
    def on_move_cursor_forward_by_character(self):
        return self._get_event_handler("move_cursor_forward_by_character")

    @on_move_cursor_forward_by_character.setter
    def on_move_cursor_forward_by_character(self, handler):
        self._add_event_handler("move_cursor_forward_by_character", handler)
        self._set_attr(
            "onMoveCursorForwardByCharacter", True if handler is not None else None
        )

    # on_move_cursor_backward_by_character
    @property
    def on_move_cursor_backward_by_character(self):
        return self._get_event_handler("move_cursor_backward_by_character")

    @on_move_cursor_backward_by_character.setter
    def on_move_cursor_backward_by_character(self, handler):
        self._add_event_handler("move_cursor_backward_by_character", handler)
        self._set_attr(
            "onMoveCursorBackwardByCharacter", True if handler is not None else None
        )

    # on_did_gain_accessibility_focus
    @property
    def on_did_gain_accessibility_focus(self):
        return self._get_event_handler("did_gain_accessibility_focus")

    @on_did_gain_accessibility_focus.setter
    def on_did_gain_accessibility_focus(self, handler):
        self._add_event_handler("did_gain_accessibility_focus", handler)
        self._set_attr(
            "onDidGainAccessibilityFocus", True if handler is not None else None
        )

    # on_did_lose_accessibility_focus
    @property
    def on_did_lose_accessibility_focus(self):
        return self._get_event_handler("did_lose_accessibility_focus")

    @on_did_lose_accessibility_focus.setter
    def on_did_lose_accessibility_focus(self, handler):
        self._add_event_handler("did_lose_accessibility_focus", handler)
        self._set_attr(
            "onDidLoseAccessibilityFocus", True if handler is not None else None
        )
