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
from flet.controls.material.textfield import TextCapitalization
from flet.controls.material.tooltip import TooltipTriggerMode
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import (
    Brightness,
    ClipBehavior,
    ColorValue,
    IconValue,
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

    background: Optional[ColorValue] = None
    """
    A color that typically appears behind scrollable content.
    """

    on_background: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `background`.
    """

    surface: Optional[ColorValue] = None
    """
    The background color for widgets like `Card`.
    """

    on_surface: Optional[ColorValue] = None
    """
    A color that's clearly legible when drawn on `surface`.
    """

    surface_variant: Optional[ColorValue] = None
    """
    A color variant of `surface` that can be used for differentiation against a
    component using `surface`.
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
class TabsTheme:
    """
    Customizes the appearance of [`Tabs`][flet.Tabs] control across the app.
    """

    divider_color: Optional[ColorValue] = None
    """
    The color of the divider.
    """

    indicator_border_radius: Optional[BorderRadiusValue] = None
    """
    The radius of the indicator's corners.
    """

    indicator_border_side: Optional[BorderSide] = None
    """
    The color and weight of the horizontal line drawn below the selected tab.
    """

    indicator_padding: Optional[PaddingValue] = None
    """
    Locates the selected tab's underline relative to the tab's boundary. The
    `indicator_tab_size` property can be used to define the tab indicator's bounds in
    terms of its (centered) tab widget with `False`, or the entire tab with `True`.
    """

    indicator_color: Optional[ColorValue] = None
    """
    The color of the line that appears below the selected tab.
    """

    indicator_tab_size: Optional[bool] = None
    """
    `True` for indicator to take entire tab.
    """

    label_color: Optional[ColorValue] = None
    """
    The color of selected tab labels.
    """

    unselected_label_color: Optional[ColorValue] = None
    """
    The color of unselected tab labels.
    """

    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    """
    Defines the ink response focus, hover, and splash colors. If specified, it is
    resolved against one of `ControlState.FOCUSED`, `ControlState.HOVERED`, and
    `ControlState.PRESSED`.
    """

    mouse_cursor: Optional[ControlStateValue[Optional[MouseCursor]]] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over the individual
    tabs.
    """

    label_padding: Optional[PaddingValue] = None
    """
    Overrides the default value for [`Tabs.label_padding`][flet.Tabs.label_padding].

    If there are few tabs with both icon and text and few tabs with only icon or text,
    this padding is vertically adjusted to provide uniform padding to all tabs.
    """

    label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`Tabs.label_text_style`][flet.Tabs.label_text_style].
    """

    unselected_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value for
    [`Tabs.unselected_label_text_style`][flet.Tabs.unselected_label_text_style].
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
    The [`Brightness`][flet.Brightness] of the system navigation bar icons. Either
    `Brightness.DARK` or `Brightness.LIGHT`.
    """

    status_bar_brightness: Optional[Brightness] = None
    """
    The [`Brightness`][flet.Brightness] of the status bar. Either `Brightness.DARK` or
    `Brightness.LIGHT`.
    """

    status_bar_icon_brightness: Optional[Brightness] = None
    """
    The [`Brightness`][flet.Brightness] of the status bar icons. Either
    `Brightness.DARK` or `Brightness.LIGHT`.
    """


@dataclass
class DialogTheme:
    """
    Customizes the appearance of [`AlertDialog`][flet.AlertDialog] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of [`AlertDialog.bgcolor`][flet.AlertDialog.bgcolor] in
    all descendant dialog controls.
    """

    shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.shadow_color`][flet.AlertDialog.shadow_color] in all descendant
    dialog controls.
    """

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.surface_tint_color`][flet.AlertDialog.surface_tint_color] in all
    descendant dialog controls.
    """

    icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.icon_color`][flet.AlertDialog.icon_color] in all descendant dialog
    controls.
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
    descendant dialog controls.
    """

    title_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AlertDialog.title_text_style`][flet.AlertDialog.title_text_style] in all
    descendant dialog controls.
    """

    content_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`AlertDialog.content_text_style`].[flet.AlertDialog.content_text_style] in all
    descendant dialog controls.
    """

    alignment: Optional[Alignment] = None
    """
    Overrides the default value of [`AlertDialog.alignment`][flet.AlertDialog.alignment]
    in all descendant dialog controls.
    """

    actions_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AlertDialog.actions_padding`][flet.AlertDialog.actions_padding] in all descendant
    dialog controls.
    """

    clip_behavior: Optional[ClipBehavior] = None
    """
    Overrides the default value of
    [`AlertDialog.clip_behavior`][flet.AlertDialog.clip_behavior] in all descendant
    dialog controls.
    """

    barrier_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AlertDialog.barrier_color`][flet.AlertDialog.barrier_color] in all descendant
    dialog controls.
    """

    inset_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`AlertDialog.inset_padding`][flet.AlertDialog.inset_padding] in all descendant
    dialog controls.
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

    modal_elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`BottomSheet.modal_elevation`][flet.BottomSheet.modal_elevation] in all
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
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None


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

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Card.surface_tint_color`][flet.Card.surface_tint_color] in all descendant
    [`Card`][flet.Card] controls.
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

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.surface_tint_color`][flet.Chip.surface_tint_color] in all descendant
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

    checkmark_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.checkmark_color`][flet.Chip.checkmark_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.delete_icon_color`][flet.Chip.delete_icon_color] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    secondary_selected_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.secondary_selected_color`][flet.Chip.secondary_selected_color] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`Chip.selected_shadow_color`][flet.Chip.selected_shadow_color] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of [`Chip.elevation`][flet.Chip.elevation] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    elevation_on_click: Optional[Number] = None
    """
    Overrides the default value of [`Chip.click_elevation`][flet.Chip.click_elevation]
    in all descendant [`Chip`][flet.Chip] controls.
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

    secondary_label_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`Chip.secondary_label_text_style`][flet.Chip.secondary_label_text_style] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    border_side: Optional[BorderSide] = None
    """
    Overrides the default value of [`Chip.border_side`][flet.Chip.border_side] in all
    descendant [`Chip`][flet.Chip] controls.
    """

    brightness: Optional[Brightness] = None
    """
    Overrides the default value of [`Chip.brightness`][flet.Chip.brightness] in all
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
    [`Chip.leading_size_constraints`][flet.Chip.leading_size_constraints] in all descendant
    [`Chip`][flet.Chip] controls.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`Chip.delete_icon_size_constraints`][flet.Chip.delete_icon_size_constraints] in
    all descendant [`Chip`][flet.Chip] controls.
    """


@dataclass
class FloatingActionButtonTheme:
    """
    Customizes the appearance of [`FloatingActionButton`][flet.FloatingActionButton]
    across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.bgcolor`][flet.FloatingActionButton.bgcolor] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    hover_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.hover_color`][flet.FloatingActionButton.hover_color] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    focus_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.focus_color`][flet.FloatingActionButton.focus_color] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    foreground_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.foreground_color`][flet.FloatingActionButton.foreground_color]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    splash_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.splash_color`][flet.FloatingActionButton.splash_color] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.elevation`][flet.FloatingActionButton.elevation] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    focus_elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.focus_elevation`][flet.FloatingActionButton.focus_elevation]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    hover_elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.hover_elevation`][flet.FloatingActionButton.hover_elevation]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    highlight_elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.highlight_elevation`][flet.FloatingActionButton.highlight_elevation]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    disabled_elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.disabled_elevation`][flet.FloatingActionButton.disabled_elevation]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    shape: Optional[OutlinedBorder] = None
    """
    Overrides the default value of
    [`FloatingActionButton.shape`][flet.FloatingActionButton.shape] in all
    descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    enable_feedback: Optional[bool] = None
    """
    Overrides the default value of
    [`FloatingActionButton.enable_feedback`][flet.FloatingActionButton.enable_feedback]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    extended_padding: Optional[PaddingValue] = None
    """
    Overrides the default value of
    [`FloatingActionButton.extended_padding`][flet.FloatingActionButton.extended_padding]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    extended_text_style: Optional[TextStyle] = None
    """
    Overrides the default value of
    [`FloatingActionButton.extended_text_style`][flet.FloatingActionButton.extended_text_style]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    extended_icon_label_spacing: Optional[Number] = None
    """
    Overrides the default value of
    [`FloatingActionButton.extended_icon_label_spacing`][flet.FloatingActionButton.extended_icon_label_spacing]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    extended_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`FloatingActionButton.extended_size_constraints`][flet.FloatingActionButton.extended_size_constraints]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`FloatingActionButton.size_constraints`][flet.FloatingActionButton.size_constraints]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    large_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`FloatingActionButton.large_size_constraints`][flet.FloatingActionButton.large_size_constraints]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """

    small_size_constraints: Optional[BoxConstraints] = None
    """
    Overrides the default value of
    [`FloatingActionButton.small_size_constraints`][flet.FloatingActionButton.small_size_constraints]
    in all descendant [`FloatingActionButton`][flet.FloatingActionButton] controls.
    """


@dataclass
class NavigationRailTheme:
    """
    Customizes the appearance of [`NavigationRail`][flet.NavigationRail] across the app.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`NavigationRail.bgcolor`][flet.NavigationRail.bgcolor] in all descendant
    [`NavigationRail`][flet.NavigationRail] controls.
    """

    indicator_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`NavigationRail.indicator_color`][flet.NavigationRail.indicator_color] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls.
    """

    elevation: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.elevation`][flet.NavigationRail.elevation]in all descendant
    [`NavigationRail`][flet.NavigationRail] controls.
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
    Overrides the default value of
    [`NavigationRail.label_type`][flet.NavigationRail.label_type] in all descendant
    [`NavigationRail`][flet.NavigationRail] controls.
    """

    min_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_width`][flet.NavigationRail.min_width] in all descendant
    [`NavigationRail`][flet.NavigationRail] controls.
    """

    min_extended_width: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.min_extended_width`][flet.NavigationRail.min_extended_width] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls.
    """

    group_alignment: Optional[Number] = None
    """
    Overrides the default value of
    [`NavigationRail.group_alignment`][flet.NavigationRail.group_alignment] in all
    descendant [`NavigationRail`][flet.NavigationRail] controls.
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

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AppBar.surface_tint_color`][flet.AppBar.surface_tint_color] in all descendant
    [`AppBar`][flet.AppBar] controls.
    """

    foreground_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`AppBar.foreground_color`][flet.AppBar.foreground_color] in all descendant
    [`AppBar`][flet.AppBar] controls.
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

    surface_tint_color: Optional[ColorValue] = None
    """
    Overrides the default value of
    [`BottomAppBar.surface_tint_color`][flet.BottomAppBar.surface_tint_color] in all
    descendant [`BottomAppBar`][flet.BottomAppBar] controls.
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
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: Optional[Number] = None
    height: Optional[Number] = None
    visual_density: Optional[VisualDensity] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class CheckboxTheme:
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    check_color: Optional[ControlStateValue[ColorValue]] = None
    fill_color: Optional[ControlStateValue[ColorValue]] = None
    splash_radius: Optional[Number] = None
    border_side: Optional[BorderSide] = None
    visual_density: Optional[VisualDensity] = None
    shape: Optional[OutlinedBorder] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None


@dataclass
class BadgeTheme:
    bgcolor: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    small_size: Optional[Number] = None
    large_size: Optional[Number] = None
    alignment: Optional[Alignment] = None
    padding: Optional[PaddingValue] = None
    offset: Optional[OffsetValue] = None
    text_style: Optional[TextStyle] = None


@dataclass
class SwitchTheme:
    thumb_color: Optional[ControlStateValue[ColorValue]] = None
    track_color: Optional[ControlStateValue[ColorValue]] = None
    overlay_color: Optional[ControlStateValue[ColorValue]] = None
    track_outline_color: Optional[ControlStateValue[ColorValue]] = None
    thumb_icon: Optional[ControlStateValue[IconValue]] = None
    track_outline_width: Optional[ControlStateValue[Optional[Number]]] = None
    splash_radius: Optional[Number] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    padding: Optional[PaddingValue] = None


@dataclass
class DividerTheme:
    color: Optional[ColorValue] = None
    thickness: Optional[Number] = None
    space: Optional[Number] = None
    leading_indent: Optional[Number] = None
    trailing_indent: Optional[Number] = None


@dataclass
class SnackBarTheme:
    bgcolor: Optional[ColorValue] = None
    action_text_color: Optional[ColorValue] = None
    action_bgcolor: Optional[ColorValue] = None
    close_icon_color: Optional[ColorValue] = None
    disabled_action_text_color: Optional[ColorValue] = None
    disabled_action_bgcolor: Optional[ColorValue] = None
    elevation: Optional[Number] = None
    content_text_style: Optional[TextStyle] = None
    width: Optional[Number] = None
    alignment: Optional[Alignment] = None
    show_close_icon: Optional[bool] = None
    dismiss_direction: Optional[DismissDirection] = None
    behavior: Optional[SnackBarBehavior] = None
    shape: Optional[OutlinedBorder] = None
    inset_padding: Optional[PaddingValue] = None
    action_overflow_threshold: Optional[Number] = None


@dataclass
class BannerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    padding: Optional[PaddingValue] = None
    leading_padding: Optional[PaddingValue] = None
    elevation: Optional[Number] = None
    content_text_style: Optional[TextStyle] = None


@dataclass
class DatePickerTheme:
    bgcolor: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    divider_color: Optional[ColorValue] = None
    header_bgcolor: Optional[ColorValue] = None
    today_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    day_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    elevation: Optional[Number] = None
    range_picker_elevation: Optional[Number] = None
    day_text_style: Optional[TextStyle] = None
    weekday_text_style: Optional[TextStyle] = None
    year_text_style: Optional[TextStyle] = None
    shape: Optional[OutlinedBorder] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    header_foreground_color: Optional[ColorValue] = None
    header_headline_text_style: Optional[TextStyle] = None
    header_help_text_style: Optional[TextStyle] = None
    range_picker_bgcolor: Optional[ColorValue] = None
    range_picker_header_bgcolor: Optional[ColorValue] = None
    range_picker_header_foreground_color: Optional[ColorValue] = None
    today_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    range_picker_shape: Optional[OutlinedBorder] = None
    range_picker_header_help_text_style: Optional[TextStyle] = None
    range_picker_header_headline_text_style: Optional[TextStyle] = None
    range_picker_surface_tint_color: Optional[ColorValue] = None
    range_selection_bgcolor: Optional[ColorValue] = None
    range_selection_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    today_border_side: Optional[BorderSide] = None
    year_bgcolor: Optional[ControlStateValue[ColorValue]] = None
    year_foreground_color: Optional[ControlStateValue[ColorValue]] = None
    year_overlay_color: Optional[ControlStateValue[ColorValue]] = None
    day_shape: Optional[ControlStateValue[OutlinedBorder]] = None
    locale: Optional[Locale] = None


@dataclass
class TimePickerTheme:
    bgcolor: Optional[ColorValue] = None
    day_period_color: Optional[ColorValue] = None
    day_period_text_color: Optional[ColorValue] = None
    dial_bgcolor: Optional[ColorValue] = None
    dial_hand_color: Optional[ColorValue] = None
    dial_text_color: Optional[ColorValue] = None
    entry_mode_icon_color: Optional[ColorValue] = None
    hour_minute_color: Optional[ColorValue] = None
    hour_minute_text_color: Optional[ColorValue] = None
    day_period_button_style: Optional[ButtonStyle] = None
    cancel_button_style: Optional[ButtonStyle] = None
    confirm_button_style: Optional[ButtonStyle] = None
    day_period_text_style: Optional[TextStyle] = None
    dial_text_style: Optional[TextStyle] = None
    help_text_style: Optional[TextStyle] = None
    hour_minute_text_style: Optional[TextStyle] = None
    elevation: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    day_period_shape: Optional[OutlinedBorder] = None
    hour_minute_shape: Optional[OutlinedBorder] = None
    day_period_border_side: Optional[BorderSide] = None
    padding: Optional[PaddingValue] = None
    time_selector_separator_color: Optional[ControlStateValue[ColorValue]] = None
    time_selector_separator_text_style: Optional[ControlStateValue[TextStyle]] = None


@dataclass
class DropdownTheme:
    menu_style: Optional[MenuStyle] = None
    text_style: Optional[TextStyle] = None


@dataclass
class ListTileTheme:
    icon_color: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    bgcolor: Optional[ColorValue] = None
    selected_tile_color: Optional[ColorValue] = None
    selected_color: Optional[ColorValue] = None
    is_three_line: Optional[bool] = None
    enable_feedback: Optional[bool] = None
    dense: Optional[bool] = None
    shape: Optional[OutlinedBorder] = None
    visual_density: Optional[VisualDensity] = None
    content_padding: Optional[PaddingValue] = None
    min_vertical_padding: Optional[PaddingValue] = None
    horizontal_spacing: Optional[Number] = None
    min_leading_width: Optional[Number] = None
    title_text_style: Optional[TextStyle] = None
    subtitle_text_style: Optional[TextStyle] = None
    leading_and_trailing_text_style: Optional[TextStyle] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    min_tile_height: Optional[Number] = None


@dataclass
class TooltipTheme:
    text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    exclude_from_semantics: Optional[bool] = None
    prefer_below: Optional[bool] = None
    vertical_offset: Optional[Number] = None
    padding: Optional[PaddingValue] = None
    wait_duration: Optional[DurationValue] = None
    exit_duration: Optional[DurationValue] = None
    show_duration: Optional[DurationValue] = None
    margin: Optional[MarginValue] = None
    trigger_mode: Optional[TooltipTriggerMode] = None
    decoration: Optional[BoxDecoration] = None
    text_align: Optional[TextAlign] = None
    size_constraints: Optional[BoxConstraints] = None


@dataclass
class ExpansionTileTheme:
    bgcolor: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_color: Optional[ColorValue] = None
    collapsed_bgcolor: Optional[ColorValue] = None
    collapsed_icon_color: Optional[ColorValue] = None
    clip_behavior: Optional[ClipBehavior] = None
    collapsed_text_color: Optional[ColorValue] = None
    tile_padding: Optional[PaddingValue] = None
    expanded_alignment: Optional[Alignment] = None
    controls_padding: Optional[PaddingValue] = None


@dataclass
class SliderTheme:
    active_track_color: Optional[ColorValue] = None
    inactive_track_color: Optional[ColorValue] = None
    thumb_color: Optional[ColorValue] = None
    overlay_color: Optional[ColorValue] = None
    value_indicator_color: Optional[ColorValue] = None
    disabled_thumb_color: Optional[ColorValue] = None
    value_indicator_text_style: Optional[TextStyle] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    active_tick_mark_color: Optional[ColorValue] = None
    disabled_active_tick_mark_color: Optional[ColorValue] = None
    disabled_active_track_color: Optional[ColorValue] = None
    disabled_inactive_tick_mark_color: Optional[ColorValue] = None
    disabled_inactive_track_color: Optional[ColorValue] = None
    disabled_secondary_active_track_color: Optional[ColorValue] = None
    inactive_tick_mark_color: Optional[ColorValue] = None
    overlapping_shape_stroke_color: Optional[ColorValue] = None
    min_thumb_separation: Optional[Number] = None
    secondary_active_track_color: Optional[ColorValue] = None
    track_height: Optional[Number] = None
    value_indicator_stroke_color: Optional[ColorValue] = None
    interaction: Optional[SliderInteraction] = None
    padding: Optional[PaddingValue] = None
    track_gap: Optional[Number] = None
    thumb_size: Optional[ControlStateValue[Size]] = None
    year_2023: Optional[bool] = None


@dataclass
class ProgressIndicatorTheme:
    color: Optional[ColorValue] = None
    circular_track_color: Optional[ColorValue] = None
    linear_track_color: Optional[ColorValue] = None
    refresh_bgcolor: Optional[ColorValue] = None
    linear_min_height: Optional[Number] = None
    border_radius: Optional[BorderRadiusValue] = None
    track_gap: Optional[Number] = None
    circular_track_padding: Optional[PaddingValue] = None
    size_constraints: Optional[BoxConstraints] = None
    stop_indicator_color: Optional[ColorValue] = None
    stop_indicator_radius: Optional[Number] = None
    stroke_align: Optional[Number] = None
    stroke_cap: Optional[StrokeCap] = None
    stroke_width: Optional[Number] = None
    year_2023: Optional[bool] = None


@dataclass
class PopupMenuTheme:
    color: Optional[ColorValue] = None
    surface_tint_color: Optional[ColorValue] = None
    shadow_color: Optional[ColorValue] = None
    icon_color: Optional[ColorValue] = None
    text_style: Optional[TextStyle] = None
    label_text_style: Optional[TextStyle] = None
    enable_feedback: Optional[bool] = None
    elevation: Optional[Number] = None
    icon_size: Optional[Number] = None
    shape: Optional[OutlinedBorder] = None
    menu_position: Optional[PopupMenuPosition] = None
    mouse_cursor: Optional[ControlStateValue[MouseCursor]] = None
    menu_padding: Optional[PaddingValue] = None


@dataclass
class SearchBarTheme:
    bgcolor: Optional[ColorValue] = None
    text_capitalization: Optional[TextCapitalization] = None
    shadow_color: Optional[ControlStateValue[ColorValue]] = None
    surface_tint_color: Optional[ControlStateValue[ColorValue]] = None
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
    surface_tint_color: Optional[ColorValue] = None
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
    surface_tint_color: Optional[ColorValue] = None
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
    surface_tint_color: Optional[ColorValue] = None
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
    selected_icon: Optional[IconValue] = None
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
    system_overlay_style: SystemOverlayStyle = field(default_factory=SystemOverlayStyle)
    tabs_theme: Optional[TabsTheme] = None
    text_theme: Optional[TextTheme] = None
    time_picker_theme: Optional[TimePickerTheme] = None
    tooltip_theme: Optional[TooltipTheme] = None
    visual_density: Optional[VisualDensity] = None
