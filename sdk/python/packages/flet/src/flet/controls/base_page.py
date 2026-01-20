import logging
from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
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
    EventHandler,
)
from flet.controls.core.view import View
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import DurationValue
from flet.controls.keys import ScrollKey
from flet.controls.material.app_bar import AppBar
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.navigation_bar import NavigationBar
from flet.controls.material.navigation_drawer import NavigationDrawer
from flet.controls.padding import Padding, PaddingValue
from flet.controls.services.service import Service
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    ColorValue,
    CrossAxisAlignment,
    FloatingActionButtonLocation,
    LocaleConfiguration,
    MainAxisAlignment,
    Number,
    Orientation,
    ScrollMode,
    ThemeMode,
)

logger = logging.getLogger("flet")

if TYPE_CHECKING:
    from flet.controls.theme import Theme


@dataclass
class PageMediaData:
    """
    Represents the environmental metrics of a page or window.

    This data is updated whenever the platform window or layout changes,
    such as when rotating a device, resizing a browser window, or adjusting
    system UI elements like the keyboard or safe areas.
    """

    padding: Padding
    """
    The space surrounding the entire display, accounting for system UI
    like notches and status bars.
    """

    view_padding: Padding
    """
    Similar to [`padding`][(c).], but includes padding that is always reserved
    (even when the system UI is hidden).
    """

    view_insets: Padding
    """
    Areas obscured by system UI overlays, such as the on-screen keyboard
    or system gesture areas.
    """

    device_pixel_ratio: float
    """
    The number of device pixels for each logical pixel.
    """

    orientation: Orientation
    """
    The orientation of the page.
    """

    always_use_24_hour_format: bool = False
    """
    Whether to use 24-hour format when formatting time.

    Note:
        The behavior of this flag is different across platforms:

        - On Android this flag is reported directly from the user settings called
            "Use 24-hour format". It applies to any locale used by the application,
            whether it is the system-wide locale, or the custom locale set by the
            application.
        - On iOS this flag is set to true when the user setting called "24-Hour Time"
            is set or the system-wide locale's default uses 24-hour
            formatting.
    """


@dataclass
class PageResizeEvent(Event["BasePage"]):
    """
    Event fired when the size of the containing window or browser is changed.

    Typically used to adapt layout dynamically in response to resizes,
    such as switching between compact and expanded views in a responsive design.
    """

    width: float
    """
    The new width of the page in logical pixels.
    """

    height: float
    """
    The new height of the page in logical pixels.
    """


@control("BasePage", isolated=True, kw_only=True)
class BasePage(AdaptiveControl):
    """
    A visual container representing a top-level view in a Flet application.

    `BasePage` serves as the base class for [Page][flet.Page] and
    [MultiView][flet.MultiView], and provides a unified surface for rendering
    application content, app bars,
    navigation elements, dialogs, overlays, and more. It manages one
    or more [View][flet.View] instances and exposes high-level layout,
    scrolling, and theming properties.

    Unlike lower-level layout controls (e.g., [Column][flet.Column],
    [Container][flet.Container]), [BasePage][flet.BasePage] represents
    an entire logical view or screen of the app. It provides direct access
    to view-level controls such as [AppBar][flet.AppBar],
    [NavigationBar][flet.NavigationBar],
    [FloatingActionButton][flet.FloatingActionButton],
    and supports system-level events like window resizing and media changes.

    This class is not intended to be used directly in most apps; instead,
    use [Page][flet.Page] or [MultiView][flet.MultiView], which extend this base
    functionality.
    """

    views: list[View] = field(default_factory=lambda: [View()])
    """
    A list of views managed by the page.

    Each [View][flet.View] represents a distinct navigation state or screen
    in the application.

    The first view in the list is considered the active one by default.
    """

    theme_mode: Optional[ThemeMode] = ThemeMode.SYSTEM
    """
    The page's theme mode.
    """

    theme: Optional["Theme"] = None
    """
    Customizes the theme of the application when in light theme mode. Currently, a
    theme can only be automatically generated from a "seed" color. For example, to
    generate light theme from a green color.
    """

    dark_theme: Optional["Theme"] = None
    """
    Customizes the theme of the application when in dark theme mode.
    """

    locale_configuration: Optional[LocaleConfiguration] = None
    """
    Configures supported locales and the current locale.
    """

    show_semantics_debugger: Optional[bool] = None
    """
    Whether to turn on an overlay that shows the accessibility information
    reported by the framework.
    """

    title: Optional[str] = None
    """
    Page or window title.
    """

    enable_screenshots: bool = False
    """
    Enable taking screenshots of the entire page with `take_screenshot` method.
    """

    on_resize: Optional[EventHandler["PageResizeEvent"]] = None
    """
    Called when a user resizes a browser or native OS window containing Flet app

    Example:
        ```python
        def main(page: ft.Page):
            def handle_page_size(e):
                print("New page size:", page.window.width, page.window_height)

            page.on_resize = handle_page_size
        ```
    """

    on_media_change: Optional[EventHandler[PageMediaData]] = None
    """
    Called when [`media`][(c).] has changed.
    """

    media: PageMediaData = field(
        default_factory=lambda: PageMediaData(
            padding=Padding.zero(),
            view_padding=Padding.zero(),
            view_insets=Padding.zero(),
            device_pixel_ratio=0,
            orientation=Orientation.PORTRAIT,
            always_use_24_hour_format=False,
        )
    )
    """
    The current environmental metrics of the page or window.

    This data is updated whenever the platform window or layout changes,
    such as when rotating a device, resizing a browser window, or adjusting
    system UI elements like the keyboard or safe areas.
    """

    width: Optional[Number] = None
    """
    Page width in logical pixels.

    Note:
        - This property is read-only.
        - To get or set the full window height including window chrome (e.g.,
            title bar and borders) when running a Flet app on desktop,
            use the [`width`][flet.Window.width] property of
            [`Page.window`][flet.Page.window] instead.
    """

    height: Optional[Number] = None
    """
    Page height in logical pixels.

    Note:
        - This property is read-only.
        - To get or set the full window height including window chrome (e.g.,
            title bar and borders) when running a Flet app on desktop,
            use the [`height`][flet.Window.height] property of
            [`Page.window`][flet.Page.window] instead.
    """

    _overlay: "Overlay" = field(default_factory=lambda: Overlay())
    _dialogs: "Dialogs" = field(default_factory=lambda: Dialogs())

    def __root_view(self) -> View:
        if len(self.views) == 0:
            raise RuntimeError("views list is empty.")
        return self.views[0]

    def __top_view(self) -> View:
        if len(self.views) == 0:
            raise RuntimeError("views list is empty.")
        return self.views[-1]

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

    async def scroll_to(
        self,
        offset: Optional[Number] = None,
        delta: Optional[Number] = None,
        scroll_key: Union[ScrollKey, str, int, float, bool, None] = None,
        duration: Optional[DurationValue] = None,
        curve: Optional[AnimationCurve] = None,
    ) -> None:
        """
        Moves scroll position to either absolute `offset`, relative `delta` or jump to
        the control with specified `scroll_key`.

        See [`Column.scroll_to()`][flet.Column.scroll_to] for method details
        and examples.
        """
        await self.__root_view().scroll_to(
            offset=offset,
            delta=delta,
            scroll_key=scroll_key,
            duration=duration,
            curve=curve,
        )

    def show_dialog(self, dialog: DialogControl) -> None:
        """
        Displays a dialog and manages its dismissal lifecycle.

        This method adds the specified `dialog` to the active dialog stack
        and renders it on the page. If the dialog is already open, a `RuntimeError`
        is raised.
        The [`on_dismiss`][flet.DialogControl.] handler of the dialog
        is temporarily wrapped to ensure the dialog is removed from the stack and
        its dismissal event is triggered appropriately.

        Args:
            dialog: The dialog instance to display. Must not yet be open.

        Raises:
            RuntimeError: If the specified dialog is already open.
        """
        if dialog in self._dialogs.controls:
            raise RuntimeError("Dialog is already opened")

        original_on_dismiss = dialog.on_dismiss

        async def wrapped_on_dismiss(*args):
            if dialog in self._dialogs.controls:
                self._dialogs.controls.remove(dialog)
                self._dialogs.update()
            dialog.on_dismiss = original_on_dismiss
            e = args[0]
            if (
                original_on_dismiss and (e.data is None or e.data)  # e.data == True for
                # TimePicker and DatePicker if they were dismissed without
                # changing the value
            ):
                await dialog._trigger_event("dismiss", e)

        dialog.open = True
        dialog.on_dismiss = wrapped_on_dismiss

        self._dialogs.controls.append(dialog)
        self._dialogs.update()

    def pop_dialog(self) -> Optional[DialogControl]:
        """
        Closes the most recently opened dialog.

        This method searches the active dialog stack for the topmost dialog
        that is currently open, marks it as closed, updates its state,
        and returns the closed dialog.

        Returns:
            The closed dialog instance if one was found, otherwise `None`.
        """
        dialog = next(
            (dlg for dlg in reversed(self._dialogs.controls) if dlg.open), None
        )
        if not dialog:
            return None
        dialog.open = False
        dialog.update()
        return dialog

    async def show_drawer(self):
        """
        Show the drawer.

        Raises:
            ValueError: If no [`drawer`][(c).] is defined.
        """
        await self.__top_view().show_drawer()

    async def close_drawer(self):
        """
        Close the drawer.
        """
        await self.__top_view().close_drawer()

    async def show_end_drawer(self):
        """
        Show the end drawer.

        Raises:
            ValueError: If no [`end_drawer`][(c).] is defined.
        """
        await self.__top_view().show_end_drawer()

    async def close_end_drawer(self):
        """
        Close the end drawer.
        """
        await self.__top_view().close_end_drawer()

    async def take_screenshot(
        self,
        pixel_ratio: Optional[Number] = None,
        delay: Optional[DurationValue] = None,
    ) -> bytes:
        """
        Captures a screenshot of the entire page with overlays.

        Args:
            pixel_ratio: A pixel ratio of the captured screenshot.
                If `None`, device-specific pixel ratio will be used.
            delay: A delay before taking a screenshot.
                The delay will be 20 milliseconds if not specified.

        Returns:
            Screenshot in PNG format.
        """
        return await self._invoke_method(
            "take_screenshot", arguments={"pixel_ratio": pixel_ratio, "delay": delay}
        )

    # overlay
    @property
    def overlay(self) -> list[BaseControl]:
        return self._overlay.controls

    # controls
    @property
    def controls(self) -> list[BaseControl]:
        return self.__root_view().controls

    @controls.setter
    def controls(self, value: list[BaseControl]):
        self.__root_view().controls = value

    # appbar
    @property
    def appbar(self) -> Union[AppBar, CupertinoAppBar, None]:
        """
        Gets or sets the top application bar ([AppBar][flet.AppBar] or
        [CupertinoAppBar][flet.CupertinoAppBar]) for the view.

        The app bar typically displays the page title and optional actions
        such as navigation icons, menus, or other interactive elements.
        """
        return self.__root_view().appbar

    @appbar.setter
    def appbar(self, value: Union[AppBar, CupertinoAppBar, None]):
        self.__root_view().appbar = value

    # bottom_appbar
    @property
    def bottom_appbar(self) -> Optional[BottomAppBar]:
        return self.__root_view().bottom_appbar

    @bottom_appbar.setter
    def bottom_appbar(self, value: Optional[BottomAppBar]):
        self.__root_view().bottom_appbar = value

    # navigation_bar
    @property
    def navigation_bar(self) -> Optional[Union[NavigationBar, CupertinoNavigationBar]]:
        return self.__root_view().navigation_bar

    @navigation_bar.setter
    def navigation_bar(
        self,
        value: Optional[Union[NavigationBar, CupertinoNavigationBar]],
    ):
        self.__root_view().navigation_bar = value

    # drawer
    @property
    def drawer(self) -> Optional[NavigationDrawer]:
        return self.__root_view().drawer

    @drawer.setter
    def drawer(self, value: Optional[NavigationDrawer]):
        self.__root_view().drawer = value

    # end_drawer
    @property
    def end_drawer(self) -> Optional[NavigationDrawer]:
        return self.__root_view().end_drawer

    @end_drawer.setter
    def end_drawer(self, value: Optional[NavigationDrawer]):
        self.__root_view().end_drawer = value

    # decoration
    @property
    def decoration(self) -> Optional[BoxDecoration]:
        return self.__root_view().decoration

    @decoration.setter
    def decoration(self, value: Optional[BoxDecoration]):
        self.__root_view().decoration = value

    # foreground_decoration
    @property
    def foreground_decoration(self) -> Optional[BoxDecoration]:
        return self.__root_view().foreground_decoration

    @foreground_decoration.setter
    def foreground_decoration(self, value: Optional[BoxDecoration]):
        self.__root_view().foreground_decoration = value

    # floating_action_button
    @property
    def floating_action_button(self) -> Optional[FloatingActionButton]:
        return self.__root_view().floating_action_button

    @floating_action_button.setter
    def floating_action_button(self, value: Optional[FloatingActionButton]):
        self.__root_view().floating_action_button = value

    # floating_action_button_location
    @property
    def floating_action_button_location(
        self,
    ) -> Optional[Union[FloatingActionButtonLocation, OffsetValue]]:
        return self.__root_view().floating_action_button_location

    @floating_action_button_location.setter
    def floating_action_button_location(
        self, value: Optional[Union[FloatingActionButtonLocation, OffsetValue]]
    ):
        self.__root_view().floating_action_button_location = value

    # horizontal_alignment
    @property
    def horizontal_alignment(self) -> CrossAxisAlignment:
        return self.__root_view().horizontal_alignment

    @horizontal_alignment.setter
    def horizontal_alignment(self, value: CrossAxisAlignment):
        self.__root_view().horizontal_alignment = value

    # vertical_alignment
    @property
    def vertical_alignment(self) -> MainAxisAlignment:
        return self.__root_view().vertical_alignment

    @vertical_alignment.setter
    def vertical_alignment(self, value: MainAxisAlignment):
        self.__root_view().vertical_alignment = value

    # spacing
    @property
    def spacing(self) -> Number:
        return self.__root_view().spacing

    @spacing.setter
    def spacing(self, value: Number):
        self.__root_view().spacing = value

    # padding
    @property
    def padding(self) -> Optional[PaddingValue]:
        return self.__root_view().padding

    @padding.setter
    def padding(self, value: Optional[PaddingValue]):
        self.__root_view().padding = value

    # bgcolor
    @property
    def bgcolor(self) -> Optional[ColorValue]:
        return self.__root_view().bgcolor

    @bgcolor.setter
    def bgcolor(self, value: Optional[ColorValue]):
        self.__root_view().bgcolor = value

    # scroll
    @property
    def scroll(self) -> Optional[ScrollMode]:
        return self.__root_view().scroll

    @scroll.setter
    def scroll(self, value: Optional[ScrollMode]):
        self.__root_view().scroll = value

    # auto_scroll
    @property
    def auto_scroll(self) -> bool:
        return self.__root_view().auto_scroll

    @auto_scroll.setter
    def auto_scroll(self, value: bool):
        self.__root_view().auto_scroll = value

    # services
    @property
    def services(self) -> list[Service]:
        return self.__root_view().services

    @services.setter
    def services(self, value: list[Service]):
        self.__root_view().services = value

    # Magic methods
    def __contains__(self, item: Control) -> bool:
        return item in self.controls


@control("Overlay")
class Overlay(BaseControl):
    controls: list[BaseControl] = field(default_factory=list)

    def init(self):
        super().init()
        self._internals["host_positioned"] = True


@control("Dialogs")
class Dialogs(BaseControl):
    controls: list[DialogControl] = field(default_factory=list)
