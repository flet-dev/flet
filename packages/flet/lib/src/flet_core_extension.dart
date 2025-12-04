import 'package:flutter/widgets.dart';

import 'controls/adaptive_alert_dialog.dart';
import 'controls/adaptive_button.dart';
import 'controls/adaptive_checkbox.dart';
import 'controls/adaptive_radio.dart';
import 'controls/adaptive_slider.dart';
import 'controls/adaptive_switch.dart';
import 'controls/adaptive_texfield.dart';
import 'controls/animated_switcher.dart';
import 'controls/app_bar.dart';
import 'controls/auto_complete.dart';
import 'controls/autofill_group.dart';
import 'controls/banner.dart';
import 'controls/bottom_app_bar.dart';
import 'controls/bottom_sheet.dart';
import 'controls/canvas.dart';
import 'controls/card.dart';
import 'controls/chip.dart';
import 'controls/circle_avatar.dart';
import 'controls/column.dart';
import 'controls/container.dart';
import 'controls/context_menu.dart';
import 'controls/cupertino_action_sheet.dart';
import 'controls/cupertino_action_sheet_action.dart';
import 'controls/cupertino_activity_indicator.dart';
import 'controls/cupertino_alert_dialog.dart';
import 'controls/cupertino_app_bar.dart';
import 'controls/cupertino_bottom_sheet.dart';
import 'controls/cupertino_button.dart';
import 'controls/cupertino_checkbox.dart';
import 'controls/cupertino_context_menu.dart';
import 'controls/cupertino_context_menu_action.dart';
import 'controls/cupertino_date_picker.dart';
import 'controls/cupertino_dialog_action.dart';
import 'controls/cupertino_list_tile.dart';
import 'controls/cupertino_navigation_bar.dart';
import 'controls/cupertino_picker.dart';
import 'controls/cupertino_radio.dart';
import 'controls/cupertino_segmented_button.dart';
import 'controls/cupertino_slider.dart';
import 'controls/cupertino_sliding_segmented_button.dart';
import 'controls/cupertino_switch.dart';
import 'controls/cupertino_textfield.dart';
import 'controls/cupertino_timer_picker.dart';
import 'controls/datatable.dart';
import 'controls/date_picker.dart';
import 'controls/date_range_picker.dart';
import 'controls/dismissible.dart';
import 'controls/divider.dart';
import 'controls/drag_target.dart';
import 'controls/draggable.dart';
import 'controls/dropdown.dart';
import 'controls/dropdownm2.dart';
import 'controls/expansion_panel.dart';
import 'controls/expansion_tile.dart';
import 'controls/flet_app_control.dart';
import 'controls/floating_action_button.dart';
import 'controls/gesture_detector.dart';
import 'controls/grid_view.dart';
import 'controls/icon.dart';
import 'controls/icon_button.dart';
import 'controls/image.dart';
import 'controls/interactive_viewer.dart';
import 'controls/keyboard_listener.dart';
import 'controls/list_tile.dart';
import 'controls/list_view.dart';
import 'controls/markdown.dart';
import 'controls/menu_bar.dart';
import 'controls/menu_item_button.dart';
import 'controls/merge_semantics.dart';
import 'controls/navigation_bar.dart';
import 'controls/navigation_bar_destination.dart';
import 'controls/navigation_drawer.dart';
import 'controls/navigation_rail.dart';
import 'controls/page.dart';
import 'controls/pagelet.dart';
import 'controls/placeholder.dart';
import 'controls/popup_menu_button.dart';
import 'controls/progress_bar.dart';
import 'controls/progress_ring.dart';
import 'controls/radio_group.dart';
import 'controls/range_slider.dart';
import 'controls/reorderable_drag_handle.dart';
import 'controls/reorderable_list_view.dart';
import 'controls/responsive_row.dart';
import 'controls/row.dart';
import 'controls/safe_area.dart';
import 'controls/screenshot.dart';
import 'controls/search_bar.dart';
import 'controls/segmented_button.dart';
import 'controls/selection_area.dart';
import 'controls/semantics.dart';
import 'controls/shader_mask.dart';
import 'controls/shimmer.dart';
import 'controls/snack_bar.dart';
import 'controls/stack.dart';
import 'controls/submenu_button.dart';
import 'controls/tabs.dart';
import 'controls/text.dart';
import 'controls/time_picker.dart';
import 'controls/transparent_pointer.dart';
import 'controls/vertical_divider.dart';
import 'controls/view.dart';
import 'controls/window_drag_area.dart';
import 'flet_extension.dart';
import 'flet_service.dart';
import 'models/control.dart';
import 'services/browser_context_menu.dart';
import 'services/battery.dart';
import 'services/clipboard.dart';
import 'services/file_picker.dart';
import 'services/haptic_feedback.dart';
import 'services/semantics_service.dart';
import 'services/shake_detector.dart';
import 'services/sensors.dart';
import 'services/shared_preferences.dart';
import 'services/screen_brightness.dart';
import 'services/storage_paths.dart';
import 'services/tester.dart';
import 'services/url_launcher.dart';
import 'services/wakelock.dart';
import 'services/window.dart';
import 'utils/cupertino_icons.dart';
import 'utils/material_icons.dart';

class FletCoreExtension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "AdaptiveAlertDialog":
        return AdaptiveAlertDialogControl(key: key, control: control);
      case "AdaptiveButton":
      case "FilledButton":
      case "FilledTonalButton":
      case "OutlinedButton":
      case "TextButton":
        return AdaptiveButtonControl(key: key, control: control);
      case "AdaptiveCheckbox":
        return AdaptiveCheckboxControl(key: key, control: control);
      case "AdaptiveRadio":
        return AdaptiveRadioControl(key: key, control: control);
      case "AdaptiveSlider":
        return AdaptiveSliderControl(key: key, control: control);
      case "AdaptiveSwitch":
        return AdaptiveSwitchControl(key: key, control: control);
      case "AdaptiveTextField":
        return AdaptiveTextFieldControl(key: key, control: control);
      case "AlertDialog":
        return AdaptiveAlertDialogControl(key: key, control: control);
      case "AnimatedSwitcher":
        return AnimatedSwitcherControl(key: key, control: control);
      case "AppBar":
        return AppBarControl(key: key, control: control);
      case "AutoComplete":
        return AutoCompleteControl(key: key, control: control);
      case "AutofillGroup":
        return AutofillGroupControl(key: key, control: control);
      case "Banner":
        return BannerControl(key: key, control: control);
      case "BottomAppBar":
        return BottomAppBarControl(key: key, control: control);
      case "BottomSheet":
        return BottomSheetControl(key: key, control: control);
      case "Button":
        return AdaptiveButtonControl(key: key, control: control);
      case "Canvas":
        return CanvasControl(key: key, control: control);
      case "Card":
        return CardControl(key: key, control: control);
      case "Checkbox":
        return AdaptiveCheckboxControl(key: key, control: control);
      case "Chip":
        return ChipControl(key: key, control: control);
      case "CircleAvatar":
        return CircleAvatarControl(key: key, control: control);
      case "Column":
        return ColumnControl(key: key, control: control);
      case "Container":
        return ContainerControl(key: key, control: control);
      case "ContextMenu":
        return ContextMenuControl(key: key, control: control);
      case "CupertinoActionSheet":
        return CupertinoActionSheetControl(key: key, control: control);
      case "CupertinoActionSheetAction":
        return CupertinoActionSheetActionControl(key: key, control: control);
      case "CupertinoActivityIndicator":
        return CupertinoActivityIndicatorControl(key: key, control: control);
      case "CupertinoAlertDialog":
        return CupertinoAlertDialogControl(key: key, control: control);
      case "CupertinoAppBar":
        return CupertinoAppBarControl(key: key, control: control);
      case "CupertinoBottomSheet":
        return CupertinoBottomSheetControl(key: key, control: control);
      case "CupertinoButton":
      case "CupertinoFilledButton":
      case "CupertinoTintedButton":
        return CupertinoButtonControl(key: key, control: control);
      case "CupertinoCheckbox":
        return CupertinoCheckboxControl(key: key, control: control);
      case "CupertinoContextMenu":
        return CupertinoContextMenuControl(key: key, control: control);
      case "CupertinoContextMenuAction":
        return CupertinoContextMenuActionControl(key: key, control: control);
      case "CupertinoDatePicker":
        return CupertinoDatePickerControl(key: key, control: control);
      case "CupertinoDialogAction":
        return CupertinoDialogActionControl(key: key, control: control);
      case "CupertinoListTile":
        return CupertinoListTileControl(key: key, control: control);
      case "CupertinoNavigationBar":
        return CupertinoNavigationBarControl(key: key, control: control);
      case "CupertinoPicker":
        return CupertinoPickerControl(key: key, control: control);
      case "CupertinoRadio":
        return CupertinoRadioControl(key: key, control: control);
      case "CupertinoSegmentedButton":
        return CupertinoSegmentedButtonControl(key: key, control: control);
      case "CupertinoSlider":
        return CupertinoSliderControl(key: key, control: control);
      case "CupertinoSlidingSegmentedButton":
        return CupertinoSlidingSegmentedButtonControl(
            key: key, control: control);
      case "CupertinoSwitch":
        return CupertinoSwitchControl(key: key, control: control);
      case "CupertinoTextField":
        return CupertinoTextFieldControl(key: key, control: control);
      case "CupertinoTimerPicker":
        return CupertinoTimerPickerControl(key: key, control: control);
      case "DataTable":
        return DataTableControl(key: key, control: control);
      case "DatePicker":
        return DatePickerControl(key: key, control: control);
      case "DateRangePicker":
        return DateRangePickerControl(key: key, control: control);
      case "Dismissible":
        return DismissibleControl(key: key, control: control);
      case "Divider":
        return DividerControl(key: key, control: control);
      case "DragTarget":
        return DragTargetControl(key: key, control: control);
      case "Draggable":
        return DraggableControl(key: key, control: control);
      case "Dropdown":
        return DropdownControl(key: key, control: control);
      case "DropdownM2":
        return DropdownM2Control(key: key, control: control);
      case "ExpansionPanelList":
        return ExpansionPanelListControl(key: key, control: control);
      case "ExpansionTile":
        return ExpansionTileControl(key: key, control: control);
      case "FletApp":
        return FletAppControl(key: key, control: control);
      case "FloatingActionButton":
        return FloatingActionButtonControl(key: key, control: control);
      case "GestureDetector":
        return GestureDetectorControl(key: key, control: control);
      case "GridView":
        return GridViewControl(key: key, control: control);
      case "Icon":
        return IconControl(key: key, control: control);
      case "IconButton":
      case "FilledIconButton":
      case "FilledTonalIconButton":
      case "OutlinedIconButton":
        return IconButtonControl(key: key, control: control);
      case "Image":
        return ImageControl(key: key, control: control);
      case "InteractiveViewer":
        return InteractiveViewerControl(key: key, control: control);
      case "KeyboardListener":
        return KeyboardListenerControl(key: key, control: control);
      case "ListTile":
        return ListTileControl(key: key, control: control);
      case "ListView":
        return ListViewControl(key: key, control: control);
      case "Markdown":
        return MarkdownControl(key: key, control: control);
      case "MenuBar":
        return MenuBarControl(key: key, control: control);
      case "MenuItemButton":
        return MenuItemButtonControl(key: key, control: control);
      case "MergeSemantics":
        return MergeSemanticsControl(key: key, control: control);
      case "NavigationBar":
        return NavigationBarControl(key: key, control: control);
      case "NavigationBarDestination":
        return NavigationBarDestinationControl(key: key, control: control);
      case "NavigationDrawer":
        return NavigationDrawerControl(key: key, control: control);
      case "NavigationRail":
        return NavigationRailControl(key: key, control: control);
      case "Page":
        return PageControl(key: key, control: control);
      case "Pagelet":
        return PageletControl(key: key, control: control);
      case "Placeholder":
        return PlaceholderControl(key: key, control: control);
      case "PopupMenuButton":
        return PopupMenuButtonControl(key: key, control: control);
      case "ProgressBar":
        return ProgressBarControl(key: key, control: control);
      case "ProgressRing":
        return ProgressRingControl(key: key, control: control);
      case "Radio":
        return AdaptiveRadioControl(key: key, control: control);
      case "RadioGroup":
        return RadioGroupControl(key: key, control: control);
      case "RangeSlider":
        return RangeSliderControl(key: key, control: control);
      case "ReorderableDragHandle":
        return ReorderableDragHandleControl(key: key, control: control);
      case "ReorderableListView":
        return ReorderableListViewControl(key: key, control: control);
      case "ResponsiveRow":
        return ResponsiveRowControl(key: key, control: control);
      case "Row":
        return RowControl(key: key, control: control);
      case "SafeArea":
        return SafeAreaControl(key: key, control: control);
      case "Screenshot":
        return ScreenshotControl(key: key, control: control);
      case "SearchBar":
        return SearchBarControl(key: key, control: control);
      case "SegmentedButton":
        return SegmentedButtonControl(key: key, control: control);
      case "SelectionArea":
        return SelectionAreaControl(key: key, control: control);
      case "Semantics":
        return SemanticsControl(key: key, control: control);
      case "ShaderMask":
        return ShaderMaskControl(key: key, control: control);
      case "Shimmer":
        return ShimmerControl(key: key, control: control);
      case "Slider":
        return AdaptiveSliderControl(key: key, control: control);
      case "SnackBar":
        return SnackBarControl(key: key, control: control);
      case "Stack":
        return StackControl(key: key, control: control);
      case "SubmenuButton":
        return SubmenuButtonControl(key: key, control: control);
      case "Switch":
        return AdaptiveSwitchControl(key: key, control: control);
      case "Tab":
        return TabControl(key: key, control: control);
      case "TabBar":
        return TabBarControl(key: key, control: control);
      case "TabBarView":
        return TabBarViewControl(key: key, control: control);
      case "Tabs":
        return TabsControl(key: key, control: control);
      case "Text":
        return TextControl(key: key, control: control);
      case "TextField":
        return AdaptiveTextFieldControl(key: key, control: control);
      case "TimePicker":
        return TimePickerControl(key: key, control: control);
      case "TransparentPointer":
        return TransparentPointerControl(key: key, control: control);
      case "VerticalDivider":
        return VerticalDividerControl(key: key, control: control);
      case "View":
        return ViewControl(key: key, control: control);
      case "WindowDragArea":
        return WindowDragAreaControl(key: key, control: control);
      default:
        return null;
    }
  }

  @override
  FletService? createService(Control control) {
    switch (control.type) {
      case "BrowserContextMenu":
        return BrowserContextMenuService(control: control);
      case "Accelerometer":
        return AccelerometerService(control: control);
      case "Barometer":
        return BarometerService(control: control);
      case "Battery":
        return BatteryService(control: control);
      case "Clipboard":
        return ClipboardService(control: control);
      case "FilePicker":
        return FilePickerService(control: control);
      case "HapticFeedback":
        return HapticFeedbackService(control: control);
      case "Gyroscope":
        return GyroscopeService(control: control);
      case "ShakeDetector":
        return ShakeDetectorService(control: control);
      case "SharedPreferences":
        return SharedPreferencesService(control: control);
      case "SemanticsService":
        return SemanticsServiceControl(control: control);
      case "Magnetometer":
        return MagnetometerService(control: control);
      case "ScreenBrightness":
        return ScreenBrightnessService(control: control);
      case "StoragePaths":
        return StoragePaths(control: control);
      case "Window":
        return WindowService(control: control);
      case "Tester":
        return TesterService(control: control);
      case "UserAccelerometer":
        return UserAccelerometerService(control: control);
      case "UrlLauncher":
        return UrlLauncherService(control: control);
      case "Wakelock":
        return WakelockService(control: control);
      default:
        return null;
    }
  }

  @override
  IconData? createIconData(iconCode) {
    int setId = (iconCode >> 16) & 0xFF;
    int iconIndex = iconCode & 0xFFFF;

    if (setId == 1) {
      return materialIcons[iconIndex];
    } else if (setId == 2) {
      return cupertinoIcons[iconIndex];
    } else {
      return null;
    }
  }

  @override
  void ensureInitialized() {}
}
