from typing import TYPE_CHECKING

from flet.app import app, app_async, run, run_async
from flet.components.component import Component
from flet.components.component_decorator import component
from flet.components.hooks.use_callback import use_callback
from flet.components.hooks.use_context import create_context, use_context
from flet.components.hooks.use_effect import (
    on_mounted,
    on_unmounted,
    on_updated,
    use_effect,
)
from flet.components.hooks.use_memo import use_memo
from flet.components.hooks.use_ref import use_ref
from flet.components.hooks.use_state import use_state
from flet.components.memo import memo
from flet.components.observable import Observable, observable
from flet.components.public_utils import unwrap_component
from flet.controls import alignment, border, border_radius, margin, padding
from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.alignment import Alignment, Axis
from flet.controls.animation import (
    Animation,
    AnimationCurve,
    AnimationStyle,
    AnimationValue,
)
from flet.controls.base_control import BaseControl, control
from flet.controls.base_page import BasePage, PageMediaData, PageResizeEvent
from flet.controls.blur import (
    Blur,
    BlurTileMode,
    BlurValue,
)
from flet.controls.border import (
    Border,
    BorderSide,
    BorderSideStrokeAlign,
    BorderSideStrokeAlignValue,
    BorderStyle,
)
from flet.controls.border_radius import (
    BorderRadius,
    BorderRadiusValue,
)
from flet.controls.box import (
    BlurStyle,
    BoxConstraints,
    BoxDecoration,
    BoxFit,
    BoxShadow,
    BoxShadowValue,
    BoxShape,
    ColorFilter,
    DecorationImage,
    FilterQuality,
)
from flet.controls.buttons import (
    BeveledRectangleBorder,
    ButtonStyle,
    CircleBorder,
    ContinuousRectangleBorder,
    OutlinedBorder,
    RoundedRectangleBorder,
    ShapeBorder,
    StadiumBorder,
)
from flet.controls.colors import Colors
from flet.controls.context import Context, context
from flet.controls.control import Control
from flet.controls.control_event import (
    ControlEvent,
    ControlEventHandler,
    Event,
    EventControlType,
    EventHandler,
)
from flet.controls.control_state import (
    ControlState,
    ControlStateValue,
)
from flet.controls.core.animated_switcher import (
    AnimatedSwitcher,
    AnimatedSwitcherTransition,
)
from flet.controls.core.autofill_group import (
    AutofillGroup,
    AutofillGroupDisposeAction,
    AutofillHint,
)
from flet.controls.core.column import Column
from flet.controls.core.dismissible import (
    Dismissible,
    DismissibleDismissEvent,
    DismissibleUpdateEvent,
)
from flet.controls.core.drag_target import (
    DragTarget,
    DragTargetEvent,
    DragTargetLeaveEvent,
    DragWillAcceptEvent,
)
from flet.controls.core.draggable import Draggable
from flet.controls.core.flet_app import FletApp
from flet.controls.core.gesture_detector import GestureDetector
from flet.controls.core.grid_view import GridView
from flet.controls.core.icon import Icon
from flet.controls.core.image import Image
from flet.controls.core.interactive_viewer import InteractiveViewer
from flet.controls.core.keyboard_listener import (
    KeyboardListener,
    KeyDownEvent,
    KeyRepeatEvent,
    KeyUpEvent,
)
from flet.controls.core.list_view import ListView
from flet.controls.core.markdown import (
    Markdown,
    MarkdownCodeTheme,
    MarkdownCustomCodeTheme,
    MarkdownExtensionSet,
    MarkdownStyleSheet,
)
from flet.controls.core.merge_semantics import MergeSemantics
from flet.controls.core.pagelet import Pagelet
from flet.controls.core.placeholder import Placeholder
from flet.controls.core.reorderable_drag_handle import ReorderableDragHandle
from flet.controls.core.responsive_row import ResponsiveRow
from flet.controls.core.row import Row
from flet.controls.core.safe_area import SafeArea
from flet.controls.core.screenshot import Screenshot
from flet.controls.core.semantics import Semantics
from flet.controls.core.shader_mask import ShaderMask
from flet.controls.core.shimmer import Shimmer, ShimmerDirection
from flet.controls.core.stack import Stack, StackFit
from flet.controls.core.text import (
    Text,
    TextAffinity,
    TextSelection,
    TextSelectionChangeCause,
    TextSelectionChangeEvent,
)
from flet.controls.core.text_span import TextSpan
from flet.controls.core.transparent_pointer import TransparentPointer
from flet.controls.core.view import View
from flet.controls.core.window import (
    Window,
    WindowEvent,
    WindowEventType,
    WindowResizeEdge,
)
from flet.controls.core.window_drag_area import WindowDragArea
from flet.controls.cupertino import cupertino_colors
from flet.controls.cupertino.cupertino_action_sheet import CupertinoActionSheet
from flet.controls.cupertino.cupertino_action_sheet_action import (
    CupertinoActionSheetAction,
)
from flet.controls.cupertino.cupertino_activity_indicator import (
    CupertinoActivityIndicator,
)
from flet.controls.cupertino.cupertino_alert_dialog import CupertinoAlertDialog
from flet.controls.cupertino.cupertino_app_bar import CupertinoAppBar
from flet.controls.cupertino.cupertino_bottom_sheet import CupertinoBottomSheet
from flet.controls.cupertino.cupertino_button import (
    CupertinoButton,
    CupertinoButtonSize,
)
from flet.controls.cupertino.cupertino_checkbox import CupertinoCheckbox
from flet.controls.cupertino.cupertino_colors import CupertinoColors
from flet.controls.cupertino.cupertino_context_menu import CupertinoContextMenu
from flet.controls.cupertino.cupertino_context_menu_action import (
    CupertinoContextMenuAction,
)
from flet.controls.cupertino.cupertino_date_picker import (
    CupertinoDatePicker,
    CupertinoDatePickerDateOrder,
    CupertinoDatePickerMode,
)
from flet.controls.cupertino.cupertino_dialog_action import CupertinoDialogAction
from flet.controls.cupertino.cupertino_filled_button import CupertinoFilledButton
from flet.controls.cupertino.cupertino_list_tile import CupertinoListTile
from flet.controls.cupertino.cupertino_navigation_bar import CupertinoNavigationBar
from flet.controls.cupertino.cupertino_picker import CupertinoPicker
from flet.controls.cupertino.cupertino_radio import CupertinoRadio
from flet.controls.cupertino.cupertino_segmented_button import CupertinoSegmentedButton
from flet.controls.cupertino.cupertino_slider import CupertinoSlider
from flet.controls.cupertino.cupertino_sliding_segmented_button import (
    CupertinoSlidingSegmentedButton,
)
from flet.controls.cupertino.cupertino_switch import CupertinoSwitch
from flet.controls.cupertino.cupertino_textfield import (
    CupertinoTextField,
    OverlayVisibilityMode,
)
from flet.controls.cupertino.cupertino_timer_picker import (
    CupertinoTimerPicker,
    CupertinoTimerPickerMode,
)
from flet.controls.cupertino.cupertino_tinted_button import CupertinoTintedButton
from flet.controls.device_info import (
    AndroidBuildVersion,
    AndroidDeviceInfo,
    DeviceInfo,
    IosDeviceInfo,
    IosUtsname,
    LinuxDeviceInfo,
    MacOsDeviceInfo,
    WebBrowserName,
    WebDeviceInfo,
    WindowsDeviceInfo,
)
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import (
    DateTimeValue,
    Duration,
    DurationValue,
)
from flet.controls.events import (
    DragDownEvent,
    DragEndEvent,
    DragStartEvent,
    DragUpdateEvent,
    ForcePressEvent,
    HoverEvent,
    LongPressDownEvent,
    LongPressEndEvent,
    LongPressMoveUpdateEvent,
    LongPressStartEvent,
    MultiTapEvent,
    PointerEvent,
    ScaleEndEvent,
    ScaleStartEvent,
    ScaleUpdateEvent,
    ScrollEvent,
    TapEvent,
    TapMoveEvent,
)
from flet.controls.exceptions import (
    FletException,
    FletPageDisconnectedException,
    FletUnimplementedPlatformException,
    FletUnsupportedPlatformException,
)
from flet.controls.geometry import Rect, Size
from flet.controls.gradients import (
    Gradient,
    GradientTileMode,
    LinearGradient,
    RadialGradient,
    SweepGradient,
)
from flet.controls.icon_data import IconData
from flet.controls.id_counter import IdCounter
from flet.controls.keys import Key, KeyValue, ScrollKey, ValueKey
from flet.controls.layout_control import ConstrainedControl, LayoutControl
from flet.controls.margin import Margin, MarginValue
from flet.controls.material import dropdown, dropdownm2
from flet.controls.material.alert_dialog import AlertDialog
from flet.controls.material.app_bar import AppBar
from flet.controls.material.auto_complete import (
    AutoComplete,
    AutoCompleteSelectEvent,
    AutoCompleteSuggestion,
)
from flet.controls.material.badge import Badge, BadgeValue
from flet.controls.material.banner import Banner
from flet.controls.material.bottom_app_bar import BottomAppBar
from flet.controls.material.bottom_sheet import BottomSheet
from flet.controls.material.button import Button
from flet.controls.material.card import Card, CardVariant
from flet.controls.material.checkbox import Checkbox
from flet.controls.material.chip import Chip
from flet.controls.material.circle_avatar import CircleAvatar
from flet.controls.material.container import Container
from flet.controls.material.context_menu import (
    ContextMenu,
    ContextMenuDismissEvent,
    ContextMenuSelectEvent,
    ContextMenuTrigger,
)
from flet.controls.material.datatable import (
    DataCell,
    DataColumn,
    DataColumnSortEvent,
    DataRow,
    DataTable,
)
from flet.controls.material.date_picker import (
    DatePicker,
    DatePickerEntryMode,
    DatePickerEntryModeChangeEvent,
    DatePickerMode,
)
from flet.controls.material.date_range_picker import DateRangePicker
from flet.controls.material.divider import Divider
from flet.controls.material.dropdown import Dropdown, DropdownOption
from flet.controls.material.dropdownm2 import DropdownM2
from flet.controls.material.elevated_button import ElevatedButton
from flet.controls.material.expansion_panel import ExpansionPanel, ExpansionPanelList
from flet.controls.material.expansion_tile import ExpansionTile, TileAffinity
from flet.controls.material.filled_button import FilledButton
from flet.controls.material.filled_tonal_button import FilledTonalButton
from flet.controls.material.floating_action_button import FloatingActionButton
from flet.controls.material.form_field_control import FormFieldControl, InputBorder
from flet.controls.material.icon_button import (
    FilledIconButton,
    FilledTonalIconButton,
    IconButton,
    OutlinedIconButton,
)
from flet.controls.material.list_tile import (
    ListTile,
    ListTileStyle,
    ListTileTitleAlignment,
)
from flet.controls.material.menu_bar import MenuBar, MenuStyle
from flet.controls.material.menu_item_button import MenuItemButton
from flet.controls.material.navigation_bar import (
    NavigationBar,
    NavigationBarDestination,
    NavigationBarLabelBehavior,
)
from flet.controls.material.navigation_drawer import (
    NavigationDrawer,
    NavigationDrawerDestination,
)
from flet.controls.material.navigation_rail import (
    NavigationRail,
    NavigationRailDestination,
    NavigationRailLabelType,
)
from flet.controls.material.outlined_button import OutlinedButton
from flet.controls.material.popup_menu_button import (
    PopupMenuButton,
    PopupMenuItem,
    PopupMenuPosition,
)
from flet.controls.material.progress_bar import ProgressBar
from flet.controls.material.progress_ring import ProgressRing
from flet.controls.material.radio import Radio
from flet.controls.material.radio_group import RadioGroup
from flet.controls.material.range_slider import RangeSlider
from flet.controls.material.reorderable_list_view import (
    OnReorderEvent,
    ReorderableListView,
)
from flet.controls.material.search_bar import SearchBar
from flet.controls.material.segmented_button import Segment, SegmentedButton
from flet.controls.material.selection_area import SelectionArea
from flet.controls.material.slider import Slider, SliderInteraction
from flet.controls.material.snack_bar import (
    DismissDirection,
    SnackBar,
    SnackBarAction,
    SnackBarBehavior,
)
from flet.controls.material.submenu_button import SubmenuButton
from flet.controls.material.switch import Switch
from flet.controls.material.tabs import (
    Tab,
    TabAlignment,
    TabBar,
    TabBarHoverEvent,
    TabBarIndicatorSize,
    TabBarView,
    TabIndicatorAnimation,
    Tabs,
    UnderlineTabIndicator,
)
from flet.controls.material.text_button import TextButton
from flet.controls.material.textfield import (
    InputFilter,
    KeyboardType,
    NumbersOnlyInputFilter,
    TextCapitalization,
    TextField,
    TextOnlyInputFilter,
)
from flet.controls.material.time_picker import (
    TimePicker,
    TimePickerEntryMode,
    TimePickerEntryModeChangeEvent,
    TimePickerHourFormat,
)
from flet.controls.material.tooltip import Tooltip, TooltipTriggerMode, TooltipValue
from flet.controls.material.vertical_divider import VerticalDivider
from flet.controls.multi_view import MultiView
from flet.controls.padding import Padding, PaddingValue
from flet.controls.page import (
    AppLifecycleStateChangeEvent,
    KeyboardEvent,
    LoginEvent,
    MultiViewAddEvent,
    MultiViewRemoveEvent,
    Page,
    PlatformBrightnessChangeEvent,
    RouteChangeEvent,
    ViewPopEvent,
)
from flet.controls.painting import (
    Paint,
    PaintGradient,
    PaintingStyle,
    PaintLinearGradient,
    PaintRadialGradient,
    PaintSweepGradient,
)
from flet.controls.query_string import QueryString
from flet.controls.ref import Ref
from flet.controls.scrollable_control import (
    OnScrollEvent,
    ScrollableControl,
    ScrollDirection,
    ScrollType,
)
from flet.controls.services.accelerometer import (
    Accelerometer,
    AccelerometerReadingEvent,
)
from flet.controls.services.barometer import Barometer, BarometerReadingEvent
from flet.controls.services.battery import (
    Battery,
    BatteryState,
    BatteryStateChangeEvent,
)
from flet.controls.services.browser_context_menu import BrowserContextMenu
from flet.controls.services.clipboard import Clipboard
from flet.controls.services.connectivity import (
    Connectivity,
    ConnectivityChangeEvent,
    ConnectivityType,
)
from flet.controls.services.file_picker import (
    FilePicker,
    FilePickerFile,
    FilePickerFileType,
    FilePickerUploadEvent,
    FilePickerUploadFile,
)
from flet.controls.services.gyroscope import Gyroscope, GyroscopeReadingEvent
from flet.controls.services.haptic_feedback import HapticFeedback
from flet.controls.services.magnetometer import Magnetometer, MagnetometerReadingEvent
from flet.controls.services.screen_brightness import (
    ScreenBrightness,
    ScreenBrightnessChangeEvent,
)
from flet.controls.services.semantics_service import Assertiveness, SemanticsService
from flet.controls.services.sensor_error_event import SensorErrorEvent
from flet.controls.services.service import Service
from flet.controls.services.shake_detector import ShakeDetector
from flet.controls.services.share import (
    Share,
    ShareCupertinoActivityType,
    ShareFile,
    ShareResult,
    ShareResultStatus,
)
from flet.controls.services.shared_preferences import SharedPreferences
from flet.controls.services.storage_paths import StoragePaths
from flet.controls.services.url_launcher import (
    BrowserConfiguration,
    LaunchMode,
    UrlLauncher,
    WebViewConfiguration,
)
from flet.controls.services.user_accelerometer import (
    UserAccelerometer,
    UserAccelerometerReadingEvent,
)
from flet.controls.services.wakelock import Wakelock
from flet.controls.template_route import TemplateRoute
from flet.controls.text_style import (
    StrutStyle,
    TextBaseline,
    TextDecoration,
    TextDecorationStyle,
    TextOverflow,
    TextStyle,
    TextThemeStyle,
)
from flet.controls.transform import (
    Offset,
    OffsetValue,
    Rotate,
    RotateValue,
    Scale,
    ScaleValue,
)
from flet.controls.types import (
    AppLifecycleState,
    AppView,
    AutomaticNotchShape,
    BlendMode,
    Brightness,
    CircularRectangleNotchShape,
    ClipBehavior,
    ColorValue,
    CrossAxisAlignment,
    DeviceOrientation,
    FloatingActionButtonLocation,
    FontWeight,
    IconDataOrControl,
    ImageRepeat,
    LabelPosition,
    Locale,
    LocaleConfiguration,
    MainAxisAlignment,
    MouseCursor,
    NotchShape,
    Number,
    Orientation,
    PagePlatform,
    PointerDeviceType,
    ResponsiveNumber,
    ResponsiveRowBreakpoint,
    RouteUrlStrategy,
    ScrollMode,
    StrokeCap,
    StrokeJoin,
    StrOrControl,
    SupportsStr,
    TextAlign,
    ThemeMode,
    Url,
    UrlTarget,
    VerticalAlignment,
    VisualDensity,
    WebRenderer,
)
from flet.pubsub.pubsub_client import PubSubClient
from flet.pubsub.pubsub_hub import PubSubHub
from flet.version import flet_version as __version__

if TYPE_CHECKING:
    from flet.controls.cupertino import cupertino_icons
    from flet.controls.cupertino.cupertino_icons import CupertinoIcons
    from flet.controls.material import icons
    from flet.controls.material.icons import Icons
    from flet.controls.theme import (
        AppBarTheme,
        BadgeTheme,
        BannerTheme,
        BottomAppBarTheme,
        BottomSheetTheme,
        ButtonTheme,
        CardTheme,
        CheckboxTheme,
        ChipTheme,
        ColorScheme,
        DataTableTheme,
        DatePickerTheme,
        DialogTheme,
        DividerTheme,
        DropdownTheme,
        ExpansionTileTheme,
        FilledButtonTheme,
        FloatingActionButtonTheme,
        IconButtonTheme,
        IconTheme,
        ListTileTheme,
        NavigationBarTheme,
        NavigationDrawerTheme,
        NavigationRailTheme,
        OutlinedButtonTheme,
        PageTransitionsTheme,
        PageTransitionTheme,
        PopupMenuTheme,
        ProgressIndicatorTheme,
        RadioTheme,
        ScrollbarTheme,
        SearchBarTheme,
        SearchViewTheme,
        SegmentedButtonTheme,
        SliderTheme,
        SnackBarTheme,
        SwitchTheme,
        SystemOverlayStyle,
        TabBarTheme,
        TextButtonTheme,
        TextTheme,
        Theme,
        TimePickerTheme,
        TooltipTheme,
    )

__all__ = [
    "Accelerometer",
    "AccelerometerReadingEvent",
    "AdaptiveControl",
    "AlertDialog",
    "Alignment",
    "AndroidBuildVersion",
    "AndroidDeviceInfo",
    "AnimatedSwitcher",
    "AnimatedSwitcherTransition",
    "Animation",
    "AnimationCurve",
    "AnimationStyle",
    "AnimationValue",
    "AppBar",
    "AppBarTheme",
    "AppLifecycleState",
    "AppLifecycleStateChangeEvent",
    "AppView",
    "Assertiveness",
    "AutoComplete",
    "AutoCompleteSelectEvent",
    "AutoCompleteSuggestion",
    "AutofillGroup",
    "AutofillGroupDisposeAction",
    "AutofillHint",
    "AutomaticNotchShape",
    "Axis",
    "Badge",
    "BadgeTheme",
    "BadgeValue",
    "Banner",
    "BannerTheme",
    "Barometer",
    "BarometerReadingEvent",
    "BaseControl",
    "BasePage",
    "Battery",
    "BatteryState",
    "BatteryStateChangeEvent",
    "BeveledRectangleBorder",
    "BlendMode",
    "Blur",
    "BlurStyle",
    "BlurTileMode",
    "BlurValue",
    "Border",
    "BorderRadius",
    "BorderRadiusValue",
    "BorderSide",
    "BorderSideStrokeAlign",
    "BorderSideStrokeAlignValue",
    "BorderStyle",
    "BottomAppBar",
    "BottomAppBarTheme",
    "BottomSheet",
    "BottomSheetTheme",
    "BoxConstraints",
    "BoxDecoration",
    "BoxFit",
    "BoxShadow",
    "BoxShadowValue",
    "BoxShape",
    "Brightness",
    "BrowserConfiguration",
    "BrowserContextMenu",
    "Button",
    "ButtonStyle",
    "ButtonTheme",
    "Card",
    "CardTheme",
    "CardVariant",
    "Checkbox",
    "CheckboxTheme",
    "Chip",
    "ChipTheme",
    "CircleAvatar",
    "CircleBorder",
    "CircularRectangleNotchShape",
    "ClipBehavior",
    "Clipboard",
    "ColorFilter",
    "ColorScheme",
    "ColorValue",
    "Colors",
    "Column",
    "Component",
    "Connectivity",
    "ConnectivityChangeEvent",
    "ConnectivityType",
    "ConstrainedControl",
    "Container",
    "Context",
    "ContextMenu",
    "ContextMenuDismissEvent",
    "ContextMenuSelectEvent",
    "ContextMenuTrigger",
    "ContinuousRectangleBorder",
    "Control",
    "ControlEvent",
    "ControlEventHandler",
    "ControlState",
    "ControlStateValue",
    "CrossAxisAlignment",
    "CupertinoActionSheet",
    "CupertinoActionSheetAction",
    "CupertinoActivityIndicator",
    "CupertinoAlertDialog",
    "CupertinoAppBar",
    "CupertinoBottomSheet",
    "CupertinoButton",
    "CupertinoButtonSize",
    "CupertinoCheckbox",
    "CupertinoColors",
    "CupertinoContextMenu",
    "CupertinoContextMenuAction",
    "CupertinoDatePicker",
    "CupertinoDatePickerDateOrder",
    "CupertinoDatePickerMode",
    "CupertinoDialogAction",
    "CupertinoFilledButton",
    "CupertinoIcons",
    "CupertinoListTile",
    "CupertinoNavigationBar",
    "CupertinoPicker",
    "CupertinoRadio",
    "CupertinoSegmentedButton",
    "CupertinoSlider",
    "CupertinoSlidingSegmentedButton",
    "CupertinoSwitch",
    "CupertinoTextField",
    "CupertinoTimerPicker",
    "CupertinoTimerPickerMode",
    "CupertinoTintedButton",
    "DataCell",
    "DataColumn",
    "DataColumnSortEvent",
    "DataRow",
    "DataTable",
    "DataTableTheme",
    "DatePicker",
    "DatePickerEntryMode",
    "DatePickerEntryModeChangeEvent",
    "DatePickerMode",
    "DatePickerTheme",
    "DateRangePicker",
    "DateTimeValue",
    "DecorationImage",
    "DeviceInfo",
    "DeviceOrientation",
    "DialogControl",
    "DialogTheme",
    "DismissDirection",
    "Dismissible",
    "DismissibleDismissEvent",
    "DismissibleUpdateEvent",
    "Divider",
    "DividerTheme",
    "DragDownEvent",
    "DragEndEvent",
    "DragStartEvent",
    "DragTarget",
    "DragTargetEvent",
    "DragTargetLeaveEvent",
    "DragUpdateEvent",
    "DragWillAcceptEvent",
    "Draggable",
    "Dropdown",
    "DropdownM2",
    "DropdownOption",
    "DropdownTheme",
    "Duration",
    "DurationValue",
    "ElevatedButton",
    "Event",
    "EventControlType",
    "EventHandler",
    "ExpansionPanel",
    "ExpansionPanelList",
    "ExpansionTile",
    "ExpansionTileTheme",
    "FilePicker",
    "FilePickerFile",
    "FilePickerFileType",
    "FilePickerUploadEvent",
    "FilePickerUploadFile",
    "FilledButton",
    "FilledButtonTheme",
    "FilledIconButton",
    "FilledTonalButton",
    "FilledTonalIconButton",
    "FilterQuality",
    "FletApp",
    "FletException",
    "FletPageDisconnectedException",
    "FletUnimplementedPlatformException",
    "FletUnsupportedPlatformException",
    "FloatingActionButton",
    "FloatingActionButtonLocation",
    "FloatingActionButtonTheme",
    "FontWeight",
    "ForcePressEvent",
    "FormFieldControl",
    "GestureDetector",
    "Gradient",
    "GradientTileMode",
    "GridView",
    "Gyroscope",
    "GyroscopeReadingEvent",
    "HapticFeedback",
    "HoverEvent",
    "Icon",
    "IconButton",
    "IconButtonTheme",
    "IconData",
    "IconDataOrControl",
    "IconTheme",
    "Icons",
    "IdCounter",
    "Image",
    "ImageRepeat",
    "InputBorder",
    "InputFilter",
    "InteractiveViewer",
    "IosDeviceInfo",
    "IosUtsname",
    "Key",
    "KeyDownEvent",
    "KeyRepeatEvent",
    "KeyUpEvent",
    "KeyValue",
    "KeyboardEvent",
    "KeyboardListener",
    "KeyboardType",
    "LabelPosition",
    "LaunchMode",
    "LayoutControl",
    "LinearGradient",
    "LinuxDeviceInfo",
    "ListTile",
    "ListTileStyle",
    "ListTileTheme",
    "ListTileTitleAlignment",
    "ListView",
    "Locale",
    "LocaleConfiguration",
    "LoginEvent",
    "LongPressDownEvent",
    "LongPressEndEvent",
    "LongPressMoveUpdateEvent",
    "LongPressStartEvent",
    "MacOsDeviceInfo",
    "Magnetometer",
    "MagnetometerReadingEvent",
    "MainAxisAlignment",
    "Margin",
    "MarginValue",
    "Markdown",
    "MarkdownCodeTheme",
    "MarkdownCustomCodeTheme",
    "MarkdownExtensionSet",
    "MarkdownStyleSheet",
    "MenuBar",
    "MenuItemButton",
    "MenuStyle",
    "MergeSemantics",
    "MouseCursor",
    "MultiTapEvent",
    "MultiView",
    "MultiViewAddEvent",
    "MultiViewRemoveEvent",
    "NavigationBar",
    "NavigationBarDestination",
    "NavigationBarLabelBehavior",
    "NavigationBarTheme",
    "NavigationDrawer",
    "NavigationDrawerDestination",
    "NavigationDrawerTheme",
    "NavigationRail",
    "NavigationRailDestination",
    "NavigationRailLabelType",
    "NavigationRailTheme",
    "NotchShape",
    "Number",
    "NumbersOnlyInputFilter",
    "Observable",
    "Offset",
    "OffsetValue",
    "OnReorderEvent",
    "OnScrollEvent",
    "Orientation",
    "OutlinedBorder",
    "OutlinedButton",
    "OutlinedButtonTheme",
    "OutlinedIconButton",
    "OverlayVisibilityMode",
    "Padding",
    "PaddingValue",
    "Page",
    "PageMediaData",
    "PagePlatform",
    "PageResizeEvent",
    "PageTransitionTheme",
    "PageTransitionsTheme",
    "Pagelet",
    "Paint",
    "PaintGradient",
    "PaintLinearGradient",
    "PaintRadialGradient",
    "PaintSweepGradient",
    "PaintingStyle",
    "Placeholder",
    "PlatformBrightnessChangeEvent",
    "PointerDeviceType",
    "PointerEvent",
    "PopupMenuButton",
    "PopupMenuItem",
    "PopupMenuPosition",
    "PopupMenuTheme",
    "ProgressBar",
    "ProgressIndicatorTheme",
    "ProgressRing",
    "PubSubClient",
    "PubSubHub",
    "QueryString",
    "RadialGradient",
    "Radio",
    "RadioGroup",
    "RadioTheme",
    "RangeSlider",
    "Rect",
    "Ref",
    "ReorderableDragHandle",
    "ReorderableListView",
    "ResponsiveNumber",
    "ResponsiveRow",
    "ResponsiveRowBreakpoint",
    "Rotate",
    "RotateValue",
    "RoundedRectangleBorder",
    "RouteChangeEvent",
    "RouteUrlStrategy",
    "Row",
    "SafeArea",
    "Scale",
    "ScaleEndEvent",
    "ScaleStartEvent",
    "ScaleUpdateEvent",
    "ScaleValue",
    "ScreenBrightness",
    "ScreenBrightnessChangeEvent",
    "Screenshot",
    "ScrollDirection",
    "ScrollEvent",
    "ScrollKey",
    "ScrollMode",
    "ScrollType",
    "ScrollableControl",
    "ScrollbarTheme",
    "SearchBar",
    "SearchBarTheme",
    "SearchViewTheme",
    "Segment",
    "SegmentedButton",
    "SegmentedButtonTheme",
    "SelectionArea",
    "Semantics",
    "SemanticsService",
    "SensorErrorEvent",
    "Service",
    "ShaderMask",
    "ShakeDetector",
    "ShapeBorder",
    "Share",
    "ShareCupertinoActivityType",
    "ShareFile",
    "ShareResult",
    "ShareResultStatus",
    "SharedPreferences",
    "Shimmer",
    "ShimmerDirection",
    "Size",
    "Slider",
    "SliderInteraction",
    "SliderTheme",
    "SnackBar",
    "SnackBarAction",
    "SnackBarBehavior",
    "SnackBarTheme",
    "Stack",
    "StackFit",
    "StadiumBorder",
    "StoragePaths",
    "StrOrControl",
    "StrokeCap",
    "StrokeJoin",
    "StrutStyle",
    "SubmenuButton",
    "SupportsStr",
    "SweepGradient",
    "Switch",
    "SwitchTheme",
    "SystemOverlayStyle",
    "Tab",
    "TabAlignment",
    "TabBar",
    "TabBarHoverEvent",
    "TabBarIndicatorSize",
    "TabBarTheme",
    "TabBarView",
    "TabIndicatorAnimation",
    "Tabs",
    "TapEvent",
    "TapMoveEvent",
    "TemplateRoute",
    "Text",
    "TextAffinity",
    "TextAlign",
    "TextBaseline",
    "TextButton",
    "TextButtonTheme",
    "TextCapitalization",
    "TextDecoration",
    "TextDecorationStyle",
    "TextField",
    "TextOnlyInputFilter",
    "TextOverflow",
    "TextSelection",
    "TextSelectionChangeCause",
    "TextSelectionChangeEvent",
    "TextSpan",
    "TextStyle",
    "TextTheme",
    "TextThemeStyle",
    "Theme",
    "ThemeMode",
    "TileAffinity",
    "TimePicker",
    "TimePickerEntryMode",
    "TimePickerEntryModeChangeEvent",
    "TimePickerHourFormat",
    "TimePickerTheme",
    "Tooltip",
    "TooltipTheme",
    "TooltipTriggerMode",
    "TooltipValue",
    "TransparentPointer",
    "UnderlineTabIndicator",
    "Url",
    "UrlLauncher",
    "UrlTarget",
    "UserAccelerometer",
    "UserAccelerometerReadingEvent",
    "ValueKey",
    "VerticalAlignment",
    "VerticalDivider",
    "View",
    "ViewPopEvent",
    "VisualDensity",
    "Wakelock",
    "WebBrowserName",
    "WebDeviceInfo",
    "WebRenderer",
    "WebViewConfiguration",
    "Window",
    "WindowDragArea",
    "WindowEvent",
    "WindowEventType",
    "WindowResizeEdge",
    "WindowsDeviceInfo",
    "__version__",
    "alignment",
    "app",
    "app_async",
    "border",
    "border_radius",
    "component",
    "context",
    "control",
    "create_context",
    "cupertino_colors",
    "cupertino_icons",
    "dropdown",
    "dropdownm2",
    "icons",
    "margin",
    "memo",
    "observable",
    "on_mounted",
    "on_unmounted",
    "on_updated",
    "padding",
    "run",
    "run_async",
    "unwrap_component",
    "use_callback",
    "use_context",
    "use_effect",
    "use_memo",
    "use_ref",
    "use_state",
]

_THEME_EXPORTS = {
    "AppBarTheme",
    "BadgeTheme",
    "BannerTheme",
    "BottomAppBarTheme",
    "BottomSheetTheme",
    "ButtonTheme",
    "CardTheme",
    "CheckboxTheme",
    "ChipTheme",
    "ColorScheme",
    "DataTableTheme",
    "DatePickerTheme",
    "DialogTheme",
    "DividerTheme",
    "DropdownTheme",
    "ExpansionTileTheme",
    "FilledButtonTheme",
    "FloatingActionButtonTheme",
    "IconButtonTheme",
    "IconTheme",
    "ListTileTheme",
    "NavigationBarTheme",
    "NavigationDrawerTheme",
    "NavigationRailTheme",
    "OutlinedButtonTheme",
    "PageTransitionsTheme",
    "PageTransitionTheme",
    "PopupMenuTheme",
    "ProgressIndicatorTheme",
    "RadioTheme",
    "ScrollbarTheme",
    "SearchBarTheme",
    "SearchViewTheme",
    "SegmentedButtonTheme",
    "SliderTheme",
    "SnackBarTheme",
    "SwitchTheme",
    "SystemOverlayStyle",
    "TabBarTheme",
    "TextButtonTheme",
    "TextTheme",
    "Theme",
    "TimePickerTheme",
    "TooltipTheme",
}


def __getattr__(name: str):
    if name in _THEME_EXPORTS:
        from flet.controls import theme

        return getattr(theme, name)
    if name == "Icons":
        from flet.controls.material.icons import Icons

        return Icons
    if name == "CupertinoIcons":
        from flet.controls.cupertino.cupertino_icons import CupertinoIcons

        return CupertinoIcons
    if name == "icons":
        import importlib

        return importlib.import_module("flet.controls.material.icons")
    if name == "cupertino_icons":
        import importlib

        return importlib.import_module("flet.controls.cupertino.cupertino_icons")
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
