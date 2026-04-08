from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationStyle
from flet.controls.base_control import value
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.box import BoxConstraints, BoxDecoration, BoxShadowValue
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue
from flet.controls.geometry import Size
from flet.controls.margin import MarginValue
from flet.controls.material.expansion_tile import TileAffinity
from flet.controls.material.list_tile import ListTileStyle, ListTileTitleAlignment
from flet.controls.material.menu_bar import MenuStyle
from flet.controls.material.navigation_bar import NavigationBarLabelBehavior
from flet.controls.material.navigation_rail import NavigationRailLabelType
from flet.controls.material.popup_menu_button import PopupMenuPosition
from flet.controls.material.slider import SliderInteraction
from flet.controls.material.snack_bar import DismissDirection, SnackBarBehavior
from flet.controls.material.tabs import (
    TabAlignment,
    TabBarIndicatorSize,
    TabIndicatorAnimation,
    UnderlineTabIndicator,
)
from flet.controls.material.textfield import TextCapitalization
from flet.controls.material.tooltip import TooltipTriggerMode
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    Brightness,
    ClipBehavior,
    ColorValue,
    IconData,
    MainAxisAlignment,
    MouseCursor,
    NotchShape,
    Number,
    StrokeCap,
    TextAlign,
    VisualDensity,
)


class PageTransitionTheme(Enum):
    """
    Page transition preset for route changes.

    These could, for example, be used together with \
    :class:`~flet.PageTransitionsTheme` to
    define per-platform navigation animations.
    """

    NONE = "none"
    """
    Disables route transition animation.
    """

    FADE_UPWARDS = "fadeUpwards"
    """
    Fade-and-slide transition where the incoming page moves upward,
    similar to the one provided by Android O.
    """

    OPEN_UPWARDS = "openUpwards"
    """
    Upward reveal transition with clipping/scrim,
    matching the transition used on Android P.
    """

    ZOOM = "zoom"
    """
    Zoom/fade transition used by modern Material route animations,
    similar to the one provided in Android Q.
    """

    CUPERTINO = "cupertino"
    """
    Cupertino-style horizontal page transition,
    which matches native iOS page transitions.
    """

    PREDICTIVE = "predictive"
    """
    Predictive-back transition that allows peeking behind the current route on Android.
    """

    FADE_FORWARDS = "fadeForwards"
    """
    Fade-forward Material route transition, similar to the one provided by Android U.
    """


@value
class PageTransitionsTheme:
    """
    Per-platform mapping of route transition presets.

    Assigned to :attr:`flet.Theme.page_transitions` to
    override how Material routes animate on each target platform.
    """

    android: Optional[PageTransitionTheme] = None
    """
    Transition preset for Android routes.

    If `None`, defaults to :attr:`flet.PageTransitionTheme.FADE_UPWARDS`.
    """

    ios: Optional[PageTransitionTheme] = None
    """
    Transition preset for iOS routes.

    If `None`, defaults to :attr:`flet.PageTransitionTheme.CUPERTINO`.
    """

    linux: Optional[PageTransitionTheme] = None
    """
    Transition preset for Linux desktop routes.

    If `None`, defaults to :attr:`flet.PageTransitionTheme.ZOOM`.
    """

    macos: Optional[PageTransitionTheme] = None
    """
    Transition preset for macOS desktop routes.

    If `None`, defaults to :attr:`flet.PageTransitionTheme.ZOOM`.
    """

    windows: Optional[PageTransitionTheme] = None
    """
    Transition preset for Windows desktop routes.

    If `None`, defaults to :attr:`flet.PageTransitionTheme.ZOOM`.
    """


@value
class ColorScheme:
    """
    A set of more than 40 colors based on the [Material \
    spec](https://m3.material.io/styles/color/the-color-system/color-roles) that can \
    be used to configure the color properties of most components.
    Read more about color schemes in
    [here](https://api.flutter.dev/flutter/material/ColorScheme-class.html).
    """

    primary: Optional[ColorValue] = None
    """
    The color displayed most frequently across your app's screens and components.
    """

    on_primary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on :attr:`primary`.
    """

    primary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than :attr:`primary`.
    """

    on_primary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`primary_container`.
    """

    secondary: Optional[ColorValue] = None
    """
    An accent color used for less prominent components in the UI, such as filter \
    :class:`~flet.Chip`s, while expanding the opportunity for color expression.
    """

    on_secondary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on :attr:`secondary`.
    """

    secondary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than :attr:`secondary`.
    """

    on_secondary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`secondary_container`.
    """

    tertiary: Optional[ColorValue] = None
    """
    A color used as a contrasting accent that can balance :attr:`primary` and \
    :attr:`secondary` colors or bring heightened attention to an element, such as an \
    input field.
    """

    on_tertiary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on :attr:`tertiary`.
    """

    tertiary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than :attr:`tertiary`.
    """

    on_tertiary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`tertiary_container`.
    """

    error: Optional[ColorValue] = None
    """
    The color to use for input validation errors, e.g. for \
    :attr:`flet.FormFieldControl.error`.
    """

    on_error: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on :attr:`error`.
    """

    error_container: Optional[ColorValue] = None
    """
    A color used for error elements needing less emphasis than :attr:`error`.
    """

    on_error_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`error_container`.
    """

    surface: Optional[ColorValue] = None
    """
    The background color for widgets like :class:`~flet.Card`.
    """

    on_surface: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on :attr:`surface`.
    """

    on_surface_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`surface_container_highest`.
    """

    outline: Optional[ColorValue] = None
    """
    A utility color that creates boundaries and emphasis to improve usability.
    """

    outline_variant: Optional[ColorValue] = None
    """
    A utility color that creates boundaries for decorative elements when a 3:1 \
    contrast isn’t required, such as for dividers or decorative elements.
    """

    shadow: Optional[ColorValue] = None
    """
    A color use to paint the drop shadows of elevated components.
    """

    scrim: Optional[ColorValue] = None
    """
    A color use to paint the scrim around of modal components.
    """

    inverse_surface: Optional[ColorValue] = None
    """
    A surface color used for displaying the reverse of what’s seen in the surrounding \
    UI, for example in a :class:`~flet.SnackBar` to bring attention to an alert.
    """

    on_inverse_surface: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on :attr:`inverse_surface`.
    """

    inverse_primary: Optional[ColorValue] = None
    """
    An accent color used for displaying a highlight color on :attr:`inverse_surface`
    backgrounds, like button text in a :class:`~flet.SnackBar`.
    """

    surface_tint: Optional[ColorValue] = None
    """
    A color used as an overlay on a surface color to indicate a component's elevation.
    """

    on_primary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having \
    :attr:`primary_fixed` color.
    """

    on_secondary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having \
    :attr:`secondary_fixed` color.
    """

    on_tertiary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having \
    :attr:`tertiary_fixed` color.
    """

    on_primary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than \
    :attr:`on_primary_fixed`.
    """

    on_secondary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than \
    :attr:`on_secondary_fixed`.
    """

    on_tertiary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than \
    :attr:`on_tertiary_fixed`.
    """

    primary_fixed: Optional[ColorValue] = None
    """
    A substitute for :attr:`primary_container` that's the same color for the dark \
    and light themes.
    """

    secondary_fixed: Optional[ColorValue] = None
    """
    A substitute for :attr:`secondary_container` that's the same color for the dark \
    and light themes.
    """

    tertiary_fixed: Optional[ColorValue] = None
    """
    A substitute for :attr:`tertiary_container` that's the same color for dark and \
    light themes.
    """

    primary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than :attr:`primary_fixed`.
    """

    secondary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than :attr:`secondary_fixed`.
    """

    surface_bright: Optional[ColorValue] = None
    """
    A color that's always the lightest in the dark or light theme.
    """

    surface_container: Optional[ColorValue] = None
    """
    A recommended color role for a distinct area within the surface.
    """

    surface_container_high: Optional[ColorValue] = None
    """
    A surface container color with a darker tone.
    """

    surface_container_highest: Optional[ColorValue] = None
    """
    A surface container color with the darkest tone. It is used to create the most \
    emphasis against the surface.
    """

    surface_container_low: Optional[ColorValue] = None
    """
    A surface container color with a lighter tone that creates less emphasis than \
    `surface_container` but more emphasis than :attr:`surface_container_lowest`.
    """

    surface_container_lowest: Optional[ColorValue] = None
    """
    A surface container color with the lightest tone and the least emphasis relative \
    to the surface.
    """

    surface_dim: Optional[ColorValue] = None
    """
    A color that's always darkest in the dark or light theme.
    """

    tertiary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than :attr:`tertiary_fixed`.
    """


@value
class TextTheme:
    """
    Customizes :class:`~flet.Text` styles.

    Material 3 design
    [defines](http://localhost:3000/docs/controls/text#pre-defined-theme-text-styles)
    5 groups of text styles with 3 sizes in each group: "Display", "Headline", "Title",
    "Label" and "Body" which are used across Flet controls.
    """

    body_large: Optional[TextStyle] = None
    """
    Largest of the body styles. Body styles are used for longer passages of text.
    """

    body_medium: Optional[TextStyle] = None
    """
    Middle size of the body styles. Body styles are used for longer passages of text.
    The default text style for Material.
    """

    body_small: Optional[TextStyle] = None
    """
    Smallest of the body styles.
    """

    display_large: Optional[TextStyle] = None
    """
    Largest of the display styles. As the largest text on the screen, display styles \
    are reserved for short, important text or numerals. They work best on large \
    screens.
    """

    display_medium: Optional[TextStyle] = None
    """
    Middle size of the display styles.
    """

    display_small: Optional[TextStyle] = None
    """
    Smallest of the display styles.
    """

    headline_large: Optional[TextStyle] = None
    """
    Largest of the headline styles. Headline styles are smaller than display styles.
    They're best-suited for short, high-emphasis text on smaller screens.
    """

    headline_medium: Optional[TextStyle] = None
    """
    Middle size of the headline styles.
    """

    headline_small: Optional[TextStyle] = None
    """
    Smallest of the headline styles.
    """

    label_large: Optional[TextStyle] = None
    """
    Largest of the label styles. Label styles are smaller, utilitarian styles, used \
    for areas of the UI such as text inside of components or very small supporting \
    text in the content body, like captions. Used for text on :class:`~flet.Button`, \
    :class:`~flet.TextButton` and :class:`~flet.OutlinedButton`.
    """

    label_medium: Optional[TextStyle] = None
    """
    Middle size of the label styles.
    """

    label_small: Optional[TextStyle] = None
    """
    Smallest of the label styles.
    """

    title_large: Optional[TextStyle] = None
    """
    Largest of the title styles. Titles are smaller than headline styles and should be \
    used for shorter, medium-emphasis text.
    """

    title_medium: Optional[TextStyle] = None
    """
    Middle size of the title styles.
    """

    title_small: Optional[TextStyle] = None
    """
    Smallest of the title styles.
    """


@value
class ScrollbarTheme:
    """
    Customizes the colors, thickness, and shape of scrollbars across the app.
    """

    thumb_visibility: Optional[ControlStateValue[bool]] = None
    """
    Indicates that the scrollbar thumb should be visible, even when a scroll is not \
    underway. When `False`, the scrollbar will be shown during scrolling and will fade \
    out otherwise. When `True`, the scrollbar will always be visible and never fade \
    out. Property value could be either a single boolean value or a dictionary with \
    `ft.ControlState` as keys and boolean as values.
    """

    thickness: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The thickness of the scrollbar in the cross axis of the scrollable. Property value \
    could be either a single float value or a dictionary with `ft.ControlState` as \
    keys and float as values.
    """

    track_visibility: Optional[ControlStateValue[bool]] = None
    """
    Indicates that the scrollbar track should be visible. When `True`, the scrollbar \
    track will always be visible so long as the thumb is visible. If the scrollbar \
    thumb is not visible, the track will not be visible either. Defaults to `False` \
    when `None`. If this property is `None`, then `ScrollbarTheme.track_visibility` of \
    `Theme.scrollbar_theme` is used. If that is also `None`, the default value is \
    `False`. Property value could be either a single boolean value or a dictionary \
    with `ft.ControlState` as keys and boolean as values.
    """

    radius: Optional[Number] = None
    """
    The Radius of the scrollbar thumb's rounded rectangle corners.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar thumb. The value is either a single \
    color string or `ft.ControlState` dictionary.
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar track. The value is either a single \
    color string or `ft.ControlState` dictionary.
    """

    track_border_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar track border. The value is either a \
    single color string or `ft.ControlState` dictionary.
    """

    cross_axis_margin: Optional[Number] = None
    """
    Distance from the scrollbar thumb to the nearest cross axis edge in logical \
    pixels.
    The scrollbar track consumes this space. Must not be null and defaults to 0.
    """

    main_axis_margin: Optional[Number] = None
    """
    Distance from the scrollbar thumb's start and end to the edge of the viewport in \
    logical pixels. It affects the amount of available paint area. The scrollbar track \
    consumes this space. Mustn't be null and defaults to 0.
    """

    min_thumb_length: Optional[Number] = None
    """
    The preferred smallest size the scrollbar thumb can shrink to when the total \
    scrollable extent is large, the current visible viewport is small, and the \
    viewport is not overscrolled.
    """

    interactive: Optional[bool] = None
    """
    Whether the Scrollbar should be interactive and respond to dragging on the thumb, \
    or tapping in the track area. When `False`, the scrollbar will not respond to \
    gesture or hover events, and will allow to click through it. Defaults to `True` \
    when `None`, unless on Android, which will default to `False` when `None`.
    """


@value
class TabBarTheme:
    """
    Customizes the appearance of :class:`~flet.TabBar` control across the app.
    """

    indicator_size: Optional[TabBarIndicatorSize] = None
    """
    Overrides the default value for :attr:`flet.TabBar.indicator_size`.
    """

    indicator: Optional[UnderlineTabIndicator] = None
    """
    Overrides the default value for :attr:`flet.TabBar.indicator`.
    """

    indicator_animation: Optional[TabIndicatorAnimation] = None
    """
    Overrides the default value for :attr:`flet.TabBar.indicator_animation`.
    """

    splash_border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.splash_border_radius`.
    """

    tab_alignment: Optional[TabAlignment] = None
    """
    Overrides the default value for :attr:`flet.TabBar.tab_alignment`.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for :attr:`flet.TabBar.overlay_color`.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.divider_color`.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.indicator_color`.
    """

    mouse_cursor: Optional[ControlStateValue[Optional[MouseCursor]]] = None
    """
    Overrides the default value for :attr:`flet.TabBar.mouse_cursor`.
    """

    divider_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.TabBar.divider_height`.
    """

    label_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.label_color`.
    """

    unselected_label_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.unselected_label_color`.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.TabBar.label_padding`.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.TabBar.label_text_style`.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.TabBar.unselected_label_text_style`.
    """


@value
class SystemOverlayStyle:
    """
    Allows the customization of the mobile's system overlay (which consists of the \
    system status and navigation bars) appearance.
    """

    status_bar_color: Optional[ColorValue] = None
    """
    The color of the status bar.
    """

    system_navigation_bar_color: Optional[ColorValue] = None
    """
    The color of the system navigation bar.
    """

    system_navigation_bar_divider_color: Optional[ColorValue] = None
    """
    The color of the divider between the system navigation bar and the app content.
    """

    enforce_system_navigation_bar_contrast: Optional[bool] = None
    """
    Indicates whether the system should enforce contrast for the status bar when \
    setting a transparent status bar.
    """

    enforce_system_status_bar_contrast: Optional[bool] = None
    """
    Indicates whether the system should enforce contrast for the navigation bar when \
    setting a transparent navigation bar.
    """

    system_navigation_bar_icon_brightness: Optional[Brightness] = None
    """
    The brightness of the system navigation bar icons.
    """

    status_bar_brightness: Optional[Brightness] = None
    """
    The brightness of the status bar.
    """

    status_bar_icon_brightness: Optional[Brightness] = None
    """
    The brightness of the status bar icons.
    """


@value
class DialogTheme:
    """
    Customizes the appearance of :class:`~flet.AlertDialog` across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.bgcolor` in all descendant \
    :class:`~flet.AlertDialog` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.shadow_color` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Used to configure the :class:`~flet.IconTheme` for the \
    :attr:`flet.AlertDialog.icon` \
    control.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.elevation` in all \
    descendant \
    dialog controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.shape` in all descendant \
    :class:`~flet.AlertDialog` controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.title_text_style` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.content_text_style` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.alignment` in all \
    descendant \
    :class:`~flet.AlertDialog` controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.actions_padding` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.clip_behavior` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.barrier_color` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.AlertDialog.inset_padding` in all \
    descendant :class:`~flet.AlertDialog` controls.
    """


@value
class ButtonTheme:
    """
    Customizes the appearance of :class:`~flet.Button` across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of :attr:`flet.Button.style` in all descendant \
    :class:`~flet.Button` controls.
    """


@value
class OutlinedButtonTheme:
    """
    Customizes the appearance of :class:`~flet.OutlinedButton` across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of :attr:`flet.OutlinedButton.style` in all descendant \
    :class:`~flet.OutlinedButton` controls.
    """


@value
class TextButtonTheme:
    """
    Customizes the appearance of :class:`~flet.TextButton` across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of :attr:`flet.TextButton.style` in all descendant \
    :class:`~flet.TextButton` controls.
    """


@value
class FilledButtonTheme:
    """
    Customizes the appearance of :class:`~flet.FilledButton` across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of :attr:`flet.Button.style`
    in all descendant \
    :class:`~flet.FilledButton` controls.
    """


@value
class IconButtonTheme:
    """
    Customizes the appearance of :class:`~flet.IconButton` across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of :attr:`flet.IconButton.style` in all descendant \
    :class:`~flet.IconButton` controls.
    """


@value
class BottomSheetTheme:
    """
    Customizes the appearance of :class:`~flet.BottomSheet` across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.bgcolor` in all descendant \
    :class:`~flet.BottomSheet` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.elevation` in all \
    descendant \
    :class:`~flet.BottomSheet` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.shape` in all descendant \
    :class:`~flet.BottomSheet` controls.
    """

    show_drag_handle: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.show_drag_handle` in all \
    descendant :class:`~flet.BottomSheet` controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.clip_behavior` in all \
    descendant :class:`~flet.BottomSheet` controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.size_constraints` in all \
    descendant :class:`~flet.BottomSheet` controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.BottomSheet.barrier_color` in all \
    descendant :class:`~flet.BottomSheet` controls.
    """

    drag_handle_color: Optional[ColorValue] = None
    """
    Overrides the default value of drag handle color in all descendant \
    :class:`~flet.BottomSheet` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of shadow color in all descendant \
    :class:`~flet.BottomSheet` controls.
    """


@value
class CardTheme:
    """
    Customizes the appearance of :class:`~flet.Card` across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Card.clip_behavior` in all descendant \
    :class:`~flet.Card` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Card.shadow_color` in all descendant \
    :class:`~flet.Card` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Card.elevation` in all descendant \
    :class:`~flet.Card` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.Card.shape` in all descendant \
    :class:`~flet.Card` controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of :attr:`flet.Card.clip_behavior` in all descendant \
    :class:`~flet.Card` controls.
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value of :attr:`flet.Card.margin` in all descendant \
    :class:`~flet.Card` controls.
    """


@value
class ChipTheme:
    """
    Customizes the appearance of :class:`~flet.Chip` across the app.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Chip.color` in all descendant \
    :class:`~flet.Chip` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.bgcolor` in all descendant \
    :class:`~flet.Chip` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.shadow_color` in all descendant \
    :class:`~flet.Chip` controls.
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.selected_shadow_color` in all \
    descendant :class:`~flet.Chip` controls.
    """

    disabled_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.disabled_color` in all descendant \
    :class:`~flet.Chip` controls.
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.selected_color` in all descendant \
    :class:`~flet.Chip` controls.
    """

    check_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.check_color` in all descendant \
    :class:`~flet.Chip` controls.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.delete_icon_color` in all \
    descendant \
    :class:`~flet.Chip` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Chip.elevation` in all descendant \
    :class:`~flet.Chip` controls.
    """

    elevation_on_click: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Chip.elevation_on_click` in all \
    descendant :class:`~flet.Chip` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.Chip.shape` in all descendant \
    :class:`~flet.Chip` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.padding` in all descendant \
    :class:`~flet.Chip` controls.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Chip.label_padding` in all descendant \
    :class:`~flet.Chip` controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.Chip.label_text_style` in all \
    descendant \
    :class:`~flet.Chip` controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of :attr:`flet.Chip.border_side` in all descendant \
    :class:`~flet.Chip` controls.
    """

    show_checkmark: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.Chip.show_checkmark` in all descendant \
    :class:`~flet.Chip` controls.
    """

    leading_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of :attr:`flet.Chip.leading_size_constraints` in all \
    descendant :class:`~flet.Chip` controls.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of :attr:`flet.Chip.delete_icon_size_constraints` in \
    all \
    descendant :class:`~flet.Chip` controls.
    """

    brightness: Optional[Brightness] = None
    """
    Overrides the default value for all chips which affects various base material \
    color choices in the chip rendering.
    """

    # secondary_selected_color: Optional[ColorValue] = None
    # secondary_label_text_style: Optional[TextStyle] = None


@value
class FloatingActionButtonTheme:
    """
    Customizes the appearance of :class:`~flet.FloatingActionButton`
    across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled :class:`~flet.FloatingActionButton`'s \
    background.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to use for filling the button when the button has a pointer hovering \
    over it.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for filling the button when the button has input focus.
    """

    foreground_color: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled :class:`~flet.FloatingActionButton`'s \
    foreground.
    """

    splash_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.FloatingActionButton.splash_color` in \
    all \
    descendant :class:`~flet.FloatingActionButton` controls.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the unselected, enabled \
    :class:`~flet.FloatingActionButton`'s elevation foreground.
    """

    focus_elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this button relative to its parent when the \
    button has the input focus.
    """

    hover_elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this button relative to its parent when the \
    button is enabled and has a pointer hovering over it.
    """

    highlight_elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the selected, enabled \
    :class:`~flet.FloatingActionButton`'s elevation foreground.
    """

    disabled_elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the disabled :class:`~flet.FloatingActionButton`'s \
    elevation foreground.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.FloatingActionButton.shape` in all \
    descendant :class:`~flet.FloatingActionButton` controls.
    """

    enable_feedback: Optional[bool] = None
    """
    If specified, defines the feedback property for :class:`~flet.FloatingActionButton`.
    """

    extended_padding: Optional[PaddingValue] = None
    """
    The padding for a :class:`~flet.FloatingActionButton`'s that has both icon and \
    content.
    """

    text_style: Optional[TextStyle] = None
    """
    Text style merged into default text style of \
    :attr:`flet.FloatingActionButton.content`.
    """

    icon_label_spacing: Optional[Number] = None
    """
    The spacing between the icon and the label for :class:`~flet.FloatingActionButton`.
    """

    extended_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of :class:`~flet.FloatingActionButton` that \
    has \
    both icon and content.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of :class:`~flet.FloatingActionButton` that \
    has \
    either icon or content and is not a mini button.
    """

    # large_size_constraints: Optional[BoxConstraints] = None
    # small_size_constraints: Optional[BoxConstraints] = None


@value
class NavigationRailTheme:
    """
    Customizes the appearance of :class:`~flet.NavigationRail` across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the :class:`~flet.NavigationRail`'s background.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.indicator_color` in all \
    descendant :class:`~flet.NavigationRail` controls. when \
    :attr:`flet.NavigationRailTheme.use_indicator`
    is true.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the :class:`~flet.NavigationRail`'s elevation.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.indicator_shape` in all \
    descendant :class:`~flet.NavigationRail` controls.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of \
    :attr:`flet.NavigationRail.unselected_label_text_style`
    in all descendant :class:`~flet.NavigationRail` controls.
    """

    selected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.selected_label_text_style`
    in all descendant :class:`~flet.NavigationRail` controls.
    """

    label_type: Optional[NavigationRailLabelType] = None
    """
    The type that defines the layout and behavior of the labels in the \
    :class:`~flet.NavigationRail`.
    """

    min_width: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.min_width` in all \
    descendant :class:`~flet.NavigationRail` controls when they are not extended.
    """

    min_extended_width: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.min_extended_width` in \
    all \
    descendant :class:`~flet.NavigationRail` controls when they are extended.
    """

    group_alignment: Optional[Number] = None
    """
    The alignment for the :attr:`flet.NavigationRail.destinations` as they are \
    positioned within the :class:`~flet.NavigationRail`.
    """

    use_indicator: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.NavigationRail.use_indicator` in all \
    descendant :class:`~flet.NavigationRail` controls.
    """


@value
class AppBarTheme:
    """
    Customizes the appearance of :class:`~flet.AppBar` controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AppBar.color` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AppBar.bgcolor` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.AppBar.shadow_color` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.AppBar.elevation` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.AppBar.shape` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.AppBar.title_text_style` in all \
    descendant :class:`~flet.AppBar` controls.
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.AppBar.toolbar_text_style` in all \
    descendant :class:`~flet.AppBar` controls.
    """

    center_title: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.AppBar.center_title` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    title_spacing: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.AppBar.title_spacing` in all descendant \
    :class:`~flet.AppBar` controls.
    """

    elevation_on_scroll: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.AppBar.elevation_on_scroll` in all \
    descendant :class:`~flet.AppBar` controls.
    """

    toolbar_height: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.AppBar.toolbar_height` in all \
    descendant \
    :class:`~flet.AppBar` controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.AppBar.actions_padding` in all \
    descendant \
    :class:`~flet.AppBar` controls.
    """


@value
class BottomAppBarTheme:
    """
    Customizes the appearance of :class:`~flet.BottomAppBar` controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.bgcolor`
    in all descendant :class:`~flet.BottomAppBar` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.shadow_color` in all \
    descendant :class:`~flet.BottomAppBar` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.elevation` in all \
    descendant :class:`~flet.BottomAppBar` controls.
    """

    height: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.height` in all descendant \
    :class:`~flet.BottomAppBar` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.padding`
    in all descendant :class:`~flet.BottomAppBar` controls.
    """

    shape: Optional[NotchShape] = None
    """
    Overrides the default value of :attr:`flet.BottomAppBar.shape` in all descendant \
    :class:`~flet.BottomAppBar` controls.
    """


@value
class RadioTheme:
    """
    Defines default property values for descendant :class:`~flet.Radio` controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Radio.fill_color` in all descendant \
    :class:`~flet.Radio` controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Radio.overlay_color` in all descendant \
    :class:`~flet.Radio` controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Radio.splash_radius` in all descendant \
    :class:`~flet.Radio` controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of :attr:`flet.Radio.visual_density`
    in all descendant :class:`~flet.Radio` controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of :attr:`flet.Radio.mouse_cursor`
    in all descendant :class:`~flet.Radio` controls.
    """


@value
class CheckboxTheme:
    """
    Defines default property values for descendant :class:`~flet.Checkbox` controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.overlay_color` in all \
    descendant \
    :class:`~flet.Checkbox` controls.
    """

    check_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.check_color` in all descendant \
    :class:`~flet.Checkbox` controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.fill_color` in all descendant \
    :class:`~flet.Checkbox` controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.splash_radius` in all \
    descendant \
    :class:`~flet.Checkbox` controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.border_side` in all descendant \
    :class:`~flet.Checkbox` controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.visual_density` in all \
    descendant :class:`~flet.Checkbox` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.shape` in all descendant \
    :class:`~flet.Checkbox` controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of :attr:`flet.Checkbox.mouse_cursor` in all \
    descendant \
    :class:`~flet.Checkbox` controls.
    """


@value
class BadgeTheme:
    """
    Defines default property values for descendant :class:`~flet.Badge` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Badge.bgcolor` in all descendant \
    :class:`~flet.Badge` controls.
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Badge.text_color` in all descendant \
    :class:`~flet.Badge` controls.
    """

    small_size: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Badge.small_size` in all descendant \
    :class:`~flet.Badge` controls.
    """

    large_size: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Badge.large_size` in all descendant \
    :class:`~flet.Badge` controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of :attr:`flet.Badge.alignment` in all descendant \
    :class:`~flet.Badge` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Badge.padding` in all descendant \
    :class:`~flet.Badge` controls.
    """

    offset: Optional[OffsetValue] = None
    """
    Overrides the default value of :attr:`flet.Badge.offset` in all descendant \
    :class:`~flet.Badge` controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.Badge.text_style` in all descendant \
    :class:`~flet.Badge` controls.
    """


@value
class SwitchTheme:
    """
    Defines default property values for descendant :class:`~flet.Switch` controls.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Switch.thumb_color` in all descendant \
    :class:`~flet.Switch` controls.
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Switch.track_color` in all descendant \
    :class:`~flet.Switch` controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Switch.overlay_color`
    in all descendant :class:`~flet.Switch` controls.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.Switch.track_outline_color` in all \
    descendant :class:`~flet.Switch` controls.
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    Overrides the default value of :attr:`flet.Switch.thumb_icon` in all descendant \
    :class:`~flet.Switch` controls.
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    Overrides the default value of :attr:`flet.Switch.track_outline_width` in all \
    descendant :class:`~flet.Switch` controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Switch.splash_radius`
    in all descendant :class:`~flet.Switch` controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of :attr:`flet.Switch.mouse_cursor` in all descendant \
    :class:`~flet.Switch` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Switch.padding` in all descendant \
    :class:`~flet.Switch` controls.
    """


@value
class DividerTheme:
    """
    Defines the visual properties of :class:`~flet.Divider`,
    :class:`~flet.VerticalDivider`,
    dividers between :class:`~flet.ListTile`s, and dividers between rows in \
    :class:`~flet.DataTable`.
    """

    color: Optional[ColorValue] = None
    """
    The color of :class:`~flet.Divider`s and :class:`~flet.VerticalDivider`s, also \
    used between :class:`~flet.ListTile`s, between rows in \
    :class:`~flet.DataTable`s, and \
    so forth.
    """

    thickness: Optional[Number] = None
    """
    The thickness of the line drawn within the divider.
    """

    space: Optional[Number] = None
    """
    The :class:`~flet.Divider`'s height or the :class:`~flet.VerticalDivider`'s width.

    This represents the amount of horizontal or vertical space the divider takes up.
    """

    leading_indent: Optional[Number] = None
    """
    The amount of empty space at the leading edge of :class:`~flet.Divider` or top \
    edge of \
    :class:`~flet.VerticalDivider`.
    """

    trailing_indent: Optional[Number] = None
    """
    The amount of empty space at the trailing edge of :class:`~flet.Divider` or bottom \
    edge of :class:`~flet.VerticalDivider`.
    """


@value
class SnackBarTheme:
    """
    Defines default property values for descendant :class:`~flet.SnackBar` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.bgcolor` in all descendant \
    :class:`~flet.SnackBar` controls.
    """

    action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `text_color` of :attr:`flet.SnackBar.action` in all \
    descendant :class:`~flet.SnackBar` controls.
    """

    action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `bgcolor` of :attr:`flet.SnackBar.action` in all \
    descendant :class:`~flet.SnackBar` controls.
    """

    close_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.close_icon_color` in all \
    descendant :class:`~flet.SnackBar` controls.
    """

    disabled_action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_text_color` of \
    :attr:`flet.SnackBar.action` \
    in all descendant :class:`~flet.SnackBar` controls.
    """

    disabled_action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_color` of :attr:`flet.SnackBar.action` in \
    all descendant :class:`~flet.SnackBar` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.elevation` in all descendant \
    :class:`~flet.SnackBar` controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Used to configure the `text_style` property for the [`SnackBar.content`] control.
    """

    width: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.width` in all descendant \
    :class:`~flet.SnackBar` controls.
    """

    show_close_icon: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.show_close_icon` in all \
    descendant :class:`~flet.SnackBar` controls.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.dismiss_direction` in all \
    descendant :class:`~flet.SnackBar` controls.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.behavior` in all descendant \
    :class:`~flet.SnackBar` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.shape` in all descendant \
    :class:`~flet.SnackBar` controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.SnackBar.margin`.

    This value is only used when behavior is SnackBarBehavior.floating.
    """

    action_overflow_threshold: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.SnackBar.action_overflow_threshold` in \
    all descendant :class:`~flet.SnackBar` controls.
    """


@value
class BannerTheme:
    """
    Defines default property values for descendant :class:`~flet.Banner` controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Banner.bgcolor` in all descendant \
    :class:`~flet.Banner` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Banner.shadow_color` in all descendant \
    :class:`~flet.Banner` controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.Banner.divider_color`
    in all descendant :class:`~flet.Banner` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Banner.content_padding` in all \
    descendant \
    :class:`~flet.Banner` controls.
    """

    leading_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.Banner.leading_padding` in all \
    descendant \
    :class:`~flet.Banner` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.Banner.elevation` in all descendant \
    :class:`~flet.Banner` controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.Banner.content_text_style` in all \
    descendant :class:`~flet.Banner` controls.
    """


@value
class DatePickerTheme:
    """
    Customizes the appearance of :class:`~flet.DatePicker` controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color of the surface in all descendant \
    :class:`~flet.DatePicker` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default shadow color in all descendant :class:`~flet.DatePicker` \
    controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default color used to paint the divider in all descendant \
    :class:`~flet.DatePicker` controls.
    """

    header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the header's default background fill color.

    The :class:`~flet.DatePicker`'s header displays the currently selected date.
    """

    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the \
    [`DatePicker.current_date`].[flet.DatePicker.current_date] label in the grid of \
    the :class:`~flet.DatePicker`.
    """

    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the day labels in the \
    grid of the :class:`~flet.DatePicker`.
    """

    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a day \
    in the grid is focused, hovered, or pressed.
    """

    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the day labels in the grid of the \
    :class:`~flet.DatePicker`.

    This will be used instead of the color provided in
    :attr:`flet.DatePickerTheme.day_text_style`.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :class:`~flet.DatePicker` elevation.
    """

    range_picker_elevation: Optional[Number] = None
    """
    Overrides the default elevation of the full screen DateRangePicker (TBD).
    """

    day_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for each individual day label in the grid of \
    the :class:`~flet.DatePicker`.

    The color in :attr:`flet.DatePickerTheme.day_text_style` is not
    used, :attr:`flet.DatePickerTheme.day_foreground_color` is used instead.
    """

    weekday_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the row of weekday labels at the top of \
    the :class:`~flet.DatePicker` grid.
    """

    year_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used to paint each of the year entries in the \
    year selector of the :class:`~flet.DatePicker`.

    The color of the :attr:`flet.DatePickerTheme.year_text_style` is not used,
    :attr:`flet.DatePickerTheme.year_foreground_color` is used instead.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :class:`~flet.DatePicker` shape.

    If elevation is greater than zero then a shadow is shown and the shadow's shape
    mirrors the shape of the dialog.
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the cancel button of a :class:`~flet.DatePicker`.
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the confirm (OK) button of a \
    :class:`~flet.DatePicker`.
    """

    header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the header's default color used for text labels and icons.

    The dialog's header displays the currently selected date.

    This is used instead of the color property of
    :attr:`flet.DatePickerTheme.header_headline_text_style`
    and :attr:`flet.DatePickerTheme.header_help_text_style`.
    """

    header_headline_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default headline text style.

    The dialog's header displays the currently selected date.

    The color of the :attr:`flet.DatePickerTheme.header_headline_text_style`
    is not used, :attr:`flet.DatePickerTheme.header_foreground_color` is used instead.
    """

    header_help_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default help text style.

    The help text (also referred to as "supporting text" in the Material spec) is
    usually a prompt to the user at the top of the header (i.e. 'Select date').

    The color of the `header_help_style` is not used,
    :attr:`flet.DatePickerTheme.header_foreground_color` is used instead.
    """

    range_picker_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color for :class:`~flet.DateRangePicker`.
    """

    range_picker_header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background fill color for :class:`~flet.DateRangePicker`.

    The dialog's header displays the currently selected date range.
    """

    range_picker_header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the default color used for text labels and icons in the header of a full \
    screen :class:`~flet.DateRangePicker`.

    The dialog's header displays the currently selected date range.

    This is used instead of any colors provided by
    `range_picker_header_headline_text_style` or
    `range_picker_header_help_text_style`.
    """

    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the :attr:`flet.DatePicker.current_date` \
    label in the grid of the dialog's CalendarDatePicker and the corresponding year in \
    the dialog's YearPicker.

    This will be used instead of the color provided in
    :attr:`flet.DatePickerTheme.day_text_style`.
    """

    range_picker_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default overall shape of a full screen DateRangePicker (TBD).

    If elevation is greater than zero then a shadow is shown and the shadow's shape
    mirrors the shape of the dialog.
    """

    range_picker_header_help_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the help text of the header of a full \
    screen DateRangePicker (TBD).

    The help text (also referred to as "supporting text" in the Material spec) is
    usually a prompt to the user at the top of the header (i.e. 'Select date').

    The color of the `range_picker_header_help_text_style` is not used,
    `range_picker_header_foreground_color` is used instead.
    """

    range_picker_header_headline_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the headline text in the header of a \
    full screen :class:`~flet.DateRangePicker`.

    The dialog's header displays the currently selected date range.

    The color of `range_picker_header_headline_text_style` is not used,
    `range_picker_header_foreground_color` is used instead.
    """

    range_selection_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color used to paint days selected between the \
    start and end dates in a :class:`~flet.DateRangePicker`.
    """

    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a \
    date in the selected range of a :class:`~flet.DateRangePicker` is focused, \
    hovered, or \
    pressed.
    """

    today_border_side: Optional[BorderSide] = None
    """
    Overrides the border used to paint the :attr:`flet.DatePicker.current_date` label \
    in \
    the grid of the :class:`~flet.DatePicker`.

    The border side's [`BorderSide.color`] is not used,
    :attr:`flet.DatePickerTheme.today_foreground_color` is used instead.
    """

    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the year labels in the \
    year selector of the of the :class:`~flet.DatePicker`.
    """

    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the year labels in the year selector of \
    the date picker.

    This will be used instead of the color provided in
    :attr:`flet.DatePickerTheme.year_text_style`.
    """

    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a \
    year in the year selector is focused, hovered, or pressed.
    """

    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    Overrides the default shape used to paint the shape decoration of the day labels \
    in the grid of the :class:`~flet.DatePicker`.

    If the selected day is the current day, the provided shape with the value of
    :attr:`flet.DatePickerTheme.today_bgcolor` is used to
    paint the shape decoration of the day label and the value of
    :attr:`flet.DatePickerTheme.today_border_side` and
    :attr:`flet.DatePickerTheme.today_foreground_color`
    is used to paint the border.

    If the selected day is not the current day, the provided shape with the value of
    :attr:`flet.DatePickerTheme.day_bgcolor` is used to paint
    the shape decoration of the day label.
    """


@value
class TimePickerTheme:
    """
    Customizes the appearance of :class:`~flet.TimePicker` controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of a :class:`~flet.TimePicker`.

    If this is null, the time picker defaults to the overall theme's
    :attr:`flet.ColorScheme.surface_container_high`.
    """

    day_period_color: Optional[ColorValue] = None
    """
    The background color of the AM/PM toggle.
    """

    day_period_text_color: Optional[ColorValue] = None
    """
    The color of the day period text that represents AM/PM.
    """

    dial_bgcolor: Optional[ColorValue] = None
    """
    The background color of the time picker dial when the entry mode is \
    :attr:`flet.TimePickerEntryMode.DIAL` or :attr:`flet.TimePickerEntryMode.DIAL_ONLY`.
    """

    dial_hand_color: Optional[ColorValue] = None
    """
    The color of the time picker dial's hand when the entry mode is \
    :attr:`flet.TimePickerEntryMode.DIAL` or :attr:`flet.TimePickerEntryMode.DIAL_ONLY`.
    """

    dial_text_color: Optional[ColorValue] = None
    """
    The color of the dial text that represents specific hours and minutes.
    """

    entry_mode_icon_color: Optional[ColorValue] = None
    """
    The color of the entry mode :class:`~flet.IconButton`.
    """

    hour_minute_color: Optional[ColorValue] = None
    """
    The background color of the hour and minute header segments.
    """

    hour_minute_text_color: Optional[ColorValue] = None
    """
    The color of the header text that represents hours and minutes.
    """

    day_period_button_style: Optional[ButtonStyle] = None
    """
    The style of the AM/PM toggle control of a :class:`~flet.TimePicker`.
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    The style of the cancel button of a :class:`~flet.TimePicker`.
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    The style of the confirm (OK) button of a :class:`~flet.TimePicker`.
    """

    day_period_text_style: Optional[TextStyle] = None
    """
    Used to configure the :class:`~flet.TextStyle` for the AM/PM toggle control.

    If this is null, the time picker defaults to the overall theme's
    :attr:`flet.TextTheme.title_medium`.
    """

    dial_text_style: Optional[TextStyle] = None
    """
    The :class:`~flet.TextStyle` for the numbers on the time selection dial.
    """

    help_text_style: Optional[TextStyle] = None
    """
    Used to configure the :class:`~flet.TextStyle` for the helper text in the \
    header.
    """

    hour_minute_text_style: Optional[TextStyle] = None
    """
    Used to configure the :class:`~flet.TextStyle` for the hour/minute controls.
    """

    elevation: Optional[Number] = None
    """
    The Material elevation for the time picker dialog.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the Dialog that the time picker is presented in.
    """

    day_period_shape: Optional[OutlinedBorder] = None
    """
    The shape of the day period that the :class:`~flet.TimePicker` uses.
    """

    hour_minute_shape: Optional[OutlinedBorder] = None
    """
    The shape of the hour and minute controls that the :class:`~flet.TimePicker`
    uses.
    """

    day_period_border_side: Optional[BorderSide] = None
    """
    The color and weight of the day period's outline.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the time picker dialog when the entry mode is \
    :attr:`flet.TimePickerEntryMode.DIAL` or :attr:`flet.TimePickerEntryMode.DIAL_ONLY`.
    """

    time_selector_separator_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of the time selector separator between the hour and minute controls.
    """

    time_selector_separator_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Used to configure the text style for the time selector separator between the hour \
    and minute controls.
    """


@value
class DropdownTheme:
    """
    Customizes the appearance of :class:`~flet.Dropdown` across the app.
    """

    menu_style: Optional[MenuStyle] = None
    """
    Overrides the default value for :attr:`flet.Dropdown.menu_style`.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.Dropdown.text_style`.
    """


@value
class ListTileTheme:
    """
    Customizes the appearance of descendant :class:`~flet.ListTile` controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.icon_color`.
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.text_color`.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.bgcolor`.
    """

    selected_tile_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.selected_tile_color`.
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.selected_color`.
    """

    is_three_line: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.ListTile.is_three_line`.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.ListTile.enable_feedback`.
    """

    dense: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.ListTile.dense`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for :attr:`flet.ListTile.shape`.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value for :attr:`flet.ListTile.visual_density`.
    """

    content_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.content_padding`.
    """

    min_vertical_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.ListTile.min_vertical_padding`.
    """

    horizontal_spacing: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ListTile.horizontal_spacing`.
    """

    min_leading_width: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ListTile.min_leading_width`.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.ListTile.title_text_style`.
    """

    subtitle_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.ListTile.subtitle_text_style`.
    """

    leading_and_trailing_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for \
    :attr:`flet.ListTile.leading_and_trailing_text_style`.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for :attr:`flet.ListTile.mouse_cursor`.
    """

    min_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ListTile.min_height`.
    """

    affinity: Optional[TileAffinity] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.affinity`.
    """

    style: Optional[ListTileStyle] = None
    """
    Overrides the default value for :attr:`flet.ListTile.style`.
    """

    title_alignment: Optional[ListTileTitleAlignment] = None
    """
    Overrides the default value for :attr:`flet.ListTile.title_alignment`.
    """


@value
class TooltipTheme:
    """
    Customizes the appearance of descendant :class:`~flet.Tooltip` controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.text_style`.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.enable_feedback`.
    """

    exclude_from_semantics: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.exclude_from_semantics`.
    """

    prefer_below: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.prefer_below`.
    """

    vertical_offset: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.vertical_offset`.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.padding`.
    """

    wait_duration: Optional[DurationValue] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.wait_duration`.
    """

    exit_duration: Optional[DurationValue] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.exit_duration`.
    """

    show_duration: Optional[DurationValue] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.show_duration`.
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.margin`.
    """

    trigger_mode: Optional[TooltipTriggerMode] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.trigger_mode`.
    """

    decoration: Optional[BoxDecoration] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.decoration`.
    """

    text_align: Optional[TextAlign] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.text_align`.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for :attr:`flet.Tooltip.size_constraints`.
    """


@value
class ExpansionTileTheme:
    """
    Customizes the appearance of descendant :class:`~flet.ExpansionTile`
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.bgcolor`.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.icon_color`.
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.text_color`.
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.collapsed_bgcolor`.
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.collapsed_icon_color`.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.clip_behavior`.
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.collapsed_text_color`.
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.tile_padding`.
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.expanded_alignment`.
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.controls_padding`.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.shape`.
    """

    collapsed_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.collapsed_shape`.
    """

    animation_style: Optional[AnimationStyle] = None
    """
    Overrides the default value for :attr:`flet.ExpansionTile.animation_style`.
    """


@value
class SliderTheme:
    """
    Customizes the appearance of descendant :class:`~flet.Slider` controls.
    """

    active_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.active_color`.
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.inactive_color`.
    """

    thumb_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.thumb_color`.
    """

    overlay_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.overlay_color`.
    """

    value_indicator_color: Optional[ColorValue] = None
    """
    The color given to the :class:`~flet.Slider`'s value indicator to draw itself with.
    """

    disabled_thumb_color: Optional[ColorValue] = None
    """
    The color given to the thumb to draw itself with when the :class:`~flet.Slider`
    is disabled.
    """

    value_indicator_text_style: Optional[TextStyle] = None
    """
    The :class:`~flet.TextStyle` for the text on the value indicator.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for :attr:`flet.Slider.mouse_cursor`.
    """

    active_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the \
    :attr:`flet.Slider.min` position and the current thumb position.
    """

    disabled_active_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb \
    osition and the :attr:`flet.Slider.max` position when the :class:`~flet.Slider` \
    is disabled.
    """

    disabled_active_track_color: Optional[ColorValue] = None
    """
    The color of the :class:`~flet.Slider` track between the :attr:`flet.Slider.min` \
    position and the current thumb position when the :class:`~flet.Slider` is disabled.
    """

    disabled_inactive_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb \
    position and the :attr:`flet.Slider.max` position when the :class:`~flet.Slider` \
    is disabled.
    """

    disabled_inactive_track_color: Optional[ColorValue] = None
    """
    The color of the :class:`~flet.Slider` track between the current thumb position \
    and \
    the :attr:`flet.Slider.max` position when the :class:`~flet.Slider` is disabled.
    """

    disabled_secondary_active_track_color: Optional[ColorValue] = None
    """
    The color of the :class:`~flet.Slider` track between the current thumb position \
    and \
    the :attr:`flet.Slider.secondary_track_value` position \
    when the :class:`~flet.Slider` is disabled.
    """

    inactive_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb \
    position and the :attr:`flet.Slider.max` position.
    """

    overlapping_shape_stroke_color: Optional[ColorValue] = None
    """
    The color given to the perimeter of the top range thumbs of a \
    :class:`~flet.RangeSlider` when the thumbs are overlapping and the top range \
    value indicator when the value indicators are overlapping.
    """

    min_thumb_separation: Optional[Number] = None
    """
    Limits the thumb's separation distance.

    Use this only if you want to control the visual appearance of the thumbs in terms
    of a logical pixel value. This can be done when you want a specific look for thumbs
    when they are close together. To limit with the real values, rather than logical
    pixels, the values can be restricted by the parent.
    """

    secondary_active_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.secondary_active_color`.
    """

    track_height: Optional[Number] = None
    """
    The height of the :class:`~flet.Slider` track.
    """

    value_indicator_stroke_color: Optional[ColorValue] = None
    """
    The color given to the value indicator shape stroke.
    """

    interaction: Optional[SliderInteraction] = None
    """
    Overrides the default value for :attr:`flet.Slider.interaction`.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.Slider.padding`.
    """

    track_gap: Optional[Number] = None
    """
    The size of the gap between the active and inactive tracks of the gapped slider \
    track shape.
    """

    thumb_size: Optional[ControlStateValue[Size]] = None
    """
    The size of the handle thumb shape thumb.
    """

    year_2023: bool = False
    """
    Overrides the default value for :attr:`flet.Slider.year_2023`.
    """


@value
class ProgressIndicatorTheme:
    """
    Customizes the appearance of progress indicators (:class:`~flet.ProgressBar`, \
    :class:`~flet.ProgressRing`) across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default values for :attr:`flet.ProgressBar.color` and \
    :attr:`flet.ProgressRing.color`.
    """

    circular_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.bgcolor`.
    """

    linear_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ProgressBar.bgcolor`.
    """

    refresh_bgcolor: Optional[ColorValue] = None
    """
    Background color of that fills the circle under the RefreshIndicator (TBD).
    """

    linear_min_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ProgressBar.bar_height`.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for :attr:`flet.ProgressBar.border_radius`.
    """

    track_gap: Optional[Number] = None
    """
    Overrides the default values for :attr:`flet.ProgressBar.track_gap` and \
    :attr:`flet.ProgressRing.track_gap`.
    """

    circular_track_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.padding`.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.size_constraints`.
    """

    stop_indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.ProgressBar.stop_indicator_color`.
    """

    stop_indicator_radius: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ProgressBar.stop_indicator_radius`.
    """

    stroke_align: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.stroke_align`.
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.stroke_cap`.
    """

    stroke_width: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.ProgressRing.stroke_width`.
    """

    year_2023: bool = False
    """
    Overrides the default values for :attr:`flet.ProgressBar.year_2023` and \
    :attr:`flet.ProgressRing.year_2023`.
    """


@value
class PopupMenuTheme:
    """
    Customizes the appearance of :class:`~flet.PopupMenuButton` across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.bgcolor` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.shadow_color` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.icon_color` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuItem.label_text_style`
    in all descendant :class:`~flet.PopupMenuItem` controls.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.enable_feedback` in all \
    descendant :class:`~flet.PopupMenuButton` controls
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.elevation` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    icon_size: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.icon_size` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.shape` in all \
    descendant \
    :class:`~flet.PopupMenuButton` controls.
    """

    menu_position: Optional[PopupMenuPosition] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.menu_position` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuItem.mouse_cursor` in all \
    descendant :class:`~flet.PopupMenuItem` controls.
    """

    menu_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.PopupMenuButton.menu_padding` in all \
    descendant :class:`~flet.PopupMenuButton` controls.
    """


@value
class SearchBarTheme:
    """
    Customizes the appearance of :class:`~flet.SearchBar` controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_bgcolor` in all \
    descendant \
    :class:`~flet.SearchBar` controls.
    """

    text_capitalization: Optional[TextCapitalization] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.capitalization` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_shadow_color` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_overlay_color` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_elevation` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_text_style` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    hint_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_hint_text_style` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_shape` in all descendant \
    :class:`~flet.SearchBar` controls.
    """

    padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_padding` in all \
    descendant \
    :class:`~flet.SearchBar` controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_size_constraints` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.bar_border_side` in all \
    descendant :class:`~flet.SearchBar` controls.
    """


@value
class SearchViewTheme:
    """
    Customizes the appearance of :class:`~flet.SearchBar` controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_bgcolor` in all \
    descendant \
    :class:`~flet.SearchBar` controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.divider_color` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_elevation` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    header_hint_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_hint_text_style` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    header_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_header_text_style` in \
    all \
    descendant :class:`~flet.SearchBar` controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_shape` in all descendant \
    :class:`~flet.SearchBar` controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_side` in all descendant \
    :class:`~flet.SearchBar` controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_size_constraints` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    header_height: Optional[Number] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_header_height` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_padding` in all \
    descendant \
    :class:`~flet.SearchBar` controls.
    """

    bar_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.view_bar_padding` in all \
    descendant :class:`~flet.SearchBar` controls.
    """

    shrink_wrap: Optional[bool] = None
    """
    Overrides the default value of :attr:`flet.SearchBar.shrink_wrap` in all \
    descendant \
    :class:`~flet.SearchBar` controls.
    """


@value
class NavigationDrawerTheme:
    """
    Customizes the appearance of descendant :class:`~flet.NavigationDrawer`
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationDrawer.bgcolor`.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationDrawer.shadow_color`.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationDrawer.indicator_color`.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.NavigationDrawer.elevation`.
    """

    tile_height: Optional[Number] = None
    """
    Overrides the default height of :class:`~flet.NavigationDrawerDestination`.
    """

    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The style to merge with the default text style for \
    :class:`~flet.NavigationDrawerDestination` labels.

    Can be used to specify a different style when the label is selected.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for :attr:`flet.NavigationDrawer.indicator_shape`.
    """

    indicator_size: Optional[Size] = None
    """
    Overrides the default size of the :class:`~flet.NavigationDrawer`'s selection \
    indicator.
    """

    icon_theme: Optional[ControlStateValue["IconTheme"]] = None
    """
    The theme to merge with the default icon theme for \
    :class:`~flet.NavigationDestination` icons.

    Can be used to specify a different icon theme when the icon is selected.
    """


@value
class NavigationBarTheme:
    """
    Customizes the appearance of :class:`~flet.NavigationBar`
    controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.bgcolor`.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.shadow_color`.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.indicator_color`.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.overlay_color`.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.elevation`.
    """

    height: Optional[Number] = None
    """
    Overrides the default value for :class:`~flet.NavigationBar` height.
    """

    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The style to merge with the default text style for \
    :class:`~flet.NavigationBarDestination` labels.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.indicator_shape`.
    """

    label_behavior: Optional[NavigationBarLabelBehavior] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.label_behavior`.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for :attr:`flet.NavigationBar.label_padding`.
    """


@value
class SegmentedButtonTheme:
    """
    Customizes the appearance of :class:`~flet.SegmentedButton`
    controls across the app.
    """

    selected_icon: Optional[IconData] = None
    """
    Overrides the default value for :attr:`flet.SegmentedButton.selected_icon`.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value for :attr:`flet.SegmentedButton.style`.
    """


@value
class IconTheme:
    """
    Customizes the appearance of :class:`~flet.Icon` controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value for :attr:`flet.Icon.color`.
    """

    apply_text_scaling: Optional[bool] = None
    """
    Overrides the default value for :attr:`flet.Icon.apply_text_scaling`.
    """

    fill: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Icon.fill`.
    """

    opacity: Optional[Number] = None
    """
    An opacity to apply to both explicit and default icon colors.
    """

    size: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Icon.size`.
    """

    optical_size: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Icon.optical_size`.
    """

    grade: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Icon.grade`.
    """

    weight: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.Icon.weight`.
    """

    shadows: Optional[BoxShadowValue] = None
    """
    Overrides the default value for :attr:`flet.Icon.shadows`.
    """


@value
class DataTableTheme:
    """
    Customizes the appearance of :class:`~flet.DataTable` controls across the app.
    """

    checkbox_horizontal_margin: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.checkbox_horizontal_margin`.
    """

    column_spacing: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.column_spacing`.
    """

    data_row_max_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.data_row_max_height`.
    """

    data_row_min_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.data_row_min_height`.
    """

    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for :attr:`flet.DataTable.data_row_color`.
    """

    data_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.DataTable.data_text_style`.
    """

    divider_thickness: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.divider_thickness`.
    """

    horizontal_margin: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.horizontal_margin`.
    """

    heading_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for :attr:`flet.DataTable.heading_text_style`.
    """

    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for :attr:`flet.DataTable.heading_row_color`.
    """

    heading_row_height: Optional[Number] = None
    """
    Overrides the default value for :attr:`flet.DataTable.heading_row_height`.
    """

    data_row_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for :class:`~flet.DataRow` mouse cursor.
    """

    decoration: Optional[BoxDecoration] = None
    """
    Overrides the default value for :class:`~flet.DataTable` decoration.
    """

    heading_row_alignment: Optional[MainAxisAlignment] = None
    """
    Overrides the default value for :attr:`flet.DataColumn.heading_row_alignment`.
    """

    heading_cell_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for :class:`~flet.DataColumn` mouse cursor.
    """


@value
class Theme:
    """
    Customizes the overall appearance of the application.
    """

    color_scheme_seed: Optional[ColorValue] = None
    """
    Overrides the default color scheme seed used to generate
    :class:`~flet.ColorScheme`.
    The default color is blue.
    """

    font_family: Optional[str] = None
    """
    Overrides a default font for the app.
    """

    use_material3: Optional[bool] = None
    """
    A temporary flag that can be used to opt-out of Material 3 features.
    """

    appbar_theme: Optional[AppBarTheme] = None
    badge_theme: Optional[BadgeTheme] = None
    banner_theme: Optional[BannerTheme] = None
    bottom_appbar_theme: Optional[BottomAppBarTheme] = None
    bottom_sheet_theme: Optional[BottomSheetTheme] = None
    card_theme: Optional[CardTheme] = None
    checkbox_theme: Optional[CheckboxTheme] = None
    chip_theme: Optional[ChipTheme] = None
    """
    Customizes the appearance of :class:`~flet.Chip` across the app.
    """

    color_scheme: Optional[ColorScheme] = None
    """
    Overrides the default :class:`~flet.ColorScheme` used for the application.
    """

    data_table_theme: Optional[DataTableTheme] = None
    """
    Customizes the appearance of :class:`~flet.DataTable` across the app.
    """

    date_picker_theme: Optional[DatePickerTheme] = None
    """
    Customizes the appearance of :class:`~flet.DatePicker` across the app.
    """

    dialog_theme: Optional[DialogTheme] = None
    """
    Customizes the appearance of :class:`~flet.AlertDialog` across the app.
    """

    divider_theme: Optional[DividerTheme] = None
    """
    Defines the visual properties of :class:`~flet.Divider`, \
    :class:`~flet.VerticalDivider`, \
    dividers between :class:`~flet.ListTile`s, and dividers between rows in \
    :class:`~flet.DataTable`.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default color of dividers used in :class:`~flet.Divider`, \
    :class:`~flet.VerticalDivider`, dividers between :class:`~flet.ListTile`s, and \
    dividers \
    between rows in :class:`~flet.DataTable`.
    """

    dropdown_theme: Optional[DropdownTheme] = None
    """
    Customizes the appearance of :class:`~flet.Dropdown` across the app.
    """

    button_theme: Optional[ButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.Button` across the app.
    """

    outlined_button_theme: Optional[OutlinedButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.OutlinedButton` across the app.
    """

    text_button_theme: Optional[TextButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.TextButton` across the app.
    """

    filled_button_theme: Optional[FilledButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.FilledButton` across the app.
    """

    icon_button_theme: Optional[IconButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.IconButton` across the app.
    """

    expansion_tile_theme: Optional[ExpansionTileTheme] = None
    """
    Customizes the appearance of :class:`~flet.ExpansionTile` across the app.
    """

    floating_action_button_theme: Optional[FloatingActionButtonTheme] = None
    """
    Customizes the appearance of :class:`~flet.FloatingActionButton`
    across the app.
    """

    icon_theme: Optional[IconTheme] = None
    """
    Customizes the appearance of :class:`~flet.Icon` across the app.
    """

    list_tile_theme: Optional[ListTileTheme] = None
    """
    Customizes the appearance of :class:`~flet.ListTile` across the app.
    """

    navigation_bar_theme: Optional[NavigationBarTheme] = None
    navigation_drawer_theme: Optional[NavigationDrawerTheme] = None
    navigation_rail_theme: Optional[NavigationRailTheme] = None
    page_transitions: PageTransitionsTheme = field(default_factory=PageTransitionsTheme)
    popup_menu_theme: Optional[PopupMenuTheme] = None
    splash_color: Optional[ColorValue] = None
    highlight_color: Optional[ColorValue] = None
    hover_color: Optional[ColorValue] = None
    focus_color: Optional[ColorValue] = None
    unselected_control_color: Optional[ColorValue] = None
    disabled_color: Optional[ColorValue] = None
    canvas_color: Optional[ColorValue] = None
    scaffold_bgcolor: Optional[ColorValue] = None
    card_bgcolor: Optional[ColorValue] = None
    hint_color: Optional[ColorValue] = None
    secondary_header_color: Optional[ColorValue] = None
    primary_text_theme: Optional[TextTheme] = None
    progress_indicator_theme: Optional[ProgressIndicatorTheme] = None
    radio_theme: Optional[RadioTheme] = None
    scrollbar_theme: Optional[ScrollbarTheme] = None
    search_bar_theme: Optional[SearchBarTheme] = None
    search_view_theme: Optional[SearchViewTheme] = None
    segmented_button_theme: Optional[SegmentedButtonTheme] = None
    slider_theme: Optional[SliderTheme] = None
    snackbar_theme: Optional[SnackBarTheme] = None
    switch_theme: Optional[SwitchTheme] = None
    system_overlay_style: Optional[SystemOverlayStyle] = None
    tab_bar_theme: Optional[TabBarTheme] = None
    text_theme: Optional[TextTheme] = None
    time_picker_theme: Optional[TimePickerTheme] = None
    tooltip_theme: Optional[TooltipTheme] = None
    visual_density: Optional[VisualDensity] = None
