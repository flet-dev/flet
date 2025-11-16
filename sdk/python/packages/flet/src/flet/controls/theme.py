from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.animation import AnimationStyle
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
    NONE = "none"
    FADE_UPWARDS = "fadeUpwards"
    OPEN_UPWARDS = "openUpwards"
    ZOOM = "zoom"
    CUPERTINO = "cupertino"
    PREDICTIVE = "predictive"
    FADE_FORWARDS = "fadeForwards"


@dataclass
class PageTransitionsTheme:
    android: Optional[PageTransitionTheme] = None
    ios: Optional[PageTransitionTheme] = None
    linux: Optional[PageTransitionTheme] = None
    macos: Optional[PageTransitionTheme] = None
    windows: Optional[PageTransitionTheme] = None


@dataclass
class ColorScheme:
    """
    A set of more than 40 colors based on the [Material spec](https://m3.material.io/styles/color/the-color-system/color-roles)
    that can be used to configure the color properties of most components.
    Read more about color schemes in [here](https://api.flutter.dev/flutter/material/ColorScheme-class.html).
    """

    primary: Optional[ColorValue] = None
    """
    The color displayed most frequently across your app's screens and components.
    """

    on_primary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on [`primary`][(c).].
    """

    primary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than [`primary`][(c).].
    """

    on_primary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`primary_container`][(c).].
    """

    secondary: Optional[ColorValue] = None
    """
    An accent color used for less prominent components in the UI, such as filter
    [`Chip`][flet.]s, while expanding the opportunity for color expression.
    """

    on_secondary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on [`secondary`][(c).].
    """

    secondary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than [`secondary`][(c).].
    """

    on_secondary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`secondary_container`][(c).].
    """

    tertiary: Optional[ColorValue] = None
    """
    A color used as a contrasting accent that can balance [`primary`][(c).] and
    [`secondary`][(c).] colors or bring heightened attention to an element, such as
    an input field.
    """

    on_tertiary: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on [`tertiary`][(c).].
    """

    tertiary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than [`tertiary`][(c).].
    """

    on_tertiary_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`tertiary_container`][(c).].
    """

    error: Optional[ColorValue] = None
    """
    The color to use for input validation errors,
    e.g. for [`FormFieldControl.error`][flet.].
    """

    on_error: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on [`error`][(c).].
    """

    error_container: Optional[ColorValue] = None
    """
    A color used for error elements needing less emphasis than [`error`][(c).].
    """

    on_error_container: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`error_container`][(c).].
    """

    surface: Optional[ColorValue] = None
    """
    The background color for widgets like [`Card`][flet.].
    """

    on_surface: Optional[ColorValue] = field(default=None, metadata={"event": False})
    """
    A color that's clearly legible when drawn on [`surface`][(c).].
    """

    on_surface_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`surface_container_highest`][(c).].
    """

    outline: Optional[ColorValue] = None
    """
    A utility color that creates boundaries and emphasis to improve usability.
    """

    outline_variant: Optional[ColorValue] = None
    """
    A utility color that creates boundaries for decorative elements when a 3:1 contrast
    isn’t required, such as for dividers or decorative elements.
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
    A surface color used for displaying the reverse of what’s seen in the surrounding
    UI, for example in a [`SnackBar`][flet.] to bring attention to an alert.
    """

    on_inverse_surface: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that's clearly legible when drawn on [`inverse_surface`][(c).].
    """

    inverse_primary: Optional[ColorValue] = None
    """
    An accent color used for displaying a highlight color on [`inverse_surface`][(c).]
    backgrounds, like button text in a [`SnackBar`][flet.].
    """

    surface_tint: Optional[ColorValue] = None
    """
    A color used as an overlay on a surface color to indicate a component's elevation.
    """

    on_primary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having
    [`primary_fixed`][(c).] color.
    """

    on_secondary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having
    [`secondary_fixed`][(c).] color.
    """

    on_tertiary_fixed: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that is used for text and icons that exist on top of elements having
    [`tertiary_fixed`][(c).] color.
    """

    on_primary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than
    [`on_primary_fixed`][(c).].
    """

    on_secondary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than
    [`on_secondary_fixed`][(c).].
    """

    on_tertiary_fixed_variant: Optional[ColorValue] = field(
        default=None, metadata={"event": False}
    )
    """
    A color that provides a lower-emphasis option for text and icons than
    [`on_tertiary_fixed`][(c).].
    """

    primary_fixed: Optional[ColorValue] = None
    """
    A substitute for [`primary_container`][(c).] that's the
    same color for the dark and light themes.
    """

    secondary_fixed: Optional[ColorValue] = None
    """
    A substitute for [`secondary_container`][(c).] that's the
    same color for the dark and light themes.
    """

    tertiary_fixed: Optional[ColorValue] = None
    """
    A substitute for [`tertiary_container`][(c).] that's the
    same color for dark and light themes.
    """

    primary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than [`primary_fixed`][(c).].
    """

    secondary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than [`secondary_fixed`][(c).].
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
    A surface container color with the darkest tone. It is used to create the most
    emphasis against the surface.
    """

    surface_container_low: Optional[ColorValue] = None
    """
    A surface container color with a lighter tone that creates less emphasis than
    `surface_container` but more emphasis than [`surface_container_lowest`][(c).].
    """

    surface_container_lowest: Optional[ColorValue] = None
    """
    A surface container color with the lightest tone and the least emphasis relative to
    the surface.
    """

    surface_dim: Optional[ColorValue] = None
    """
    A color that's always darkest in the dark or light theme.
    """

    tertiary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than [`tertiary_fixed`][(c).].
    """


@dataclass
class TextTheme:
    """
    Customizes [`Text`][flet.] styles.

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
    Largest of the display styles. As the largest text on the screen, display styles
    are reserved for short, important text or numerals. They work best on large screens.
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
    Largest of the label styles. Label styles are smaller, utilitarian styles, used for
    areas of the UI such as text inside of components or very small supporting text in
    the content body, like captions. Used for text on
    [`Button`][flet.], [`TextButton`][flet.] and
    [`OutlinedButton`][flet.].
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
    Largest of the title styles. Titles are smaller than headline styles and should be
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


@dataclass
class ScrollbarTheme:
    """
    Customizes the colors, thickness, and shape of scrollbars across the app.
    """

    thumb_visibility: Optional[ControlStateValue[bool]] = None
    """
    Indicates that the scrollbar thumb should be visible, even when a scroll is not
    underway. When `False`, the scrollbar will be shown during scrolling and will fade
    out otherwise. When `True`, the scrollbar will always be visible and never fade
    out. Property value could be either a single boolean value or a dictionary with
    `ft.ControlState` as keys and boolean as values.
    """

    thickness: Optional[ControlStateValue[Optional[Number]]] = None
    """
    The thickness of the scrollbar in the cross axis of the scrollable. Property value
    could be either a single float value or a dictionary with `ft.ControlState` as keys
    and float as values.
    """

    track_visibility: Optional[ControlStateValue[bool]] = None
    """
    Indicates that the scrollbar track should be visible. When `True`, the scrollbar
    track will always be visible so long as the thumb is visible. If the scrollbar
    thumb is not visible, the track will not be visible either. Defaults to `False`
    when `None`. If this property is `None`, then `ScrollbarTheme.track_visibility` of
    `Theme.scrollbar_theme` is used. If that is also `None`, the default value is
    `False`. Property value could be either a single boolean value or a dictionary with
    `ft.ControlState` as keys and boolean as values.
    """

    radius: Optional[Number] = None
    """
    The Radius of the scrollbar thumb's rounded rectangle corners.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar thumb. The value is either a single
    color string or `ft.ControlState` dictionary.
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar track. The value is either a single
    color string or `ft.ControlState` dictionary.
    """

    track_border_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default Color of the Scrollbar track border. The value is either a
    single color string or `ft.ControlState` dictionary.
    """

    cross_axis_margin: Optional[Number] = None
    """
    Distance from the scrollbar thumb to the nearest cross axis edge in logical pixels.
    The scrollbar track consumes this space. Must not be null and defaults to 0.
    """

    main_axis_margin: Optional[Number] = None
    """
    Distance from the scrollbar thumb's start and end to the edge of the viewport in
    logical pixels. It affects the amount of available paint area. The scrollbar track
    consumes this space. Mustn't be null and defaults to 0.
    """

    min_thumb_length: Optional[Number] = None
    """
    The preferred smallest size the scrollbar thumb can shrink to when the total
    scrollable extent is large, the current visible viewport is small, and the viewport
    is not overscrolled.
    """

    interactive: Optional[bool] = None
    """
    Whether the Scrollbar should be interactive and respond to dragging on the thumb,
    or tapping in the track area. When `False`, the scrollbar will not respond to
    gesture or hover events, and will allow to click through it. Defaults to `True`
    when `None`, unless on Android, which will default to `False` when `None`.
    """


@dataclass
class TabBarTheme:
    """
    Customizes the appearance of [`TabBar`][flet.] control across the app.
    """

    indicator_size: Optional[TabBarIndicatorSize] = None
    """
    Overrides the default value for [`TabBar.indicator_size`][flet.].
    """

    indicator: Optional[UnderlineTabIndicator] = None
    """
    Overrides the default value for [`TabBar.indicator`][flet.].
    """

    indicator_animation: Optional[TabIndicatorAnimation] = None
    """
    Overrides the default value for [`TabBar.indicator_animation`][flet.].
    """

    splash_border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for [`TabBar.splash_border_radius`][flet.].
    """

    tab_alignment: Optional[TabAlignment] = None
    """
    Overrides the default value for [`TabBar.tab_alignment`][flet.].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for [`TabBar.overlay_color`][flet.].
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`TabBar.divider_color`][flet.].
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`TabBar.indicator_color`][flet.].
    """

    mouse_cursor: Optional[ControlStateValue[Optional[MouseCursor]]] = None
    """
    Overrides the default value for [`TabBar.mouse_cursor`][flet.].
    """

    divider_height: Optional[Number] = None
    """
    Overrides the default value for [`TabBar.divider_height`][flet.].
    """

    label_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`TabBar.label_color`][flet.].
    """

    unselected_label_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`TabBar.unselected_label_color`][flet.].
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`TabBar.label_padding`][flet.].
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`TabBar.label_text_style`][flet.].
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`TabBar.unselected_label_text_style`][flet.].
    """


@dataclass
class SystemOverlayStyle:
    """
    Allows the customization of the mobile's system overlay (which consists of the
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
    Indicates whether the system should enforce contrast for the status bar when
    setting a transparent status bar.
    """

    enforce_system_status_bar_contrast: Optional[bool] = None
    """
    Indicates whether the system should enforce contrast for the navigation bar when
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


@dataclass
class DialogTheme:
    """
    Customizes the appearance of [`AlertDialog`][flet.] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`AlertDialog.bgcolor`][flet.] in
    all descendant [`AlertDialog`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.shadow_color`][flet.] in all descendant
    [`AlertDialog`][flet.] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Used to configure the [`IconTheme`][flet.] for the
    [`AlertDialog.icon`][flet.] control.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`AlertDialog.elevation`][flet.] in all descendant dialog
    controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`AlertDialog.shape`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of [`AlertDialog.title_text_style`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of [`AlertDialog.content_text_style`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of [`AlertDialog.alignment`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`AlertDialog.actions_padding`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of [`AlertDialog.clip_behavior`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`AlertDialog.barrier_color`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`AlertDialog.inset_padding`][flet.] in all
    descendant [`AlertDialog`][flet.] controls.
    """


@dataclass
class ButtonTheme:
    """
    Customizes the appearance of [`Button`][flet.] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of [`Button.style`][flet.] in all
    descendant [`Button`][flet.] controls.
    """


@dataclass
class OutlinedButtonTheme:
    """
    Customizes the appearance of [`OutlinedButton`][flet.] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of [`OutlinedButton.style`][flet.] in all
    descendant [`OutlinedButton`][flet.] controls.
    """


@dataclass
class TextButtonTheme:
    """
    Customizes the appearance of [`TextButton`][flet.] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of [`TextButton.style`][flet.] in all
    descendant [`TextButton`][flet.] controls.
    """


@dataclass
class FilledButtonTheme:
    """
    Customizes the appearance of [`FilledButton`][flet.] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of [`FilledButton.style`][flet.] in all
    descendant [`FilledButton`][flet.] controls.
    """


@dataclass
class IconButtonTheme:
    """
    Customizes the appearance of [`IconButton`][flet.] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of [`IconButton.style`][flet.] in all
    descendant [`IconButton`][flet.] controls.
    """


@dataclass
class BottomSheetTheme:
    """
    Customizes the appearance of [`BottomSheet`][flet.] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`BottomSheet.bgcolor`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`BottomSheet.elevation`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`BottomSheet.shape`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    show_drag_handle: Optional[bool] = None
    """
    Overrides the default value of [`BottomSheet.show_drag_handle`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of [`BottomSheet.clip_behavior`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of [`BottomSheet.size_constraints`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`BottomSheet.barrier_color`][flet.] in all
    descendant [`BottomSheet`][flet.] controls.
    """

    drag_handle_color: Optional[ColorValue] = None
    """
    Overrides the default value of drag handle color in all
    descendant [`BottomSheet`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of shadow color in all
    descendant [`BottomSheet`][flet.] controls.
    """


@dataclass
class CardTheme:
    """
    Customizes the appearance of [`Card`][flet.] across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Card.clip_behavior`][flet.] in all
    descendant [`Card`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Card.shadow_color`][flet.] in all
    descendant [`Card`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Card.elevation`][flet.] in all
    descendant [`Card`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`Card.shape`][flet.] in all
    descendant [`Card`][flet.] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of [`Card.clip_behavior`][flet.] in all
    descendant [`Card`][flet.] controls.
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value of [`Card.margin`][flet.] in all
    descendant [`Card`][flet.] controls.
    """


@dataclass
class ChipTheme:
    """
    Customizes the appearance of [`Chip`][flet.] across the app.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Chip.color`][flet.] in all descendant
    [`Chip`][flet.] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.bgcolor`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.shadow_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.selected_shadow_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    disabled_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.disabled_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.selected_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    check_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.check_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.delete_icon_color`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Chip.elevation`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    elevation_on_click: Optional[Number] = None
    """
    Overrides the default value of [`Chip.elevation_on_click`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`Chip.shape`][flet.] in all descendant
    [`Chip`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Chip.padding`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Chip.label_padding`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of [`Chip.label_text_style`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of [`Chip.border_side`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    show_checkmark: Optional[bool] = None
    """
    Overrides the default value of [`Chip.show_checkmark`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    leading_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of [`Chip.leading_size_constraints`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of [`Chip.delete_icon_size_constraints`][flet.] in all
    descendant [`Chip`][flet.] controls.
    """

    brightness: Optional[Brightness] = None
    """
    Overrides the default value for all chips which affects various base material
    color choices in the chip rendering.
    """

    # secondary_selected_color: Optional[ColorValue] = None
    # secondary_label_text_style: Optional[TextStyle] = None


@dataclass
class FloatingActionButtonTheme:
    """
    Customizes the appearance of [`FloatingActionButton`][flet.]
    across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled
    [`FloatingActionButton`][flet.]'s background.
    """

    hover_color: Optional[ColorValue] = None
    """
    The color to use for filling the button when the button has a pointer hovering over
    it.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for filling the button when the button has input focus.
    """

    foreground_color: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled
    [`FloatingActionButton`][flet.]'s foreground.
    """

    splash_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.splash_color`][flet.] in all
    descendant [`FloatingActionButton`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the unselected, enabled
    [`FloatingActionButton`][flet.]'s elevation foreground.
    """

    focus_elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this button relative to its parent when the
    button has the input focus.
    """

    hover_elevation: Optional[Number] = None
    """
    The z-coordinate at which to place this button relative to its parent when the
    button is enabled and has a pointer hovering over it.
    """

    highlight_elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the selected, enabled
    [`FloatingActionButton`][flet.]'s elevation foreground.
    """

    disabled_elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the disabled
    [`FloatingActionButton`][flet.]'s elevation foreground.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`FloatingActionButton.shape`][flet.] in all
    descendant [`FloatingActionButton`][flet.] controls.
    """

    enable_feedback: Optional[bool] = None
    """
    If specified, defines the feedback property for [`FloatingActionButton`][flet.].
    """

    extended_padding: Optional[PaddingValue] = None
    """
    The padding for a [`FloatingActionButton`][flet.]'s that has both icon and content.
    """

    text_style: Optional[TextStyle] = None
    """
    Text style merged into default text style of
    [`FloatingActionButton.content`][flet.].
    """

    icon_label_spacing: Optional[Number] = None
    """
    The spacing between the icon and the label for [`FloatingActionButton`][flet.].
    """

    extended_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of
    [`FloatingActionButton`][flet.] that has both icon and content.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of
    [`FloatingActionButton`][flet.] that has either icon or content
    and is not a mini button.
    """

    # large_size_constraints: Optional[BoxConstraints] = None
    # small_size_constraints: Optional[BoxConstraints] = None


@dataclass
class NavigationRailTheme:
    """
    Customizes the appearance of [`NavigationRail`][flet.] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the [`NavigationRail`][flet.]'s background.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`NavigationRail.indicator_color`][flet.] in all
    descendant [`NavigationRail`][flet.] controls. when
    [`NavigationRailTheme.use_indicator`][flet.]
    is true.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the [`NavigationRail`][flet.]'s
    elevation.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`NavigationRail.indicator_shape`][flet.] in all
    descendant [`NavigationRail`][flet.] controls.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`NavigationRail.unselected_label_text_style`][flet.]
    in all descendant [`NavigationRail`][flet.] controls.
    """

    selected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`NavigationRail.selected_label_text_style`][flet.]
    in all descendant [`NavigationRail`][flet.] controls.
    """

    label_type: Optional[NavigationRailLabelType] = None
    """
    The type that defines the layout and behavior of the labels in the
    [`NavigationRail`][flet.].
    """

    min_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_width`][flet.] in all descendant
    [`NavigationRail`][flet.] controls when they are not extended.
    """

    min_extended_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_extended_width`][flet.] in all
    descendant [`NavigationRail`][flet.] controls when they are extended.
    """

    group_alignment: Optional[Number] = None
    """
    The alignment for the
    [`NavigationRail.destinations`][flet.] as they are
    positioned within the [`NavigationRail`][flet.].
    """

    use_indicator: Optional[bool] = None
    """
    Overrides the default value of
    [`NavigationRail.use_indicator`][flet.] in all
    descendant [`NavigationRail`][flet.] controls.
    """


@dataclass
class AppBarTheme:
    """
    Customizes the appearance of [`AppBar`][flet.] controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.color`][flet.] in all
    descendant [`AppBar`][flet.] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.bgcolor`][flet.] in all
    descendant [`AppBar`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.shadow_color`][flet.] in
    all descendant [`AppBar`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`AppBar.elevation`][flet.] in all
    descendant [`AppBar`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`AppBar.shape`][flet.] in all
    descendant [`AppBar`][flet.] controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AppBar.title_text_style`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AppBar.toolbar_text_style`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """

    center_title: Optional[bool] = None
    """
    Overrides the default value of [`AppBar.center_title`][flet.] in
    all descendant [`AppBar`][flet.] controls.
    """

    title_spacing: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.title_spacing`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """

    elevation_on_scroll: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.elevation_on_scroll`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """

    toolbar_height: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.toolbar_height`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AppBar.actions_padding`][flet.] in all descendant
    [`AppBar`][flet.] controls.
    """


@dataclass
class BottomAppBarTheme:
    """
    Customizes the appearance of [`BottomAppBar`][flet.] controls across
    the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`BottomAppBar.bgcolor`][flet.]
    in all descendant [`BottomAppBar`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`BottomAppBar.shadow_color`][flet.] in all descendant
    [`BottomAppBar`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`BottomAppBar.elevation`][flet.] in all descendant
    `BottomAppBar`][flet.BottomAppBar] controls.
    """

    height: Optional[Number] = None
    """
    Overrides the default value of [`BottomAppBar.height`][flet.] in
    all descendant [`BottomAppBar`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`BottomAppBar.padding`][flet.]
    in all descendant [`BottomAppBar`][flet.] controls.
    """

    shape: Optional[NotchShape] = None
    """
    Overrides the default value of [`BottomAppBar.shape`][flet.] in
    all descendant [`BottomAppBar`][flet.] controls.
    """


@dataclass
class RadioTheme:
    """
    Defines default property values for descendant [`Radio`][flet.] controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Radio.fill_color`][flet.] in
    all descendant [`Radio`][flet.] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Radio.overlay_color`][flet.] in
    all descendant [`Radio`][flet.] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of [`Radio.splash_radius`][flet.] in
    all descendant [`Radio`][flet.] controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of [`Radio.visual_density`][flet.]
    in all descendant [`Radio`][flet.] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of [`Radio.mouse_cursor`][flet.]
    in all descendant [`Radio`][flet.] controls.
    """


@dataclass
class CheckboxTheme:
    """
    Defines default property values for descendant [`Checkbox`][flet.] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.overlay_color`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    check_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.check_color`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.fill_color`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of
    [`Checkbox.splash_radius`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of
    [`Checkbox.border_side`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of
    [`Checkbox.visual_density`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`Checkbox.shape`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of
    [`Checkbox.mouse_cursor`][flet.] in all descendant
    [`Checkbox`][flet.] controls.
    """


@dataclass
class BadgeTheme:
    """
    Defines default property values for descendant [`Badge`][flet.] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Badge.bgcolor`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Badge.text_color`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    small_size: Optional[Number] = None
    """
    Overrides the default value of [`Badge.small_size`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    large_size: Optional[Number] = None
    """
    Overrides the default value of [`Badge.large_size`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of [`Badge.alignment`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Badge.padding`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    offset: Optional[OffsetValue] = None
    """
    Overrides the default value of [`Badge.offset`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value of [`Badge.text_style`][flet.] in all
    descendant [`Badge`][flet.] controls.
    """


@dataclass
class SwitchTheme:
    """
    Defines default property values for descendant [`Switch`][flet.] controls.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.thumb_color`][flet.] in
    all descendant [`Switch`][flet.] controls.
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.track_color`][flet.] in
    all descendant [`Switch`][flet.] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.overlay_color`][flet.]
    in all descendant [`Switch`][flet.] controls.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Switch.track_outline_color`][flet.] in all descendant
    [`Switch`][flet.] controls.
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    Overrides the default value of [`Switch.thumb_icon`][flet.] in all
    descendant [`Switch`][flet.] controls.
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    Overrides the default value of
    [`Switch.track_outline_width`][flet.] in all descendant
    [`Switch`][flet.] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of [`Switch.splash_radius`][flet.]
    in all descendant [`Switch`][flet.] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of [`Switch.mouse_cursor`][flet.] in
    all descendant [`Switch`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Switch.padding`][flet.] in
    all descendant [`Switch`][flet.] controls.
    """


@dataclass
class DividerTheme:
    """
    Defines the visual properties of [`Divider`][flet.],
    [`VerticalDivider`][flet.], dividers between
    [`ListTile`][flet.]s, and dividers between rows in
    [`DataTable`][flet.].
    """

    color: Optional[ColorValue] = None
    """
    The color of [`Divider`][flet.]s and
    [`VerticalDivider`][flet.]s, also used between
    [`ListTile`][flet.]s, between rows in [`DataTable`][flet.]s, and
    so forth.
    """

    thickness: Optional[Number] = None
    """
    The thickness of the line drawn within the divider.
    """

    space: Optional[Number] = None
    """
    The [`Divider`][flet.]'s height or the
    [`VerticalDivider`][flet.]'s width.

    This represents the amount of horizontal or vertical space the divider takes up.
    """

    leading_indent: Optional[Number] = None
    """
    The amount of empty space at the leading edge of [`Divider`][flet.] or top
    edge of [`VerticalDivider`][flet.].
    """

    trailing_indent: Optional[Number] = None
    """
    The amount of empty space at the trailing edge of [`Divider`][flet.] or
    bottom edge of [`VerticalDivider`][flet.].
    """


@dataclass
class SnackBarTheme:
    """
    Defines default property values for descendant [`SnackBar`][flet.] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`SnackBar.bgcolor`][flet.] in all
    descendant [`SnackBar`][flet.] controls.
    """

    action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `text_color` of
    [`SnackBar.action`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `bgcolor` of
    [`SnackBar.action`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    close_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SnackBar.close_icon_color`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    disabled_action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_text_color` of
    [`SnackBar.action`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    disabled_action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_color` of
    [`SnackBar.action`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`SnackBar.elevation`][flet.] in
    all descendant [`SnackBar`][flet.] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Used to configure the `text_style` property for the [`SnackBar.content`] control.
    """

    width: Optional[Number] = None
    """
    Overrides the default value of [`SnackBar.width`][flet.] in all
    descendant [`SnackBar`][flet.] controls.
    """

    show_close_icon: Optional[bool] = None
    """
    Overrides the default value of
    [`SnackBar.show_close_icon`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    Overrides the default value of
    [`SnackBar.dismiss_direction`][flet.] in all descendant
    [`SnackBar`][flet.] controls.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    Overrides the default value of [`SnackBar.behavior`][flet.] in all
    descendant [`SnackBar`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`SnackBar.shape`][flet.] in all
    descendant [`SnackBar`][flet.] controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`SnackBar.margin`][flet.].

    This value is only used when behavior is SnackBarBehavior.floating.
    """

    action_overflow_threshold: Optional[Number] = None
    """
    Overrides the default value of
    [`SnackBar.action_overflow_threshold`][flet.] in
    all descendant [`SnackBar`][flet.] controls.
    """


@dataclass
class BannerTheme:
    """
    Defines default property values for descendant [`Banner`][flet.] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.bgcolor`][flet.] in all
    descendant [`Banner`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.shadow_color`][flet.] in
    all descendant [`Banner`][flet.] controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.divider_color`][flet.]
    in all descendant [`Banner`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`Banner.content_padding`][flet.] in all descendant
    [`Banner`][flet.] controls.
    """

    leading_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`Banner.leading_padding`][flet.] in all descendant
    [`Banner`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Banner.elevation`][flet.] in all
    descendant [`Banner`][flet.] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`Banner.content_text_style`][flet.] in all descendant
    [`Banner`][flet.] controls.
    """


@dataclass
class DatePickerTheme:
    """
    Customizes the appearance of [`DatePicker`][flet.] controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color of the surface in all descendant
    [`DatePicker`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default shadow color in all descendant
    [`DatePicker`][flet.] controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default color used to paint the divider in all descendant
    [`DatePicker`][flet.] controls.
    """

    header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the header's default background fill color.

    The [`DatePicker`][flet.]'s header displays the currently selected date.
    """

    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the
    [`DatePicker.current_date`].[flet.DatePicker.current_date] label in the grid of the
    [`DatePicker`][flet.].
    """

    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the day labels in the
    grid of the [`DatePicker`][flet.].
    """

    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a day
    in the grid is focused, hovered, or pressed.
    """

    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the day labels in the grid of the
    [`DatePicker`][flet.].

    This will be used instead of the color provided in
    [`DatePickerTheme.day_text_style`][flet.].
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`DatePicker`][flet.] elevation.
    """

    range_picker_elevation: Optional[Number] = None
    """
    Overrides the default elevation of the full screen DateRangePicker (TBD).
    """

    day_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for each individual day label in the grid of
    the [`DatePicker`][flet.].

    The color in [`DatePickerTheme.day_text_style`][flet.] is not
    used, [`DatePickerTheme.day_foreground_color`][flet.] is used instead.
    """

    weekday_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the row of weekday labels at the top of
    the [`DatePicker`][flet.] grid.
    """

    year_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used to paint each of the year entries in the year
    selector of the [`DatePicker`][flet.].

    The color of the [`DatePickerTheme.year_text_style`][flet.] is not used,
    [`DatePickerTheme.year_foreground_color`][flet.] is used instead.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`DatePicker`][flet.] shape.

    If elevation is greater than zero then a shadow is shown and the shadow's shape
    mirrors the shape of the dialog.
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the cancel button of a [`DatePicker`][flet.].
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the confirm (OK) button of a [`DatePicker`][flet.].
    """

    header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the header's default color used for text labels and icons.

    The dialog's header displays the currently selected date.

    This is used instead of the color property of
    [`DatePickerTheme.header_headline_text_style`][flet.]
    and [`DatePickerTheme.header_help_text_style`][flet.].
    """

    header_headline_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default headline text style.

    The dialog's header displays the currently selected date.

    The color of the [`DatePickerTheme.header_headline_text_style`][flet.]
    is not used, [`DatePickerTheme.header_foreground_color`][flet.] is used instead.
    """

    header_help_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default help text style.

    The help text (also referred to as "supporting text" in the Material spec) is
    usually a prompt to the user at the top of the header (i.e. 'Select date').

    The color of the `header_help_style` is not used,
    [`DatePickerTheme.header_foreground_color`][flet.] is used instead.
    """

    range_picker_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color for [`DateRangePicker`][flet.].
    """

    range_picker_header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background fill color for [`DateRangePicker`][flet.].

    The dialog's header displays the currently selected date range.
    """

    range_picker_header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the default color used for text labels and icons in the header of a full
    screen [`DateRangePicker`][flet.].

    The dialog's header displays the currently selected date range.

    This is used instead of any colors provided by
    `range_picker_header_headline_text_style` or
    `range_picker_header_help_text_style`.
    """

    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the
    [`DatePicker.current_date`][flet.] label in the grid of the
    dialog's CalendarDatePicker and the corresponding year in the dialog's YearPicker.

    This will be used instead of the color provided in
    [`DatePickerTheme.day_text_style`][flet.].
    """

    range_picker_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default overall shape of a full screen DateRangePicker (TBD).

    If elevation is greater than zero then a shadow is shown and the shadow's shape
    mirrors the shape of the dialog.
    """

    range_picker_header_help_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the help text of the header of a full
    screen DateRangePicker (TBD).

    The help text (also referred to as "supporting text" in the Material spec) is
    usually a prompt to the user at the top of the header (i.e. 'Select date').

    The color of the `range_picker_header_help_text_style` is not used,
    `range_picker_header_foreground_color` is used instead.
    """

    range_picker_header_headline_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the headline text in the header of a
    full screen [`DateRangePicker`][flet.].

    The dialog's header displays the currently selected date range.

    The color of `range_picker_header_headline_text_style` is not used,
    `range_picker_header_foreground_color` is used instead.
    """

    range_selection_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color used to paint days selected between the
    start and end dates in a [`DateRangePicker`][flet.].
    """

    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a
    date in the selected range of a [`DateRangePicker`][flet.] is focused, hovered, or
    pressed.
    """

    today_border_side: Optional[BorderSide] = None
    """
    Overrides the border used to paint the [`DatePicker.current_date`][flet.] label
    in the grid of the [`DatePicker`][flet.].

    The border side's [`BorderSide.color`] is not used,
    [`DatePickerTheme.today_foreground_color`][flet.] is used instead.
    """

    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the year labels in the
    year selector of the of the [`DatePicker`][flet.].
    """

    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the year labels in the year selector of
    the date picker.

    This will be used instead of the color provided in
    [`DatePickerTheme.year_text_style`][flet.].
    """

    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a year
    in the year selector is focused, hovered, or pressed.
    """

    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    Overrides the default shape used to paint the shape decoration of the day labels in
    the grid of the [`DatePicker`][flet.].

    If the selected day is the current day, the provided shape with the value of
    [`DatePickerTheme.today_bgcolor`][flet.] is used to
    paint the shape decoration of the day label and the value of
    [`DatePickerTheme.today_border_side`][flet.] and
    [`DatePickerTheme.today_foreground_color`][flet.]
    is used to paint the border.

    If the selected day is not the current day, the provided shape with the value of
    [`DatePickerTheme.day_bgcolor`][flet.] is used to paint
    the shape decoration of the day label.
    """


@dataclass
class TimePickerTheme:
    """
    Customizes the appearance of [`TimePicker`][flet.] controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of a [`TimePicker`][flet.].

    If this is null, the time picker defaults to the overall theme's
    [`ColorScheme.surface_container_high`][flet.].
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
    The background color of the time picker dial when the entry mode is
    [`TimePickerEntryMode.DIAL`][flet.] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.].
    """

    dial_hand_color: Optional[ColorValue] = None
    """
    The color of the time picker dial's hand when the entry mode is
    [`TimePickerEntryMode.DIAL`][flet.] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.].
    """

    dial_text_color: Optional[ColorValue] = None
    """
    The color of the dial text that represents specific hours and minutes.
    """

    entry_mode_icon_color: Optional[ColorValue] = None
    """
    The color of the entry mode [`IconButton`][flet.].
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
    The style of the AM/PM toggle control of a [`TimePicker`][flet.].
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    The style of the cancel button of a [`TimePicker`][flet.].
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    The style of the confirm (OK) button of a [`TimePicker`][flet.].
    """

    day_period_text_style: Optional[TextStyle] = None
    """
    Used to configure the [`TextStyle`][flet.TextStyle] for the AM/PM toggle control.

    If this is null, the time picker defaults to the overall theme's
    [`TextTheme.title_medium`][flet.].
    """

    dial_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] for the numbers on the time selection dial.
    """

    help_text_style: Optional[TextStyle] = None
    """
    Used to configure the [`TextStyle`][flet.TextStyle]
    for the helper text in the header.
    """

    hour_minute_text_style: Optional[TextStyle] = None
    """
    Used to configure the [`TextStyle`][flet.] for the hour/minute controls.
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
    The shape of the day period that the [`TimePicker`][flet.] uses.
    """

    hour_minute_shape: Optional[OutlinedBorder] = None
    """
    The shape of the hour and minute controls that the [`TimePicker`][flet.]
    uses.
    """

    day_period_border_side: Optional[BorderSide] = None
    """
    The color and weight of the day period's outline.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the time picker dialog when the entry mode is
    [`TimePickerEntryMode.DIAL`][flet.] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.].
    """

    time_selector_separator_color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color of the time selector separator between the hour and minute controls.
    """

    time_selector_separator_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Used to configure the text style for the time selector separator between the hour
    and minute controls.
    """


@dataclass
class DropdownTheme:
    """
    Customizes the appearance of [`Dropdown`][flet.] across the app.
    """

    menu_style: Optional[MenuStyle] = None
    """
    Overrides the default value for [`Dropdown.menu_style`][flet.].
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`Dropdown.text_style`][flet.].
    """


@dataclass
class ListTileTheme:
    """
    Customizes the appearance of descendant [`ListTile`][flet.] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.icon_color`][flet.].
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.text_color`][flet.].
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.bgcolor`][flet.].
    """

    selected_tile_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.selected_tile_color`][flet.].
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.selected_color`][flet.].
    """

    is_three_line: Optional[bool] = None
    """
    Overrides the default value for [`ListTile.is_three_line`][flet.].
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for [`ListTile.enable_feedback`][flet.].
    """

    dense: Optional[bool] = None
    """
    Overrides the default value for [`ListTile.dense`][flet.].
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for [`ListTile.shape`][flet.].
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value for [`ListTile.visual_density`][flet.].
    """

    content_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`ListTile.content_padding`][flet.].
    """

    min_vertical_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`ListTile.min_vertical_padding`][flet.].
    """

    horizontal_spacing: Optional[Number] = None
    """
    Overrides the default value for [`ListTile.horizontal_spacing`][flet.].
    """

    min_leading_width: Optional[Number] = None
    """
    Overrides the default value for [`ListTile.min_leading_width`][flet.].
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`ListTile.title_text_style`][flet.].
    """

    subtitle_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`ListTile.subtitle_text_style`][flet.].
    """

    leading_and_trailing_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`ListTile.leading_and_trailing_text_style`][flet.].
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for [`ListTile.mouse_cursor`][flet.].
    """

    min_height: Optional[Number] = None
    """
    Overrides the default value for [`ListTile.min_height`][flet.].
    """

    affinity: Optional[TileAffinity] = None
    """
    Overrides the default value for [`ExpansionTile.affinity`][flet.].
    """

    style: Optional[ListTileStyle] = None
    """
    Overrides the default value for [`ListTile.style`][flet.].
    """

    title_alignment: Optional[ListTileTitleAlignment] = None
    """
    Overrides the default value for [`ListTile.title_alignment`][flet.].
    """


@dataclass
class TooltipTheme:
    """
    Customizes the appearance of descendant [`Tooltip`][flet.] controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`Tooltip.text_style`][flet.].
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for
    [`Tooltip.enable_feedback`][flet.].
    """

    exclude_from_semantics: Optional[bool] = None
    """
    Overrides the default value for
    [`Tooltip.exclude_from_semantics`][flet.].
    """

    prefer_below: Optional[bool] = None
    """
    Overrides the default value for [`Tooltip.prefer_below`][flet.].
    """

    vertical_offset: Optional[Number] = None
    """
    Overrides the default value for
    [`Tooltip.vertical_offset`][flet.].
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`Tooltip.padding`][flet.].
    """

    wait_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.wait_duration`][flet.].
    """

    exit_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.exit_duration`][flet.].
    """

    show_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.show_duration`][flet.].
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value for [`Tooltip.margin`][flet.].
    """

    trigger_mode: Optional[TooltipTriggerMode] = None
    """
    Overrides the default value for
    [`Tooltip.trigger_mode`][flet.].
    """

    decoration: Optional[BoxDecoration] = None
    """
    Overrides the default value for [`Tooltip.decoration`][flet.].
    """

    text_align: Optional[TextAlign] = None
    """
    Overrides the default value for [`Tooltip.text_align`][flet.].
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for
    [`Tooltip.size_constraints`][flet.].
    """


@dataclass
class ExpansionTileTheme:
    """
    Customizes the appearance of descendant [`ExpansionTile`][flet.]
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.bgcolor`][flet.].
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.icon_color`][flet.].
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.text_color`][flet.].
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_bgcolor`][flet.].
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_icon_color`][flet.].
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value for
    [`ExpansionTile.clip_behavior`][flet.].
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_text_color`][flet.].
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.tile_padding`][flet.].
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Overrides the default value for
    [`ExpansionTile.expanded_alignment`][flet.].
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.controls_padding`][flet.].
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for [`ExpansionTile.shape`][flet.].
    """

    collapsed_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_shape`][flet.].
    """

    animation_style: Optional[AnimationStyle] = None
    """
    Overrides the default value for
    [`ExpansionTile.animation_style`][flet.].
    """


@dataclass
class SliderTheme:
    """
    Customizes the appearance of descendant [`Slider`][flet.] controls.
    """

    active_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.active_color`][flet.].
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`Slider.inactive_color`][flet.].
    """

    thumb_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.thumb_color`][flet.].
    """

    overlay_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.overlay_color`][flet.].
    """

    value_indicator_color: Optional[ColorValue] = None
    """
    The color given to the [`Slider`][flet.]'s value indicator to draw
    itself with.
    """

    disabled_thumb_color: Optional[ColorValue] = None
    """
    The color given to the thumb to draw itself with when the [`Slider`][flet.]
    is disabled.
    """

    value_indicator_text_style: Optional[TextStyle] = None
    """
    The [`TextStyle`][flet.TextStyle] for the text on the value indicator.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for [`Slider.mouse_cursor`][flet.].
    """

    active_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the
    [Slider.min][flet.Slider.min] position and the current thumb position.
    """

    disabled_active_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb
    osition and the [Slider.max][flet.Slider.max] position when the
    [`Slider`][flet.] is disabled.
    """

    disabled_active_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.] track between the
    [Slider.min][flet.Slider.min] position and the current thumb position when the
    [`Slider`][flet.] is disabled.
    """

    disabled_inactive_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb
    position and the [Slider.max][flet.Slider.max] position when the
    [`Slider`][flet.] is disabled.
    """

    disabled_inactive_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.] track between the current thumb position
    and the [Slider.max][flet.Slider.max] position when the [`Slider`][flet.] is
    disabled.
    """

    disabled_secondary_active_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.] track between the current thumb position
    and the [Slider.secondary_track_value][flet.Slider.secondary_track_value] position
    when the [`Slider`][flet.] is disabled.
    """

    inactive_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb
    position and the [Slider.max][flet.Slider.max] position.
    """

    overlapping_shape_stroke_color: Optional[ColorValue] = None
    """
    The color given to the perimeter of the top range thumbs of a
    [RangeSlider][flet.RangeSlider] when the thumbs are overlapping and the top
    range value indicator when the value indicators are overlapping.
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
    Overrides the default value for
    [`Slider.secondary_active_color`][flet.].
    """

    track_height: Optional[Number] = None
    """
    The height of the [Slider][flet.Slider] track.
    """

    value_indicator_stroke_color: Optional[ColorValue] = None
    """
    The color given to the value indicator shape stroke.
    """

    interaction: Optional[SliderInteraction] = None
    """
    Overrides the default value for [`Slider.interaction`][flet.].
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`Slider.padding`][flet.].
    """

    track_gap: Optional[Number] = None
    """
    The size of the gap between the active and inactive tracks of the gapped slider
    track shape.
    """

    thumb_size: Optional[ControlStateValue[Size]] = None
    """
    The size of the handle thumb shape thumb.
    """

    year_2023: bool = False
    """
    Overrides the default value for [`Slider.year_2023`][flet.].
    """


@dataclass
class ProgressIndicatorTheme:
    """
    Customizes the appearance of progress indicators
    ([`ProgressBar`][flet.], [`ProgressRing`][flet.]) across the
    app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default values for [`ProgressBar.color`][flet.] and
    [`ProgressRing.color`][flet.].
    """

    circular_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ProgressRing.bgcolor`][flet.].
    """

    linear_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ProgressBar.bgcolor`][flet.].
    """

    refresh_bgcolor: Optional[ColorValue] = None
    """
    Background color of that fills the circle under the RefreshIndicator (TBD).
    """

    linear_min_height: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressBar.bar_height`][flet.].
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for
    [`ProgressBar.border_radius`][flet.].
    """

    track_gap: Optional[Number] = None
    """
    Overrides the default values for
    [`ProgressBar.track_gap`][flet.] and
    [`ProgressRing.track_gap`][flet.].
    """

    circular_track_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ProgressRing.padding`][flet.].
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for
    [`ProgressRing.size_constraints`][flet.].
    """

    stop_indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ProgressBar.stop_indicator_color`][flet.].
    """

    stop_indicator_radius: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressBar.stop_indicator_radius`][flet.].
    """

    stroke_align: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_align`][flet.].
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_cap`][flet.].
    """

    stroke_width: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_width`][flet.].
    """

    year_2023: bool = False
    """
    Overrides the default values for
    [`ProgressBar.year_2023`][flet.] and
    [`ProgressRing.year_2023`][flet.].
    """


@dataclass
class PopupMenuTheme:
    """
    Customizes the appearance of [`PopupMenuButton`][flet.] across the
    app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.bgcolor`][flet.] in all descendant
    [`PopupMenuButton`][flet.] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.shadow_color`][flet.] in all
    descendant [`PopupMenuButton`][flet.] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.icon_color`][flet.] in all
    descendant [`PopupMenuButton`][flet.] controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`PopupMenuItem.label_text_style`][flet.]
    in all descendant [`PopupMenuItem`][flet.] controls.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value of
    [`PopupMenuButton.enable_feedback`][flet.] in all
    descendant [`PopupMenuButton`][flet.] controls
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`PopupMenuButton.elevation`][flet.] in all descendant
    [`PopupMenuButton`][flet.] controls.
    """

    icon_size: Optional[Number] = None
    """
    Overrides the default value of
    [`PopupMenuButton.icon_size`][flet.] in all descendant
    [`PopupMenuButton`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`PopupMenuButton.shape`][flet.] in all descendant
    [`PopupMenuButton`][flet.] controls.
    """

    menu_position: Optional[PopupMenuPosition] = None
    """
    Overrides the default value of
    [`PopupMenuButton.menu_position`][flet.] in all
    descendant [`PopupMenuButton`][flet.] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of
    [`PopupMenuItem.mouse_cursor`][flet.] in all
    descendant [`PopupMenuItem`][flet.] controls.
    """

    menu_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.menu_padding`][flet.] in all
    descendant [`PopupMenuButton`][flet.] controls.
    """


@dataclass
class SearchBarTheme:
    """
    Customizes the appearance of [`SearchBar`][flet.] controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SearchBar.bar_bgcolor`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    text_capitalization: Optional[TextCapitalization] = None
    """
    Overrides the default value of
    [`SearchBar.capitalization`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_shadow_color`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_overlay_color`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_elevation`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_text_style`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    hint_style: Optional[ControlStateValue[TextStyle]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_hint_text_style`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_shape`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    padding: Optional[ControlStateValue[PaddingValue]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_padding`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`SearchBar.bar_size_constraints`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    border_side: Optional[ControlStateValue[BorderSide]] = None
    """
    Overrides the default value of
    [`SearchBar.bar_border_side`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """


@dataclass
class SearchViewTheme:
    """
    Customizes the appearance of [`SearchBar`][flet.] controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SearchBar.view_bgcolor`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SearchBar.divider_color`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`SearchBar.view_elevation`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    header_hint_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`SearchBar.view_hint_text_style`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    header_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`SearchBar.view_header_text_style`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`SearchBar.view_shape`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    border_side: Optional[BorderSide] = None
    """ Overrides the default value of
    [`SearchBar.view_side`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`SearchBar.view_size_constraints`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    header_height: Optional[Number] = None
    """
    Overrides the default value of
    [`SearchBar.view_header_height`][flet.] in all
    descendant [`SearchBar`][flet.] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`SearchBar.view_padding`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    bar_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`SearchBar.view_bar_padding`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """

    shrink_wrap: Optional[bool] = None
    """
    Overrides the default value of
    [`SearchBar.shrink_wrap`][flet.] in all descendant
    [`SearchBar`][flet.] controls.
    """


@dataclass
class NavigationDrawerTheme:
    """
    Customizes the appearance of descendant [`NavigationDrawer`][flet.]
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`NavigationDrawer.bgcolor`][flet.].
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`NavigationDrawer.shadow_color`][flet.].
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`NavigationDrawer.indicator_color`][flet.].
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value for
    [`NavigationDrawer.elevation`][flet.].
    """

    tile_height: Optional[Number] = None
    """
    Overrides the default height of
    [`NavigationDrawerDestination`][flet.].
    """

    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The style to merge with the default text style for
    [`NavigationDrawerDestination`][flet.] labels.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for
    [`NavigationDrawer.indicator_shape`][flet.].
    """

    indicator_size: Optional[Size] = None
    """
    Overrides the default size of the [`NavigationDrawer`][flet.]'s
    selection indicator.
    """


@dataclass
class NavigationBarTheme:
    """
    Customizes the appearance of [`NavigationBar`][flet.]
    controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """Overrides the default value for
    [`NavigationBar.bgcolor`][flet.].
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`NavigationBar.shadow_color`][flet.].
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`NavigationBar.indicator_color`][flet.].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for
    [`NavigationBar.overlay_color`][flet.].
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value for
    [`NavigationBar.elevation`][flet.].
    """

    height: Optional[Number] = None
    """
    Overrides the default value for NavigationBar height.
    """

    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    """
    The style to merge with the default text style for
    [`NavigationBarDestination`][flet.] labels.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for
    [`NavigationBar.indicator_shape`][flet.].
    """

    label_behavior: Optional[NavigationBarLabelBehavior] = None
    """
    Overrides the default value for
    [`NavigationBar.label_behavior`][flet.].
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`NavigationBar.label_padding`][flet.].
    """


@dataclass
class SegmentedButtonTheme:
    """
    Customizes the appearance of [`SegmentedButton`][flet.]
    controls across the app.
    """

    selected_icon: Optional[IconData] = None
    """
    Overrides the default value for
    [`SegmentedButton.selected_icon`][flet.].
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value for
    [`SegmentedButton.style`][flet.].
    """


@dataclass
class IconTheme:
    """
    Customizes the appearance of [`Icon`][flet.] controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Icon.color`][flet.].
    """

    apply_text_scaling: Optional[bool] = None
    """
    Overrides the default value for
    [`Icon.apply_text_scaling`][flet.].
    """

    fill: Optional[Number] = None
    """
    Overrides the default value for [`Icon.fill`][flet.].
    """

    opacity: Optional[Number] = None
    """
    An opacity to apply to both explicit and default icon colors.
    """

    size: Optional[Number] = None
    """
    Overrides the default value for [`Icon.size`][flet.].
    """

    optical_size: Optional[Number] = None
    """
    Overrides the default value for [`Icon.optical_size`][flet.].
    """

    grade: Optional[Number] = None
    """
    Overrides the default value for [`Icon.grade`][flet.].
    """

    weight: Optional[Number] = None
    """
    Overrides the default value for [`Icon.weight`][flet.].
    """

    shadows: Optional[BoxShadowValue] = None
    """
    Overrides the default value for [`Icon.shadows`][flet.].
    """


@dataclass
class DataTableTheme:
    """
    Customizes the appearance of [`DataTable`][flet.] controls across the app.
    """

    checkbox_horizontal_margin: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.checkbox_horizontal_margin`][flet.].
    """

    column_spacing: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.column_spacing`][flet.].
    """

    data_row_max_height: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.data_row_max_height`][flet.].
    """

    data_row_min_height: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.data_row_min_height`][flet.].
    """

    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for
    [`DataTable.data_row_color`][flet.].
    """

    data_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`DataTable.data_text_style`][flet.].
    """

    divider_thickness: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.divider_thickness`][flet.].
    """

    horizontal_margin: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.horizontal_margin`][flet.].
    """

    heading_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`DataTable.heading_text_style`][flet.].
    """

    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for
    [`DataTable.heading_row_color`][flet.].
    """

    heading_row_height: Optional[Number] = None
    """
    Overrides the default value for
    [`DataTable.heading_row_height`][flet.].
    """

    data_row_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for [`DataRow`][flet.] mouse cursor.
    """

    decoration: Optional[BoxDecoration] = None
    """
    Overrides the default value for [`DataTable`][flet.] decoration.
    """

    heading_row_alignment: Optional[MainAxisAlignment] = None
    """
    Overrides the default value for
    [`DataColumn.heading_row_alignment`][flet.].
    """

    heading_cell_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for
    [`DataColumn`][flet.] mouse cursor.
    """


@dataclass
class Theme:
    """
    Customizes the overall appearance of the application.
    """

    color_scheme_seed: Optional[ColorValue] = None
    """
    Overrides the default color scheme seed used to generate
    [`ColorScheme`][flet.]. The default color is blue.
    """

    font_family: Optional[str] = None
    use_material3: Optional[bool] = None
    appbar_theme: Optional[AppBarTheme] = None
    badge_theme: Optional[BadgeTheme] = None
    banner_theme: Optional[BannerTheme] = None
    bottom_appbar_theme: Optional[BottomAppBarTheme] = None
    bottom_sheet_theme: Optional[BottomSheetTheme] = None
    card_theme: Optional[CardTheme] = None
    checkbox_theme: Optional[CheckboxTheme] = None
    chip_theme: Optional[ChipTheme] = None
    """
    Customizes the appearance of [`Chip`][flet.] across the app.
    """

    color_scheme: Optional[ColorScheme] = None
    """
    Overrides the default [`ColorScheme`][flet.] used for the application.
    """

    data_table_theme: Optional[DataTableTheme] = None
    """
    Customizes the appearance of [`DataTable`][flet.DataTable] across the app.
    """

    date_picker_theme: Optional[DatePickerTheme] = None
    """
    Customizes the appearance of [`DatePicker`][flet.DatePicker] across the app.
    """

    dialog_theme: Optional[DialogTheme] = None
    """
    Customizes the appearance of [`AlertDialog`][flet.] across the app.
    """

    divider_theme: Optional[DividerTheme] = None
    """
    Defines the visual properties of [`Divider`][flet.],
    [`VerticalDivider`][flet.], dividers between
    [`ListTile`][flet.]s, and dividers between rows in
    [`DataTable`][flet.].
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default color of dividers used in
    [`Divider`][flet.], [`VerticalDivider`][flet.], dividers between
    [`ListTile`][flet.]s, and dividers between rows in
    [`DataTable`][flet.].
    """

    dropdown_theme: Optional[DropdownTheme] = None
    """
    Customizes the appearance of [`Dropdown`][flet.] across the app.
    """

    button_theme: Optional[ButtonTheme] = None
    """
    Customizes the appearance of [`Button`][flet.] across the app.
    """

    outlined_button_theme: Optional[OutlinedButtonTheme] = None
    """
    Customizes the appearance of [`OutlinedButton`][flet.] across the app.
    """

    text_button_theme: Optional[TextButtonTheme] = None
    """
    Customizes the appearance of [`TextButton`][flet.] across the app.
    """

    filled_button_theme: Optional[FilledButtonTheme] = None
    """
    Customizes the appearance of [`FilledButton`][flet.] across the app.
    """

    icon_button_theme: Optional[IconButtonTheme] = None
    """
    Customizes the appearance of [`IconButton`][flet.] across the app.
    """

    expansion_tile_theme: Optional[ExpansionTileTheme] = None
    """
    Customizes the appearance of [`ExpansionTile`][flet.] across the app.
    """

    floating_action_button_theme: Optional[FloatingActionButtonTheme] = None
    """
    Customizes the appearance of [`FloatingActionButton`][flet.]
    across the app.
    """

    icon_theme: Optional[IconTheme] = None
    """
    Customizes the appearance of [`Icon`][flet.] across the app.
    """

    list_tile_theme: Optional[ListTileTheme] = None
    """
    Customizes the appearance of [`ListTile`][flet.] across the app.
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
