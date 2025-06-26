import logging
from dataclasses import dataclass, field
from typing import (
    Optional,
    Union,
)

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.animation import AnimationCurve
from flet.controls.base_control import BaseControl, control
from flet.controls.box import BoxDecoration
from flet.controls.control import Control
from flet.controls.control_event import (
    Event,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.core.view import View
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import OptionalDurationValue
from flet.controls.keys import ScrollKey
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.padding import OptionalPaddingValue, Padding
from flet.controls.scrollable_control import OnScrollEvent
from flet.controls.theme import Theme
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    LocaleConfiguration,
    MainAxisAlignment,
    OptionalColorValue,
    OptionalNumber,
    ScrollMode,
    ThemeMode,
)
from flet.utils import deprecated

logger = logging.getLogger("flet")


@dataclass
class PageMediaData:
    padding: Padding
    view_padding: Padding
    view_insets: Padding


@dataclass
class PageResizeEvent(Event["PageView"]):
    width: float
    height: float


@control("PageView", isolated=True, kw_only=True)
class PageView(AdaptiveControl):
    """
    TBD
    """

    views: list[View] = field(default_factory=lambda: [View()])
    _overlay: "Overlay" = field(default_factory=lambda: Overlay())
    _dialogs: "Dialogs" = field(default_factory=lambda: Dialogs())

    theme_mode: Optional[ThemeMode] = ThemeMode.SYSTEM
    """
    The page's theme mode.

    Value is of type [`ThemeMode`](https://flet.dev/docs/reference/types/thememode) and 
    defaults to `ThemeMode.SYSTEM`.
    """
    theme: Optional[Theme] = None
    """
    Customizes the theme of the application when in light theme mode. Currently, a 
    theme can only be automatically generated from a "seed" color. For example, to 
    generate light theme from a green color.

    Value is an instance of the `Theme()` class - more information in the [theming](https://flet.dev/docs/cookbook/theming) 
    guide.
    """
    dark_theme: Optional[Theme] = None
    """
    Customizes the theme of the application when in dark theme mode.

    Value is an instance of the `Theme()` class - more information in the 
    [theming](https://flet.dev/docs/cookbook/theming) guide.
    """
    locale_configuration: Optional[LocaleConfiguration] = None
    show_semantics_debugger: Optional[bool] = None
    """
    `True` turns on an overlay that shows the accessibility information reported by the 
    framework.
    """
    width: OptionalNumber = None
    height: OptionalNumber = None
    title: Optional[str] = None
    media: Optional[PageMediaData] = None
    scroll_event_interval: OptionalNumber = None
    on_resized: OptionalEventHandler["PageResizeEvent"] = None
    """
    Fires when a user resizes a browser or native OS window containing Flet app, for 
    example:

    ```python
    def page_resized(e):
        print("New page size:", page.window.width, page.window_height)

    page.on_resized = page_resized
    ```

    Event handler argument is of type [`WindowResizeEvent`](https://flet.dev/docs/reference/types/windowresizeevent).
    """
    on_media_change: OptionalControlEventHandler["PageView"] = None
    """
    Fires when `page.media` has changed. 

    Event handler argument is of type 
    [`PageMediaData`](https://flet.dev/docs/docs/reference/types/pagemediadata).
    """
    on_scroll: OptionalEventHandler["OnScrollEvent"] = None
    """
    Fires when page's scroll position is changed by a user.

    Event handler argument is of type 
    [`OnScrollEvent`](https://flet.dev/docs/reference/types/onscrollevent).
    """

    def __default_view(self) -> View:
        assert len(self.views) > 0, "views list is empty."
        return self.views[0]

    def update(self, *controls) -> None:
        if len(controls) == 0:
            self.page.update(self)
        else:
            self.page.update(*controls)

    def add(self, *controls: Control) -> None:
        """
        Adds controls to the page.

        ```python
        page.add(ft.Text("Hello!"), ft.FilledButton("Button"))
        ```
        """
        self.controls.extend(controls)
        self.update()

    def insert(self, at: int, *controls: Control) -> None:
        """
        Inserts controls at specific index of `page.controls` list.
        """
        n = at
        for c in controls:
            self.controls.insert(n, c)
            n += 1
        self.update()

    def remove(self, *controls: Control) -> None:
        """
        Removes specific controls from `page.controls` list.
        """
        for c in controls:
            self.controls.remove(c)
        self.update()

    def remove_at(self, index: int) -> None:
        """
        Remove controls from `page.controls` list at specific index.
        """
        self.controls.pop(index)
        self.update()

    def clean(self) -> None:
        self.controls.clear()
        self.update()

    def scroll_to(
        self,
        offset: Optional[float] = None,
        delta: Optional[float] = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: OptionalDurationValue = None,
        curve: Optional[AnimationCurve] = None,
    ) -> None:
        """
        Moves scroll position to either absolute `offset`, relative `delta` or jump to
        the control with specified `scroll_key`.

        See [`Column.scroll_to()`](https://flet.dev/docs/controls/column#scroll_tooffset-delta-key-duration-curve)
        for method details and examples.
        """
        self.__default_view().scroll_to(
            offset=offset,
            delta=delta,
            scroll_key=scroll_key,
            duration=duration,
            curve=curve,
        )

    @deprecated(
        reason="Use Page.show_dialog() instead",
        version="0.70.0",
        delete_version="0.73.0",
        show_parentheses=True,
    )
    def open(self, control: DialogControl) -> None:
        self.show_dialog(control)

    def show_dialog(self, dialog: DialogControl) -> None:
        """
        TBD
        """
        if dialog in self._dialogs.controls:
            raise Exception("Dialog is already opened")

        original_on_dismiss = dialog.on_dismiss

        def wrapped_on_dismiss(*args, **kwargs):
            if dialog in self._dialogs.controls:
                self._dialogs.controls.remove(dialog)
                self._dialogs.update()
            if (
                original_on_dismiss
                and not hasattr(dialog, "_force_close")
                and args[
                    0
                ].data  # e.data == False for TimePicker and DatePicker if they were
                # dismissed without changing the value
            ):
                original_on_dismiss(*args, **kwargs)
            dialog.on_dismiss = original_on_dismiss
            if hasattr(dialog, "_force_close"):
                del dialog._force_close

        dialog.open = True
        dialog.on_dismiss = wrapped_on_dismiss

        self._dialogs.controls.append(dialog)
        self._dialogs.update()

    @deprecated(
        reason="Use Page.pop_dialog() instead",
        version="0.70.0",
        delete_version="0.73.0",
        show_parentheses=True,
    )
    def close(self, control: DialogControl) -> None:
        self.pop_dialog()

    def pop_dialog(self) -> Optional[DialogControl]:
        # get the top most opened dialog
        dialog = next(
            (dlg for dlg in reversed(self._dialogs.controls) if dlg.open), None
        )
        if not dialog:
            return None
        dialog.open = False
        dialog._force_close = True
        dialog.update()
        return dialog

    # overlay
    @property
    def overlay(self) -> list[BaseControl]:
        return self._overlay.controls

    # controls
    @property
    def controls(self) -> list[BaseControl]:
        return self.__default_view().controls

    @controls.setter
    def controls(self, value: list[BaseControl]):
        self.__default_view().controls = value

    # appbar
    @property
    def appbar(self) -> Union[AppBar, CupertinoAppBar, None]:
        return self.__default_view().appbar

    @appbar.setter
    def appbar(self, value: Union[AppBar, CupertinoAppBar, None]):
        self.__default_view().appbar = value

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__default_view().bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__default_view().bottom_appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[Union[NavigationBar, CupertinoNavigationBar]]:
        return self.__default_view().navigation_bar

    @navigation_bar.setter
    def navigation_bar(
        self,
        value: Optional[Union[NavigationBar, CupertinoNavigationBar]],
    ):
        self.__default_view().navigation_bar = value

    # drawer
    @property
    def drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view().drawer

    @drawer.setter
    def drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view().drawer = value

    # end_drawer
    @property
    def end_drawer(self) -> Optional[NavigationDrawer]:
        return self.__default_view().end_drawer

    @end_drawer.setter
    def end_drawer(self, value: Optional[NavigationDrawer]):
        self.__default_view().end_drawer = value

    # decoration
    @property
    def decoration(self) -> Optional[BoxDecoration]:
        return self.__default_view().decoration

    @decoration.setter
    def decoration(self, value: Optional[BoxDecoration]):
        self.__default_view().decoration = value

    # foreground_decoration
    @property
    def foreground_decoration(self) -> Optional[BoxDecoration]:
        return self.__default_view().foreground_decoration

    @foreground_decoration.setter
    def foreground_decoration(self, value: Optional[BoxDecoration]):
        self.__default_view().foreground_decoration = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__default_view().floating_action_button

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__default_view().floating_action_button = value

    # floating_action_button_location
    @property
    def floating_action_button_location(
        self,
    ) -> Optional[Union[FloatingActionButtonLocation, OffsetValue]]:
        return self.__default_view().floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(
        self, value: Optional[Union[FloatingActionButtonLocation, OffsetValue]]
    ):
        self.__default_view().floating_action_button_location = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> Optional[CrossAxisAlignment]:
        return self.__default_view().horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: Optional[CrossAxisAlignment]):
        self.__default_view().horizontal_alignment = value

    # vertical_alignment
    @property
    def vertical_alignment(self) -> Optional[MainAxisAlignment]:
        return self.__default_view().vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: Optional[MainAxisAlignment]):
        self.__default_view().vertical_alignment = value

    # spacing
    @property
    def spacing(self) -> OptionalNumber:
        return self.__default_view().spacing

    @spacing.setter
    def spacing(self, value: OptionalNumber):
        self.__default_view().spacing = value

    # padding
    @property
    def padding(self) -> OptionalPaddingValue:
        return self.__default_view().padding

    @padding.setter
    def padding(self, value: OptionalPaddingValue):
        self.__default_view().padding = value

    # bgcolor
    @property
    def bgcolor(self) -> OptionalColorValue:
        return self.__default_view().bgcolor

    @bgcolor.setter
    def bgcolor(self, value: OptionalColorValue):
        self.__default_view().bgcolor = value

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__default_view().scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__default_view().scroll = value

    # auto_scroll
    @property
    def auto_scroll(self):
        return self.__default_view().auto_scroll

    @auto_scroll.setter
    def auto_scroll(self, value: bool):
        self.__default_view().auto_scroll = value

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls


@control("Overlay")
class Overlay(BaseControl):
    controls: list[BaseControl] = field(default_factory=list)


@control("Dialogs")
class Dialogs(BaseControl):
    controls: list[DialogControl] = field(default_factory=list)
