from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border import BorderSide
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.box import BoxConstraints, BoxDecoration, BoxShadow
from flet.controls.buttons import ButtonStyle, OutlinedBorder
from flet.controls.control_state import ControlStateValue
from flet.controls.duration import DurationValue
from flet.controls.geometry import Size
from flet.controls.margin import MarginValue
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
    Locale,
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
    The color displayed most frequently across your app’s screens and components.
    """

    on_primary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `primary`.
    """

    primary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `primary`.
    """

    on_primary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `primary_container`.
    """

    secondary: Optional[ColorValue] = None
    """
    An accent color used for less prominent components in the UI, such as filter chips,
    while expanding the opportunity for color expression.
    """

    on_secondary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `secondary`.
    """

    secondary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `secondary`.
    """

    on_secondary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `secondary_container`.
    """

    tertiary: Optional[ColorValue] = None
    """
    A color used as a contrasting accent that can balance `primary` and `secondary`
    colors or bring heightened attention to an element, such as an input field.
    """

    on_tertiary: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `tertiary`.
    """

    tertiary_container: Optional[ColorValue] = None
    """
    A color used for elements needing less emphasis than `tertiary`.
    """

    on_tertiary_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `tertiary_container`.
    """

    error: Optional[ColorValue] = None
    """
    The color to use for input validation errors, e.g. for `TextField.error_text`.
    """

    on_error: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `error`.
    """

    error_container: Optional[ColorValue] = None
    """
    A color used for error elements needing less emphasis than `error`.
    """

    on_error_container: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `error_container`.
    """

    surface: Optional[ColorValue] = None
    """
    The background color for widgets like `Card`.
    """

    on_surface: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `surface`.
    """

    on_surface_variant: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `surface_variant`.
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
    UI, for example in a `SnackBar` to bring attention to an alert.
    """

    on_inverse_surface: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `inverse_surface`.
    """

    inverse_primary: Optional[ColorValue] = None
    """
    An accent color used for displaying a highlight color on `inverse_surface`
    backgrounds, like button text in a `SnackBar`.
    """

    surface_tint: Optional[ColorValue] = None
    """
    A color used as an overlay on a surface color to indicate a component's elevation.
    """

    on_primary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `primary_fixed` color.
    """

    on_secondary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `secondary_fixed` color.
    """

    on_tertiary_fixed: Optional[ColorValue] = None
    """
    A color that is used for text and icons that exist on top of elements having
    `tertiary_fixed` color.
    """

    on_primary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_primary_fixed`.
    """

    on_secondary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_secondary_fixed`.
    """

    on_tertiary_fixed_variant: Optional[ColorValue] = None
    """
    A color that provides a lower-emphasis option for text and icons than
    `on_tertiary_fixed`.
    """

    primary_fixed: Optional[ColorValue] = None
    """
    A substitute for `primary_container` that's the same color for the dark and light
    themes.
    """

    secondary_fixed: Optional[ColorValue] = None
    """
    A substitute for `secondary_container` that's the same color for the dark and light
    themes.
    """

    tertiary_fixed: Optional[ColorValue] = None
    """
    A substitute for `tertiary_container` that's the same color for dark and light
    themes.
    """

    primary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than `primary_fixed`.
    """

    secondary_fixed_dim: Optional[ColorValue] = None
    """
    A color used for elements needing more emphasis than `secondary_fixed`.
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
    `surface_container` but more emphasis than `surface_container_lowest`.
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
    A color used for elements needing more emphasis than `tertiary_fixed`.
    """


@dataclass
class TextTheme:
    """
    Customizes [`Text`][flet.Text] styles.

    Material 3 design [defines](http://localhost:3000/docs/controls/text#pre-defined-theme-text-styles)
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
    [`ElevatedButton`][flet.ElevatedButton], [`TextButton`][flet.TextButton] and
    [`OutlinedButton`][flet.OutlinedButton].
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
    Customizes the appearance of [`TabBar`][flet.TabBar] control across the app.
    """

    indicator_size: Optional[TabBarIndicatorSize] = None
    """
    Overrides the default value for
    [`TabBar.indicator_size`][flet.TabBar.indicator_size].
    """

    indicator: Optional[UnderlineTabIndicator] = None
    """
    Overrides the default value for
    [`TabBar.indicator`][flet.TabBar.indicator].
    """

    indicator_animation: Optional[TabIndicatorAnimation] = None
    """
    Overrides the default value for
    [`TabBar.indicator_animation`][flet.TabBar.indicator_animation].
    """

    splash_border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for
    [`TabBar.splash_border_radius`][flet.TabBar.splash_border_radius].
    """

    tab_alignment: Optional[TabAlignment] = None
    """
    Overrides the default value for
    [`TabBar.tab_alignment`][flet.TabBar.tab_alignment].
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value for
    [`TabBar.overlay_color`][flet.TabBar.overlay_color].
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`TabBar.divider_color`][flet.TabBar.divider_color].
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`TabBar.indicator_color`][flet.TabBar.indicator_color].
    """

    mouse_cursor: Optional[ControlStateValue[Optional[MouseCursor]]] = None
    """
    Overrides the default value for
    [`TabBar.mouse_cursor`][flet.TabBar.mouse_cursor].
    """

    divider_height: Optional[Number] = None
    """
    Overrides the default value for
    [`TabBar.divider_height`][flet.TabBar.divider_height].
    """

    label_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`TabBar.label_color`][flet.TabBar.label_color].
    """

    unselected_label_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`TabBar.unselected_label_color`][flet.TabBar.unselected_label_color].
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`TabBar.label_padding`][flet.TabBar.label_padding].
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`TabBar.label_text_style`][flet.TabBar.label_text_style].
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`TabBar.unselected_label_text_style`][flet.TabBar.unselected_label_text_style].
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
    Customizes the appearance of [`AlertDialog`][flet.AlertDialog] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`AlertDialog.bgcolor`][flet.AlertDialog.bgcolor] in
    all descendant [`AlertDialog`][flet.AlertDialog] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.shadow_color`][flet.AlertDialog.shadow_color] in all descendant
    [`AlertDialog`][flet.AlertDialog] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Used to configure the [`IconTheme`][flet.IconTheme] for the
    [`AlertDialog.icon`][flet.AlertDialog.icon] control.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`AlertDialog.elevation`][flet.AlertDialog.elevation] in all descendant dialog
    controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`AlertDialog.shape`][flet.AlertDialog.shape] in all
    descendant [`AlertDialog`][flet.AlertDialog] controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AlertDialog.title_text_style`][flet.AlertDialog.title_text_style] in all
    descendant [`AlertDialog`][flet.AlertDialog] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AlertDialog.content_text_style`].[flet.AlertDialog.content_text_style] in all
    descendant [`AlertDialog`][flet.AlertDialog] controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of [`AlertDialog.alignment`][flet.AlertDialog.alignment]
    in all descendant [`AlertDialog`][flet.AlertDialog] controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AlertDialog.actions_padding`][flet.AlertDialog.actions_padding] in all descendant
    [`AlertDialog`][flet.AlertDialog] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of
    [`AlertDialog.clip_behavior`][flet.AlertDialog.clip_behavior] in all descendant
    [`AlertDialog`][flet.AlertDialog] controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.barrier_color`][flet.AlertDialog.barrier_color] in all descendant
    [`AlertDialog`][flet.AlertDialog] controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AlertDialog.inset_padding`][flet.AlertDialog.inset_padding] in all descendant
    [`AlertDialog`][flet.AlertDialog] controls.
    """


@dataclass
class ElevatedButtonTheme:
    """
    Customizes the appearance of [`ElevatedButton`][flet.ElevatedButton] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of
    [`ElevatedButton.style`][flet.ElevatedButton.style] in all descendant
    [`ElevatedButton`][flet.ElevatedButton] controls.
    """


@dataclass
class OutlinedButtonTheme:
    """
    Customizes the appearance of [`OutlinedButton`][flet.OutlinedButton] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of
    [`OutlinedButton.style`][flet.OutlinedButton.style] in all descendant
    [`OutlinedButton`][flet.OutlinedButton] controls.
    """


@dataclass
class TextButtonTheme:
    """
    Customizes the appearance of [`TextButton`][flet.TextButton] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of
    [`TextButton.style`][flet.TextButton.style] in all descendant
    [`TextButton`][flet.TextButton] controls.
    """


@dataclass
class FilledButtonTheme:
    """
    Customizes the appearance of [`FilledButton`][flet.FilledButton] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of
    [`FilledButton.style`][flet.FilledButton.style] in all descendant
    [`FilledButton`][flet.FilledButton] controls.
    """


@dataclass
class IconButtonTheme:
    """
    Customizes the appearance of [`IconButton`][flet.IconButton] across the app.
    """

    style: Optional[ButtonStyle] = None
    """
    Overrides the default value of
    [`IconButton.style`][flet.IconButton.style] in all descendant
    [`IconButton`][flet.IconButton] controls.
    """


@dataclass
class BottomSheetTheme:
    """
    Customizes the appearance of [`BottomSheet`][flet.BottomSheet] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`BottomSheet.bgcolor`][flet.BottomSheet.bgcolor] in
    all descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`BottomSheet.elevation`][flet.BottomSheet.elevation] in all descendant
    [`BottomSheet`][flet.BottomSheet] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`BottomSheet.shape`][flet.BottomSheet.shape] in all
    descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    show_drag_handle: Optional[bool] = None
    """
    Overrides the default value of
    [`BottomSheet.show_drag_handle`][flet.BottomSheet.show_drag_handle] in all
    descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of
    [`BottomSheet.clip_behavior`][flet.BottomSheet.clip_behavior] in all
    descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`BottomSheet.size_constraints`][flet.BottomSheet.size_constraints] in all
    descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`BottomSheet.barrier_color`][flet.BottomSheet.barrier_color] in all
    descendant [`BottomSheet`][flet.BottomSheet] controls.
    """

    drag_handle_color: Optional[ColorValue] = None
    """
    Overrides the default value of drag handle color in all descendant
    [`BottomSheet`][flet.BottomSheet] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of shadow color in all descendant
    [`BottomSheet`][flet.BottomSheet] controls.
    """


@dataclass
class CardTheme:
    """
    Customizes the appearance of [`Card`][flet.Card] across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Card.clip_behavior`][flet.Card.clip_behavior] in
    all descendant [`Card`][flet.Card] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Card.shadow_color`][flet.Card.shadow_color] in
    all descendant [`Card`][flet.Card] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`Card.elevation`][flet.Card.elevation] in all descendant [`Card`][flet.Card]
    controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`Card.shape`][flet.Card.shape] in all descendant
    [`Card`][flet.Card] controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of [`Card.clip_behavior`][flet.Card.clip_behavior] in
    all descendant [`Card`][flet.Card] controls.
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value of [`Card.margin`][flet.Card.margin] in all descendant
    [`Card`][flet.Card] controls.
    """


@dataclass
class ChipTheme:
    """
    Customizes the appearance of [`Chip`][flet.Chip] across the app.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Chip.color`][flet.Chip.color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.bgcolor`][flet.Chip.bgcolor] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Chip.shadow_color`][flet.Chip.shadow_color] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.selected_shadow_color`][flet.Chip.selected_shadow_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    disabled_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.disabled_color`][flet.Chip.disabled_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.selected_color`][flet.Chip.selected_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    check_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.check_color`][flet.Chip.check_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.delete_icon_color`][flet.Chip.delete_icon_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Chip.elevation`][flet.Chip.elevation] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    elevation_on_click: Optional[Number] = None
    """
    Overrides the default value of
    [`Chip.elevation_on_click`][flet.Chip.elevation_on_click] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`Chip.shape`][flet.Chip.shape] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Chip.padding`][flet.Chip.padding] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Chip.label_padding`][flet.Chip.label_padding] in
    all descendant [`Chip`][flet.Chip] controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`Chip.label_text_style`][flet.Chip.label_text_style] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of [`Chip.border_side`][flet.Chip.border_side] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    show_checkmark: Optional[bool] = None
    """
    Overrides the default value of [`Chip.show_checkmark`][flet.Chip.show_checkmark] in
    all descendant [`Chip`][flet.Chip] controls.
    """

    leading_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`Chip.leading_size_constraints`][flet.Chip.leading_size_constraints] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`Chip.delete_icon_size_constraints`][flet.Chip.delete_icon_size_constraints] in
    all descendant [`Chip`][flet.Chip] controls.
    """

    brightness: Optional[Brightness] = None
    """
    Overrides the default value for all chips which affects various base
    material color choices in the chip rendering.
    """

    # secondary_selected_color: Optional[ColorValue] = None
    # secondary_label_text_style: Optional[TextStyle] = None


@dataclass
class FloatingActionButtonTheme:
    """
    Customizes the appearance of [`FloatingActionButton`][flet.FloatingActionButton]
    across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled
    [`FloatingActionButton`][flet.FloatingActionButton]'s background.
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
    [`FloatingActionButton`][flet.FloatingActionButton]'s foreground.
    """

    splash_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.splash_color`][flet.FloatingActionButton.splash_color] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the unselected, enabled
    [`FloatingActionButton`][flet.FloatingActionButton]'s elevation foreground.
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
    [`FloatingActionButton`][flet.FloatingActionButton]'s elevation foreground.
    """

    disabled_elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the disabled
    [`FloatingActionButton`][flet.FloatingActionButton]'s elevation foreground.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`FloatingActionButton.shape`][flet.FloatingActionButton.shape] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    enable_feedback: Optional[bool] = None
    """
    If specified, defines the feedback property for
    [`FloatingActionButton`][flet.FloatingActionButton].
    """

    extended_padding: Optional[PaddingValue] = None
    """
    The padding for an extended [`FloatingActionButton`][flet.FloatingActionButton]'s
    content.
    """

    extended_text_style: Optional[TextStyle] = None
    """
    The text style for an extended
    [`FloatingActionButton`][flet.FloatingActionButton].
    """

    extended_icon_label_spacing: Optional[Number] = None
    """
    The spacing between the icon and the label for an extended
    [`FloatingActionButton`][flet.FloatingActionButton].
    """

    extended_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of
    extended [`FloatingActionButton`][flet.FloatingActionButton].
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default size constraints of
    [`FloatingActionButton`][flet.FloatingActionButton].
    """

    # large_size_constraints: Optional[BoxConstraints] = None
    # small_size_constraints: Optional[BoxConstraints] = None


@dataclass
class NavigationRailTheme:
    """
    Customizes the appearance of [`NavigationRail`][flet.NavigationRail] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the [`NavigationRail`][flet.NavigationRail]'s background.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`NavigationRail.indicator_color`][flet.NavigationRail.indicator_color] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls. when
    [`NavigationRailTheme.use_indicator`][flet.NavigationRailTheme.use_indicator]
    is true.
    """

    elevation: Optional[Number] = None
    """
    The z-coordinate to be used for the [`NavigationRail`][flet.NavigationRail]'s
    elevation.
    """

    indicator_shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`NavigationRail.indicator_shape`][flet.NavigationRail.indicator_shape] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls.
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`NavigationRail.unselected_label_text_style`][flet.NavigationRail.unselected_label_text_style]
    in all descendant [`NavigationRail`][flet.NavigationRail] controls.
    """

    selected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`NavigationRail.selected_label_text_style`][flet.NavigationRail.selected_label_text_style]
    in all descendant [`NavigationRail`][flet.NavigationRail] controls.
    """

    label_type: Optional[NavigationRailLabelType] = None
    """
    The type that defines the layout and behavior of the labels in the
    [`NavigationRail`][flet.NavigationRail].
    """

    min_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_width`][flet.NavigationRail.min_width] in all descendant
    [`NavigationRail`][flet.NavigationRail] controls when they are not extended.
    """

    min_extended_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_extended_width`][flet.NavigationRail.min_extended_width] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls when they are extended.
    """

    group_alignment: Optional[Number] = None
    """
    The alignment for the
    [`NavigationRail.destinations`][flet.NavigationRail.destinations] as they are
    positioned within the [`NavigationRail`][flet.NavigationRail].
    """

    use_indicator: Optional[bool] = None
    """
    Overrides the default value of
    [`NavigationRail.use_indicator`][flet.NavigationRail.use_indicator] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls.
    """


@dataclass
class AppBarTheme:
    """
    Customizes the appearance of [`AppBar`][flet.AppBar] controls across the app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.color`][flet.AppBar.color] in all
    descendant [`AppBar`][flet.AppBar] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.bgcolor`][flet.AppBar.bgcolor] in all
    descendant [`AppBar`][flet.AppBar] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`AppBar.shadow_color`][flet.AppBar.shadow_color] in
    all descendant [`AppBar`][flet.AppBar] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`AppBar.elevation`][flet.AppBar.elevation] in all
    descendant [`AppBar`][flet.AppBar] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`AppBar.shape`][flet.AppBar.shape] in all
    descendant [`AppBar`][flet.AppBar] controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AppBar.title_text_style`][flet.AppBar.title_text_style] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    toolbar_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AppBar.toolbar_text_style`][flet.AppBar.toolbar_text_style] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    center_title: Optional[bool] = None
    """
    Overrides the default value of [`AppBar.center_title`][flet.AppBar.center_title] in
    all descendant [`AppBar`][flet.AppBar] controls.
    """

    title_spacing: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.title_spacing`][flet.AppBar.title_spacing] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    elevation_on_scroll: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.elevation_on_scroll`][flet.AppBar.elevation_on_scroll] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    toolbar_height: Optional[Number] = None
    """
    Overrides the default value of
    [`AppBar.toolbar_height`][flet.AppBar.toolbar_height] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AppBar.actions_padding`][flet.AppBar.actions_padding] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """


@dataclass
class BottomAppBarTheme:
    """
    Customizes the appearance of [`BottomAppBar`][flet.BottomAppBar] controls across
    the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`BottomAppBar.bgcolor`][flet.BottomAppBar.bgcolor]
    in all descendant [`BottomAppBar`][flet.BottomAppBar] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`BottomAppBar.shadow_color`][flet.BottomAppBar.shadow_color] in all descendant
    [`BottomAppBar`][flet.BottomAppBar] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`BottomAppBar.elevation`][flet.BottomAppBar.elevation] in all descendant
    `BottomAppBar`][flet.BottomAppBar] controls.
    """

    height: Optional[Number] = None
    """
    Overrides the default value of [`BottomAppBar.height`][flet.BottomAppBar.height] in
    all descendant [`BottomAppBar`][flet.BottomAppBar] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`BottomAppBar.padding`][flet.BottomAppBar.padding]
    in all descendant [`BottomAppBar`][flet.BottomAppBar] controls.
    """

    shape: Optional[NotchShape] = None
    """
    Overrides the default value of [`BottomAppBar.shape`][flet.BottomAppBar.shape] in
    all descendant [`BottomAppBar`][flet.BottomAppBar] controls.
    """


@dataclass
class RadioTheme:
    """
    Defines default property values for descendant [`Radio`][flet.Radio] controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Radio.fill_color`][flet.Radio.fill_color] in
    all descendant [`Radio`][flet.Radio] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Radio.overlay_color`][flet.Radio.overlay_color] in
    all descendant [`Radio`][flet.Radio] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of [`Radio.splash_radius`][flet.Radio.splash_radius] in
    all descendant [`Radio`][flet.Radio] controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of [`Radio.visual_density`][flet.Radio.visual_density]
    in all descendant [`Radio`][flet.Radio] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of [`Radio.mouse_cursor`][flet.Radio.mouse_cursor]
    in all descendant [`Radio`][flet.Radio] controls.
    """


@dataclass
class CheckboxTheme:
    """
    Defines default property values for descendant [`Checkbox`][flet.Checkbox] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.overlay_color`][flet.Checkbox.overlay_color] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    check_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.check_color`][flet.Checkbox.check_color] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    fill_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Checkbox.fill_color`][flet.Checkbox.fill_color] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of
    [`Checkbox.splash_radius`][flet.Checkbox.splash_radius] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of
    [`Checkbox.border_side`][flet.Checkbox.border_side] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value of
    [`Checkbox.visual_density`][flet.Checkbox.visual_density] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`Checkbox.shape`][flet.Checkbox.shape] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of
    [`Checkbox.mouse_cursor`][flet.Checkbox.mouse_cursor] in all descendant
    [`Checkbox`][flet.Checkbox] controls.
    """


@dataclass
class BadgeTheme:
    """
    Defines default property values for descendant [`Badge`][flet.Badge] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Badge.bgcolor`][flet.Badge.bgcolor] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Badge.text_color`][flet.Badge.text_color] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    small_size: Optional[Number] = None
    """
    Overrides the default value of [`Badge.small_size`][flet.Badge.small_size] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    large_size: Optional[Number] = None
    """
    Overrides the default value of [`Badge.large_size`][flet.Badge.large_size] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of [`Badge.alignment`][flet.Badge.alignment] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Badge.padding`][flet.Badge.padding] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    offset: Optional[OffsetValue] = None
    """
    Overrides the default value of [`Badge.offset`][flet.Badge.offset] in all
    descendant [`Badge`][flet.Badge] controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value of [`Badge.text_style`][flet.Badge.text_style] in all
    descendant [`Badge`][flet.Badge] controls.
    """


@dataclass
class SwitchTheme:
    """
    Defines default property values for descendant [`Switch`][flet.Switch] controls.
    """

    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.thumb_color`][flet.Switch.thumb_color] in
    all descendant [`Switch`][flet.Switch] controls.
    """

    track_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.track_color`][flet.Switch.track_color] in
    all descendant [`Switch`][flet.Switch] controls.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of [`Switch.overlay_color`][flet.Switch.overlay_color]
    in all descendant [`Switch`][flet.Switch] controls.
    """

    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default value of
    [`Switch.track_outline_color`][flet.Switch.track_outline_color] in all descendant
    [`Switch`][flet.Switch] controls.
    """

    thumb_icon: Optional[ControlStateValue[IconData]] = None
    """
    Overrides the default value of [`Switch.thumb_icon`][flet.Switch.thumb_icon] in all
    descendant [`Switch`][flet.Switch] controls.
    """

    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    """
    Overrides the default value of
    [`Switch.track_outline_width`][flet.Switch.track_outline_width] in all descendant
    [`Switch`][flet.Switch] controls.
    """

    splash_radius: Optional[Number] = None
    """
    Overrides the default value of [`Switch.splash_radius`][flet.Switch.splash_radius]
    in all descendant [`Switch`][flet.Switch] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of [`Switch.mouse_cursor`][flet.Switch.mouse_cursor] in
    all descendant [`Switch`][flet.Switch] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of [`Switch.padding`][flet.Switch.padding] in
    all descendant [`Switch`][flet.Switch] controls.
    """


@dataclass
class DividerTheme:
    """
    Defines the visual properties of [`Divider`][flet.Divider],
    [`VerticalDivider`][flet.VerticalDivider], dividers between
    [`ListTile`][flet.ListTile]s, and dividers between rows in
    [`DataTable`][flet.DataTable].
    """

    color: Optional[ColorValue] = None
    """
    The color of [`Divider`][flet.Divider]s and
    [`VerticalDivider`][flet.VerticalDivider]s, also used between
    [`ListTile`][flet.ListTile]s, between rows in [`DataTable`][flet.DataTable]s, and
    so forth.
    """

    thickness: Optional[Number] = None
    """
    The thickness of the line drawn within the divider.
    """

    space: Optional[Number] = None
    """
    The [`Divider`][flet.Divider]'s height or the
    [`VerticalDivider`][flet.VerticalDivider]'s width.

    This represents the amount of horizontal or vertical space the divider takes up.
    """

    leading_indent: Optional[Number] = None
    """
    The amount of empty space at the leading edge of [`Divider`][flet.Divider] or top
    edge of [`VerticalDivider`][flet.VerticalDivider].
    """

    trailing_indent: Optional[Number] = None
    """
    The amount of empty space at the trailing edge of [`Divider`][flet.Divider] or
    bottom edge of [`VerticalDivider`][flet.VerticalDivider].
    """


@dataclass
class SnackBarTheme:
    """
    Defines default property values for descendant [`SnackBar`][flet.SnackBar] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`SnackBar.bgcolor`][flet.SnackBar.bgcolor] in all
    descendant [`SnackBar`][flet.SnackBar] controls.
    """

    action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `text_color` of
    [`SnackBar.action`][flet.SnackBar.action] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `bgcolor` of
    [`SnackBar.action`][flet.SnackBar.action] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    close_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SnackBar.close_icon_color`][flet.SnackBar.close_icon_color] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    disabled_action_text_color: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_text_color` of
    [`SnackBar.action`][flet.SnackBar.action] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    disabled_action_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of `disabled_color` of
    [`SnackBar.action`][flet.SnackBar.action] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`SnackBar.elevation`][flet.SnackBar.elevation] in
    all descendant [`SnackBar`][flet.SnackBar] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Used to configure the `text_style` property for the [`SnackBar.content`] control.
    """

    width: Optional[Number] = None
    """
    Overrides the default value of [`SnackBar.width`][flet.SnackBar.width] in all
    descendant [`SnackBar`][flet.SnackBar] controls.
    """

    show_close_icon: Optional[bool] = None
    """
    Overrides the default value of
    [`SnackBar.show_close_icon`][flet.SnackBar.show_close_icon] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    Overrides the default value of
    [`SnackBar.dismiss_direction`][flet.SnackBar.dismiss_direction] in all descendant
    [`SnackBar`][flet.SnackBar] controls.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    Overrides the default value of [`SnackBar.behavior`][flet.SnackBar.behavior] in all
    descendant [`SnackBar`][flet.SnackBar] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`SnackBar.shape`][flet.SnackBar.shape] in all
    descendant [`SnackBar`][flet.SnackBar] controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`SnackBar.margin`][flet.SnackBar.margin].

    This value is only used when behavior is SnackBarBehavior.floating.
    """

    action_overflow_threshold: Optional[Number] = None
    """
    Overrides the default value of
    [`SnackBar.action_overflow_threshold`][flet.SnackBar.action_overflow_threshold] in
    all descendant [`SnackBar`][flet.SnackBar] controls.
    """


@dataclass
class BannerTheme:
    """
    Defines default property values for descendant [`Banner`][flet.Banner] controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.bgcolor`][flet.Banner.bgcolor] in all
    descendant [`Banner`][flet.Banner] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.shadow_color`][flet.Banner.shadow_color] in
    all descendant [`Banner`][flet.Banner] controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default value of [`Banner.divider_color`][flet.Banner.divider_color]
    in all descendant [`Banner`][flet.Banner] controls.
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`Banner.content_padding`][flet.Banner.content_padding] in all descendant
    [`Banner`][flet.Banner] controls.
    """

    leading_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`Banner.leading_padding`][flet.Banner.leading_padding] in all descendant
    [`Banner`][flet.Banner] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Banner.elevation`][flet.Banner.elevation] in all
    descendant [`Banner`][flet.Banner] controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`Banner.content_text_style`][flet.Banner.content_text_style] in all descendant
    [`Banner`][flet.Banner] controls.
    """


@dataclass
class DatePickerTheme:
    """
    Customizes the appearance of [`DatePicker`][flet.DatePicker] controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color of the surface in all descendant
    [`DatePicker`][flet.DatePicker] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default shadow color in all descendant
    [`DatePicker`][flet.DatePicker] controls.
    """

    divider_color: Optional[ColorValue] = None
    """
    Overrides the default color used to paint the divider in all descendant
    [`DatePicker`][flet.DatePicker] controls.
    """

    header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the header's default background fill color.

    The [`DatePicker`][flet.DatePicker]'s header displays the currently selected date.
    """

    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the
    [`DatePicker.current_date`].[flet.DatePicker.current_date] label in the grid of the
    [`DatePicker`][flet.DatePicker].
    """

    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the day labels in the
    grid of the [`DatePicker`][flet.DatePicker].
    """

    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a day
    in the grid is focused, hovered, or pressed.
    """

    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the day labels in the grid of the
    [`DatePicker`][flet.DatePicker].

    This will be used instead of the color provided in
    [`DatePickerTheme.day_text_style`][flet.DatePickerTheme.day_text_style].
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`DatePicker`][flet.DatePicker] elevation.
    """

    range_picker_elevation: Optional[Number] = None
    """
    Overrides the default elevation of the full screen DateRangePicker (TBD).
    """

    day_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for each individual day label in the grid of
    the [`DatePicker`][flet.DatePicker].

    The color in
    [`DatePickerTheme.day_text_style`][flet.DatePickerTheme.day_text_style] is not
    used,
    [`DatePickerTheme.day_foreground_color`][flet.DatePickerTheme.day_foreground_color]
    is used instead.
    """

    weekday_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used for the row of weekday labels at the top of
    the [`DatePicker`][flet.DatePicker] grid.
    """

    year_text_style: Optional[TextStyle] = None
    """
    Overrides the default text style used to paint each of the year entries in the year
    selector of the [`DatePicker`][flet.DatePicker].

    The color of the
    [`DatePickerTheme.year_text_style`][flet.DatePickerTheme.year_text_style] is not
    used,
    [`DatePickerTheme.year_foreground_color`][flet.DatePickerTheme.year_foreground_color]
    is used instead.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of [`DatePicker`][flet.DatePicker] shape.

    If elevation is greater than zero then a shadow is shown and the shadow's shape
    mirrors the shape of the dialog.
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the cancel button of a
    [`DatePicker`][flet.DatePicker].
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    Overrides the default style of the confirm (OK) button of a
    [`DatePicker`][flet.DatePicker].
    """

    header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the header's default color used for text labels and icons.

    The dialog's header displays the currently selected date.

    This is used instead of the color property of
    [`DatePickerTheme.header_headline_text_style`][flet.DatePickerTheme.header_headline_text_style]
    and
    [`DatePickerTheme.header_help_text_style`][flet.DatePickerTheme.header_help_text_style].
    """

    header_headline_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default headline text style.

    The dialog's header displays the currently selected date.

    The color of the
    [`DatePickerTheme.header_headline_text_style`][flet.DatePickerTheme.header_headline_text_style]
    is not used,
    [`DatePickerTheme.header_foreground_color`][flet.DatePickerTheme.header_foreground_color]
    is used instead.
    """

    header_help_text_style: Optional[TextStyle] = None
    """
    Overrides the header's default help text style.

    The help text (also referred to as "supporting text" in the Material spec) is
    usually a prompt to the user at the top of the header (i.e. 'Select date').

    The color of the `header_help_style` is not used,
    [`DatePickerTheme.header_foreground_color`][flet.DatePickerTheme.header_foreground_color]
    is used instead.
    """

    range_picker_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color for DateRangePicker (TBD).
    """

    range_picker_header_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background fill color for DateRangePicker (TBD).

    The dialog's header displays the currently selected date range.
    """

    range_picker_header_foreground_color: Optional[ColorValue] = None
    """
    Overrides the default color used for text labels and icons in the header of a full
    screen DateRangePicker (TBD)

    The dialog's header displays the currently selected date range.

    This is used instead of any colors provided by
    `range_picker_header_headline_text_style` or `range_picker_header_help_text_style`.
    """

    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the
    [`DatePicker.current_date`][flet.DatePicker.current_date] label in the grid of the
    dialog's CalendarDatePicker and the corresponding year in the dialog's YearPicker.

    This will be used instead of the color provided in
    [`DatePickerTheme.day_text_style`][flet.DatePickerTheme.day_text_style].
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
    Overrides the default text style used for the headline text in the header of a full
    screen DateRangePicker (TBD).

    The dialog's header displays the currently selected date range.

    The color of `range_picker_header_headline_text_style` is not used,
    `range_picker_header_foreground_color` is used instead.
    """

    range_selection_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default background color used to paint days selected between the
    start and end dates in a DateRangePicker (TBD).
    """

    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a date
    in the selected range of a DateRangePicker (TBD) is focused, hovered, or pressed.
    """

    today_border_side: Optional[BorderSide] = None
    """
    Overrides the border used to paint the
    [`DatePicker.current_date`][flet.DatePicker.current_date] label in the
    grid of the [`DatePicker`][flet.DatePicker].

    The border side's [`BorderSide.color`] is not used,
    [`DatePickerTheme.today_foreground_color`][flet.DatePickerTheme.today_foreground_color]
    is used instead.
    """

    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the background of the year labels in the
    year selector of the of the [`DatePicker`][flet.DatePicker].
    """

    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default color used to paint the year labels in the year selector of
    the date picker.

    This will be used instead of the color provided in
    [`DatePickerTheme.year_text_style`][flet.DatePickerTheme.year_text_style].
    """

    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Overrides the default highlight color that's typically used to indicate that a year
    in the year selector is focused, hovered, or pressed.
    """

    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    """
    Overrides the default shape used to paint the shape decoration of the day labels in
    the grid of the [`DatePicker`][flet.DatePicker].

    If the selected day is the current day, the provided shape with the value of
    [`DatePickerTheme.today_bgcolor`][flet.DatePickerTheme.today_bgcolor] is used to
    paint the shape decoration of the day label and the value of
    [`DatePickerTheme.today_border_side`][flet.DatePickerTheme.today_border_side] and
    [`DatePickerTheme.today_foreground_color`][flet.DatePickerTheme.today_foreground_color]
    is used to paint the border.

    If the selected day is not the current day, the provided shape with the value of
    [`DatePickerTheme.day_bgcolor`][flet.DatePickerTheme.day_bgcolor] is used to paint
    the shape decoration of the day label.
    """

    locale: Optional[Locale] = None
    """
    An optional locale argument can be used to set the locale for the date picker. It
    defaults to the ambient locale provided by Localizations.
    """


@dataclass
class TimePickerTheme:
    """
    Customizes the appearance of [`TimePicker`][flet.TimePicker] controls across the
    app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of a [`TimePicker`][flet.TimePicker].

    If this is null, the time picker defaults to the overall theme's
    [`ColorScheme.surface_container_high`][flet.ColorScheme.surface_container_high].
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
    [`TimePickerEntryMode.DIAL`][flet.TimePickerEntryMode.DIAL] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.TimePickerEntryMode.DIAL_ONLY].
    """

    dial_hand_color: Optional[ColorValue] = None
    """
    The color of the time picker dial's hand when the entry mode is
    [`TimePickerEntryMode.DIAL`][flet.TimePickerEntryMode.DIAL] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.TimePickerEntryMode.DIAL_ONLY].
    """

    dial_text_color: Optional[ColorValue] = None
    """
    The color of the dial text that represents specific hours and minutes.
    """

    entry_mode_icon_color: Optional[ColorValue] = None
    """
    The color of the entry mode [`IconButton`][flet.IconButton].
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
    The style of the AM/PM toggle control of a [`TimePicker`][flet.TimePicker].
    """

    cancel_button_style: Optional[ButtonStyle] = None
    """
    The style of the cancel button of a [`TimePicker`][flet.TimePicker].
    """

    confirm_button_style: Optional[ButtonStyle] = None
    """
    The style of the confirm (OK) button of a [`TimePicker`][flet.TimePicker].
    """

    day_period_text_style: Optional[TextStyle] = None
    """
    Used to configure the [TextStyle][flet.TextStyle] for the AM/PM toggle control.

    If this is null, the time picker defaults to the overall theme's
    [`TextTheme.title_medium`][flet.TextTheme.title_medium].
    """

    dial_text_style: Optional[TextStyle] = None
    """
    The [TextStyle][flet.TextStyle] for the numbers on the time selection dial.
    """

    help_text_style: Optional[TextStyle] = None
    """
    Used to configure the [TextStyle][flet.TextStyle] for the helper text in the header.

    """

    hour_minute_text_style: Optional[TextStyle] = None
    """
    Used to configure the [TextStyle][flet.TextStyle] for the hour/minute controls.
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
    The shape of the day period that the [`TimePicker`][flet.TimePicker] uses.
    """

    hour_minute_shape: Optional[OutlinedBorder] = None
    """
    The shape of the hour and minute controls that the [`TimePicker`][flet.TimePicker]
    uses.
    """

    day_period_border_side: Optional[BorderSide] = None
    """
    The color and weight of the day period's outline.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding around the time picker dialog when the entry mode is
    [`TimePickerEntryMode.DIAL`][flet.TimePickerEntryMode.DIAL] or
    [`TimePickerEntryMode.DIAL_ONLY`][flet.TimePickerEntryMode.DIAL_ONLY].
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
    Overrides the default values of visual properties for descendant
    [`Dropdown`][flet.Dropdown] controls.
    """

    menu_style: Optional[MenuStyle] = None
    """
    The menu style for descendant [`Dropdown`][flet.Dropdown] controls. If `elevation`,
    `bgcolor` and/or `menu_width` are provided for the [`MenuStyle`][flet.MenuStyle]
    then they will override the default values for
    [`DropdownMenu.elevation`][flet.Dropdown.elevation],
    [`DropdownMenu.bgcolor`][flet.Dropdown.bgcolor] and
    [`DropdownMenu.menu_width`][flet.Dropdown.menu_width].
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`DropdownMenu.text_style`][flet.Dropdown.text_style].
    """


@dataclass
class ListTileTheme:
    """
    Customizes the appearance of descendant [`ListTile`][flet.ListTile] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.icon_color`][flet.ListTile.icon_color].
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.text_color`][flet.ListTile.text_color].
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for [`ListTile.bgcolor`][flet.ListTile.bgcolor].
    """

    selected_tile_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ListTile.selected_tile_color`][flet.ListTile.selected_tile_color].
    """

    selected_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ListTile.selected_color`][flet.ListTile.selected_color].
    """

    is_three_line: Optional[bool] = None
    """
    Overrides the default value for
    [`ListTile.is_three_line`][flet.ListTile.is_three_line].
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for
    [`ListTile.enable_feedback`][flet.ListTile.enable_feedback].
    """

    dense: Optional[bool] = None
    """
    Overrides the default value for [`ListTile.dense`][flet.ListTile.dense].
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value for [`ListTile.shape`][flet.ListTile.shape].
    """

    visual_density: Optional[VisualDensity] = None
    """
    Overrides the default value for
    [`ListTile.visual_density`][flet.ListTile.visual_density].
    """

    content_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ListTile.content_padding`][flet.ListTile.content_padding].
    """

    min_vertical_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ListTile.min_vertical_padding`][flet.ListTile.min_vertical_padding].
    """

    horizontal_spacing: Optional[Number] = None
    """
    Overrides the default value for
    [`ListTile.horizontal_spacing`][flet.ListTile.horizontal_spacing].
    """

    min_leading_width: Optional[Number] = None
    """
    Overrides the default value for
    [`ListTile.min_leading_width`][flet.ListTile.min_leading_width].
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`ListTile.title_text_style`][flet.ListTile.title_text_style].
    """

    subtitle_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`ListTile.subtitle_text_style`][flet.ListTile.subtitle_text_style].
    """

    leading_and_trailing_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`ListTile.leading_and_trailing_text_style`][flet.ListTile.leading_and_trailing_text_style].
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for
    [`ListTile.mouse_cursor`][flet.ListTile.mouse_cursor].
    """

    min_tile_height: Optional[Number] = None
    """
    Overrides the default value for
    [`ListTile.min_height`][flet.ListTile.min_height].
    """


@dataclass
class TooltipTheme:
    """
    Customizes the appearance of descendant [`Tooltip`][flet.Tooltip] controls.
    """

    text_style: Optional[TextStyle] = None
    """
    Overrides the default value for [`Tooltip.text_style`][flet.Tooltip.text_style].
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value for
    [`Tooltip.enable_feedback`][flet.Tooltip.enable_feedback].
    """

    exclude_from_semantics: Optional[bool] = None
    """
    Overrides the default value for
    [`Tooltip.exclude_from_semantics`][flet.Tooltip.exclude_from_semantics].
    """

    prefer_below: Optional[bool] = None
    """
    Overrides the default value for [`Tooltip.prefer_below`][flet.Tooltip.prefer_below].
    """

    vertical_offset: Optional[Number] = None
    """
    Overrides the default value for
    [`Tooltip.vertical_offset`][flet.Tooltip.vertical_offset].
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`Tooltip.padding`][flet.Tooltip.padding].
    """

    wait_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.wait_duration`][flet.Tooltip.wait_duration].
    """

    exit_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.exit_duration`][flet.Tooltip.exit_duration].
    """

    show_duration: Optional[DurationValue] = None
    """
    Overrides the default value for
    [`Tooltip.show_duration`][flet.Tooltip.show_duration].
    """

    margin: Optional[MarginValue] = None
    """
    Overrides the default value for [`Tooltip.margin`][flet.Tooltip.margin].
    """

    trigger_mode: Optional[TooltipTriggerMode] = None
    """
    Overrides the default value for
    [`Tooltip.trigger_mode`][flet.Tooltip.trigger_mode].
    """

    decoration: Optional[BoxDecoration] = None
    """
    Overrides the default value for [`Tooltip.decoration`][flet.Tooltip.decoration].
    """

    text_align: Optional[TextAlign] = None
    """
    Overrides the default value for [`Tooltip.text_align`][flet.Tooltip.text_align].
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for
    [`Tooltip.size_constraints`][flet.Tooltip.size_constraints].
    """


@dataclass
class ExpansionTileTheme:
    """
    Customizes the appearance of descendant [`ExpansionTile`][flet.ExpansionTile]
    controls.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.bgcolor`][flet.ExpansionTile.bgcolor].
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.icon_color`][flet.ExpansionTile.icon_color].
    """

    text_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.text_color`][flet.ExpansionTile.text_color].
    """

    collapsed_bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_bgcolor`][flet.ExpansionTile.collapsed_bgcolor].
    """

    collapsed_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_icon_color`][flet.ExpansionTile.collapsed_icon_color].
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value for
    [`ExpansionTile.clip_behavior`][flet.ExpansionTile.clip_behavior].
    """

    collapsed_text_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.collapsed_text_color`][flet.ExpansionTile.collapsed_text_color].
    """

    tile_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.tile_padding`][flet.ExpansionTile.tile_padding].
    """

    expanded_alignment: Optional[Alignment] = None
    """
    Overrides the default value for
    [`ExpansionTile.expanded_alignment`][flet.ExpansionTile.expanded_alignment].
    """

    controls_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ExpansionTile.controls_padding`][flet.ExpansionTile.controls_padding].
    """


@dataclass
class SliderTheme:
    """
    Customizes the appearance of descendant [`Slider`][flet.Slider] controls.
    """

    active_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.active_color`][flet.Slider.active_color].
    """

    inactive_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`Slider.inactive_color`][flet.Slider.inactive_color].
    """

    thumb_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.thumb_color`][flet.Slider.thumb_color].
    """

    overlay_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`Slider.overlay_color`][flet.Slider.overlay_color].
    """

    value_indicator_color: Optional[ColorValue] = None
    """
    The color given to the [`Slider`][flet.Slider]'s value indicator to draw
    itself with.
    """

    disabled_thumb_color: Optional[ColorValue] = None
    """
    The color given to the thumb to draw itself with when the [`Slider`][flet.Slider]
    is disabled.
    """

    value_indicator_text_style: Optional[TextStyle] = None
    """
    The [TextStyle][flet.TextStyle] for the text on the value indicator.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value for [`Slider.mouse_cursor`][flet.Slider.mouse_cursor].
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
    [`Slider`][flet.Slider] is disabled.
    """

    disabled_active_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.Slider] track between the
    [Slider.min][flet.Slider.min] position and the current thumb position when the
    [`Slider`][flet.Slider] is disabled.
    """

    disabled_inactive_tick_mark_color: Optional[ColorValue] = None
    """
    The color of the track's tick marks that are drawn between the current thumb
    position and the [Slider.max][flet.Slider.max] position when the
    [`Slider`][flet.Slider] is disabled.
    """

    disabled_inactive_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.Slider] track between the current thumb position
    and the [Slider.max][flet.Slider.max] position when the [`Slider`][flet.Slider] is
    disabled.
    """

    disabled_secondary_active_track_color: Optional[ColorValue] = None
    """
    The color of the [`Slider`][flet.Slider] track between the current thumb position
    and the [Slider.secondary_track_value][flet.Slider.secondary_track_value] position
    when the [`Slider`][flet.Slider] is disabled.
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
    [`Slider.secondary_active_color`][flet.Slider.secondary_active_color].
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
    Overrides the default value for [`Slider.interaction`][flet.Slider.interaction].
    """

    padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`Slider.padding`][flet.Slider.padding].
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
    Overrides the default value for [`Slider.year_2023`][flet.Slider.year_2023].
    """


@dataclass
class ProgressIndicatorTheme:
    """
    Customizes the appearance of progress indicators
    ([`ProgressBar`][flet.ProgressBar], [`ProgressRing`][flet.ProgressRing]) across the
    app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default values for [`ProgressBar.color`][flet.ProgressBar.color] and
    [`ProgressRing.color`][flet.ProgressRing.color].
    """

    circular_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ProgressRing.bgcolor`][flet.ProgressRing.bgcolor].
    """

    linear_track_color: Optional[ColorValue] = None
    """
    Overrides the default value for [`ProgressBar.bgcolor`][flet.ProgressBar.bgcolor].
    """

    refresh_bgcolor: Optional[ColorValue] = None
    """
    Background color of that fills the circle under the RefreshIndicator (TBD).
    """

    linear_min_height: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressBar.bar_height`][flet.ProgressBar.bar_height].
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Overrides the default value for
    [`ProgressBar.border_radius`][flet.ProgressBar.border_radius].
    """

    track_gap: Optional[Number] = None
    """
    Overrides the default values for
    [`ProgressBar.track_gap`][flet.ProgressBar.track_gap] and
    [`ProgressRing.track_gap`][flet.ProgressRing.track_gap].
    """

    circular_track_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for
    [`ProgressRing.padding`][flet.ProgressRing.padding].
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value for
    [`ProgressRing.size_constraints`][flet.ProgressRing.size_constraints].
    """

    stop_indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value for
    [`ProgressBar.stop_indicator_color`][flet.ProgressBar.stop_indicator_color].
    """

    stop_indicator_radius: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressBar.stop_indicator_radius`][flet.ProgressBar.stop_indicator_radius].
    """

    stroke_align: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_align`][flet.ProgressRing.stroke_align].
    """

    stroke_cap: Optional[StrokeCap] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_cap`][flet.ProgressRing.stroke_cap].
    """

    stroke_width: Optional[Number] = None
    """
    Overrides the default value for
    [`ProgressRing.stroke_width`][flet.ProgressRing.stroke_width].
    """

    year_2023: bool = False
    """
    Overrides the default values for
    [`ProgressBar.year_2023`][flet.ProgressBar.year_2023] and
    [`ProgressRing.year_2023`][flet.ProgressRing.year_2023].
    """


@dataclass
class PopupMenuTheme:
    """
    Customizes the appearance of [`PopupMenuButton`][flet.PopupMenuButton] across the
    app.
    """

    color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.bgcolor`][flet.PopupMenuButton.bgcolor] in all descendant
    [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.shadow_color`][flet.PopupMenuButton.shadow_color] in all
    descendant [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.icon_color`][flet.PopupMenuButton.icon_color] in all
    descendant [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`PopupMenuItem.label_text_style`][flet.PopupMenuItem.label_text_style]
    in all descendant [`PopupMenuItem`][flet.PopupMenuItem] controls.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value of
    [`PopupMenuButton.enable_feedback`][flet.PopupMenuButton.enable_feedback] in all
    descendant [`PopupMenuButton`][flet.PopupMenuButton] controls
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`PopupMenuButton.elevation`][flet.PopupMenuButton.elevation] in all descendant
    [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    icon_size: Optional[Number] = None
    """
    Overrides the default value of
    [`PopupMenuButton.icon_size`][flet.PopupMenuButton.icon_size] in all descendant
    [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`PopupMenuButton.shape`][flet.PopupMenuButton.shape] in all descendant
    [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    menu_position: Optional[PopupMenuPosition] = None
    """
    Overrides the default value of
    [`PopupMenuButton.menu_position`][flet.PopupMenuButton.menu_position] in all
    descendant [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """

    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    """
    Overrides the default value of
    [`PopupMenuItem.mouse_cursor`][flet.PopupMenuItem.mouse_cursor] in all
    descendant [`PopupMenuItem`][flet.PopupMenuItem] controls.
    """

    menu_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`PopupMenuButton.menu_padding`][flet.PopupMenuButton.menu_padding] in all
    descendant [`PopupMenuButton`][flet.PopupMenuButton] controls.
    """


@dataclass
class SearchBarTheme:
    """
    Customizes the appearance of [`SearchBar`][flet.SearchBar] controls across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`SearchBar.bar_bgcolor`][flet.SearchBar.bar_bgcolor] in all descendant
    [`SearchBar`][flet.SearchBar] controls.
    """

    text_capitalization: Optional[TextCapitalization] = None
    """
    Overrides the default value of
    [`SearchBar.capitalization`][flet.SearchBar.capitalization] in all descendant
    [`SearchBar`][flet.SearchBar] controls.
    """

    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[ControlStateValue[Optional[Number]]] = None
    text_style: Optional[ControlStateValue[TextStyle]] = None
    hint_style: Optional[ControlStateValue[TextStyle]] = None
    shape: Optional[ControlStateValue[OutlinedBorder]] = None
    padding: Optional[ControlStateValue[PaddingValue]] = None
    size_constraints: Optional[BoxConstraints] = None
    border_side: Optional[ControlStateValue[BorderSide]] = None


@dataclass
class SearchViewTheme:
    bgcolor: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    header_hint_text_style: Optional[TextStyle] = None
    header_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    border_side: Optional[BorderSide] = None
    size_constraints: Optional[BoxConstraints] = None
    header_height: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    bar_padding: Optional[PaddingValue] = None
    shrink_wrap: Optional[bool] = None


@dataclass
class NavigationDrawerTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    tile_height: Optional[Number] = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    indicator_size: Optional[Size] = None


@dataclass
class NavigationBarTheme:
    bgcolor: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    indicator_color: Optional[ColorValue] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[Number] = None
    height: Optional[Number] = None
    label_text_style: Optional[ControlStateValue[TextStyle]] = None
    indicator_shape: Optional[OutlinedBorder] = None
    label_behavior: Optional[NavigationBarLabelBehavior] = None
    label_padding: Optional[PaddingValue] = None


@dataclass
class SegmentedButtonTheme:
    selected_icon: Optional[IconData] = None
    style: Optional[ButtonStyle] = None


@dataclass
class IconTheme:
    color: Optional[ColorValue] = None
    apply_text_scaling: Optional[bool] = None
    fill: Optional[Number] = None
    opacity: Optional[Number] = None
    size: Optional[Number] = None
    optical_size: Optional[Number] = None
    grade: Optional[Number] = None
    weight: Optional[Number] = None
    shadows: Optional[list[BoxShadow]] = None


@dataclass
class DataTableTheme:
    checkbox_horizontal_margin: Optional[Number] = None
    column_spacing: Optional[Number] = None
    data_row_max_height: Optional[Number] = None
    data_row_min_height: Optional[Number] = None
    data_row_color: Optional[ControlStateValue[ColorValue]] = None
    data_text_style: Optional[TextStyle] = None
    divider_thickness: Optional[Number] = None
    horizontal_margin: Optional[Number] = None
    heading_text_style: Optional[TextStyle] = None
    heading_row_color: Optional[ControlStateValue[ColorValue]] = None
    heading_row_height: Optional[Number] = None
    data_row_cursor: Optional[ControlStateValue[MouseCursor]] = None
    decoration: Optional[BoxDecoration] = None
    heading_row_alignment: Optional[MainAxisAlignment] = None
    heading_cell_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class Theme:
    color_scheme_seed: Optional[ColorValue] = None
    primary_swatch: Optional[ColorValue] = None
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
    color_scheme: Optional[ColorScheme] = None
    data_table_theme: Optional[DataTableTheme] = None
    date_picker_theme: Optional[DatePickerTheme] = None
    dialog_theme: Optional[DialogTheme] = None
    divider_theme: Optional[DividerTheme] = None
    dropdown_theme: Optional[DropdownTheme] = None
    elevated_button_theme: Optional[ElevatedButtonTheme] = None
    outlined_button_theme: Optional[OutlinedButtonTheme] = None
    text_button_theme: Optional[TextButtonTheme] = None
    filled_button_theme: Optional[FilledButtonTheme] = None
    icon_button_theme: Optional[IconButtonTheme] = None
    expansion_tile_theme: Optional[ExpansionTileTheme] = None
    floating_action_button_theme: Optional[FloatingActionButtonTheme] = None
    icon_theme: Optional[IconTheme] = None
    list_tile_theme: Optional[ListTileTheme] = None
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
    divider_color: Optional[ColorValue] = None
    hint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    secondary_header_color: Optional[ColorValue] = None
    primary_color: Optional[ColorValue] = None
    primary_color_dark: Optional[ColorValue] = None
    primary_color_light: Optional[ColorValue] = None
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
