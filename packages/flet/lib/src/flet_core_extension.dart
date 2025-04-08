import 'package:flutter/widgets.dart';

import 'controls/adaptive_alert_dialog.dart';
import 'controls/adaptive_elevated_button.dart';
import 'controls/adaptive_slider.dart';
import 'controls/adaptive_switch.dart';
import 'controls/animated_switcher.dart';
import 'controls/banner.dart';
import 'controls/card.dart';
import 'controls/center.dart';
import 'controls/chip.dart';
import 'controls/circle_avatar.dart';
import 'controls/column.dart';
import 'controls/container.dart';
import 'controls/cupertino_action_sheet.dart';
import 'controls/cupertino_action_sheet_action.dart';
import 'controls/cupertino_activity_indicator.dart';
import 'controls/cupertino_alert_dialog.dart';
import 'controls/cupertino_button.dart';
import 'controls/cupertino_checkbox.dart';
import 'controls/cupertino_context_menu.dart';
import 'controls/cupertino_context_menu_action.dart';
import 'controls/cupertino_dialog_action.dart';
import 'controls/cupertino_list_tile.dart';
import 'controls/cupertino_slider.dart';
import 'controls/cupertino_switch.dart';
import 'controls/datatable.dart';
import 'controls/divider.dart';
import 'controls/dropdown.dart';
import 'controls/elevated_button.dart';
import 'controls/expansion_panel.dart';
import 'controls/expansion_tile.dart';
import 'controls/flet_app_control.dart';
import 'controls/floating_action_button.dart';
import 'controls/icon.dart';
import 'controls/icon_button.dart';
import 'controls/image.dart';
import 'controls/line_chart.dart';
import 'controls/list_tile.dart';
import 'controls/list_view.dart';
import 'controls/menu_bar.dart';
import 'controls/menu_item_button.dart';
import 'controls/merge_semantics.dart';
import 'controls/navigation_drawer.dart';
import 'controls/navigation_rail.dart';
import 'controls/outlined_button.dart';
import 'controls/page.dart';
import 'controls/placeholder.dart';
import 'controls/progress_bar.dart';
import 'controls/progress_ring.dart';
import 'controls/radio_group.dart';
import 'controls/range_slider.dart';
import 'controls/reorderable_draggable.dart';
import 'controls/reorderable_list_view.dart';
import 'controls/responsive_row.dart';
import 'controls/row.dart';
import 'controls/safe_area.dart';
import 'controls/search_bar.dart';
import 'controls/segmented_button.dart';
import 'controls/selection_area.dart';
import 'controls/semantics.dart';
import 'controls/shader_mask.dart';
import 'controls/snack_bar.dart';
import 'controls/stack.dart';
import 'controls/submenu_button.dart';
import 'controls/text.dart';
import 'controls/text_button.dart';
import 'controls/transparent_pointer.dart';
import 'controls/vertical_divider.dart';
import 'controls/view.dart';
import 'controls/window.dart';
import 'flet_backend.dart';
import 'flet_extension.dart';
import 'flet_service.dart';
import 'models/control.dart';
import 'services/browser_context_menu.dart';
import 'services/clipboard.dart';
import 'services/haptic_feedback.dart';
import 'services/semantics_service.dart';
import 'services/shake_detector.dart';
import 'services/shared_preferences.dart';
import 'services/url_launcher.dart';

class FletCoreExtension extends FletExtension {
  @override
  Widget? createWidget(Key? key, Control control) {
    switch (control.type) {
      case "AlertDialog":
        return AdaptiveAlertDialogControl(key: key, control: control);
      case "AnimatedSwitcher":
        return AnimatedSwitcherControl(key: key, control: control);
      case "Banner":
        return BannerControl(key: key, control: control);
      case "OutlinedButton":
        return OutlinedButtonControl(key: key, control: control);
      case "SearchBar":
        return SearchBarControl(key: key, control: control);
      case "Card":
        return CardControl(key: key, control: control);
      case "Center":
        return CenterControl(key: key, control: control);
      case "SegmentedButton":
        return SegmentedButtonControl(key: key, control: control);
      case "Semantics":
        return SemanticsControl(key: key, control: control);
      case "MergeSemantics":
        return MergeSemanticsControl(key: key, control: control);
      case "Column":
        return ColumnControl(key: key, control: control);
      case "CupertinoActionSheet":
        return CupertinoActionSheetControl(key: key, control: control);
      case "CupertinoActionSheetAction":
        return CupertinoActionSheetActionControl(key: key, control: control);
      case "TextButton":
        return TextButtonControl(key: key, control: control);
      case "Container":
        return ContainerControl(key: key, control: control);
      case "Chip":
        return ChipControl(key: key, control: control);
      case "CircleAvatar":
        return CircleAvatarControl(key: key, control: control);
      case "IconButton":
        return IconButtonControl(key: key, control: control);
      case "CupertinoActivityIndicator":
        return CupertinoActivityIndicatorControl(key: key, control: control);
      case "CupertinoAlertDialog":
        return CupertinoAlertDialogControl(key: key, control: control);
      case "CupertinoButton":
        return CupertinoButtonControl(key: key, control: control);
      case "CupertinoContextMenu":
        return CupertinoContextMenuControl(key: key, control: control);
      case "CupertinoContextMenuAction":
        return CupertinoContextMenuActionControl(key: key, control: control);
      case "CupertinoDialogAction":
        return CupertinoDialogActionControl(key: key, control: control);
      case "CupertinoSlider":
        return CupertinoSliderControl(key: key, control: control);
      case "CupertinoSwitch":
        return CupertinoSwitchControl(key: key, control: control);
      case "CupertinoListTile":
        return CupertinoListTileControl(key: key, control: control);
      case "DataTable":
        return DataTableControl(key: key, control: control);
      case "Divider":
        return DividerControl(key: key, control: control);
      case "Dropdown":
        return DropdownControl(key: key, control: control);
      case "ElevatedButton":
        return AdaptiveElevatedButtonControl(key: key, control: control);
      case "ExpansionPanelList":
        return ExpansionPanelListControl(key: key, control: control);
      case "ExpansionTile":
        return ExpansionTileControl(key: key, control: control);
      case "FilledButton":
        return ElevatedButtonControl(key: key, control: control);
      case "FilledTonalButton":
        return ElevatedButtonControl(key: key, control: control);
      case "FletApp":
        return FletAppControl(key: key, control: control);
      case "SubmenuButton":
        return SubmenuButtonControl(key: key, control: control);
      case "FloatingActionButton":
        return FloatingActionButtonControl(key: key, control: control);
      case "Icon":
        return IconControl(key: key, control: control);
      case "Image":
        return ImageControl(key: key, control: control);
      case "LineChart":
        return LineChartControl(key: key, control: control);
      case "ListTile":
        return ListTileControl(key: key, control: control);
      case "ListView":
        return ListViewControl(key: key, control: control);
      case "TransparentPointer":
        return TransparentPointerControl(key: key, control: control);
      case "ResponsiveRow":
        return ResponsiveRowControl(key: key, control: control);
      case "NavigationDrawer":
        return NavigationDrawerControl(key: key, control: control);
      case "NavigationRail":
        return NavigationRailControl(key: key, control: control);
      case "ReorderableListView":
        return ReorderableListViewControl(key: key, control: control);
      case "Page":
        return PageControl(key: key, control: control);
      case "ProgressBar":
        return ProgressBarControl(key: key, control: control);
      case "ProgressRing":
        return ProgressRingControl(key: key, control: control);
      case "ShaderMask":
        return ShaderMaskControl(key: key, control: control);
      case "RangeSlider":
        return RangeSliderControl(key: key, control: control);
      case "ReorderableDraggable":
        return ReorderableDraggableControl(key: key, control: control);
      case "Row":
        return RowControl(key: key, control: control);
      case "Slider":
        return AdaptiveSliderControl(key: key, control: control);
      case "SnackBar":
        return SnackBarControl(key: key, control: control);
      case "Stack":
        return StackControl(key: key, control: control);
      case "Switch":
        return AdaptiveSwitchControl(key: key, control: control);
      case "Text":
        return TextControl(key: key, control: control);
      case "Placeholder":
        return PlaceholderControl(key: key, control: control);
      case "MenuBar":
        return MenuBarControl(key: key, control: control);
      case "VerticalDivider":
        return VerticalDividerControl(key: key, control: control);
      case "MenuItemButton":
        return MenuItemButtonControl(key: key, control: control);
      case "View":
        return ViewControl(key: key, control: control);
      case "SafeArea":
        return SafeAreaControl(key: key, control: control);
      case "SelectionArea":
        return SelectionAreaControl(key: key, control: control);
      case "RadioGroup":
        return RadioGroupControl(key: key, control: control);
      case "CupertinoCheckbox":
        return CupertinoCheckboxControl(key: key, control: control);
      case "Window":
        return WindowControl(key: key, control: control);
      default:
        return null;
    }
  }

  @override
  FletService? createService(Control control, FletBackend backend) {
    switch (control.type) {
      case "BrowserContextMenu":
        return BrowserContextMenuService(control: control, backend: backend);
      case "Clipboard":
        return ClipboardService(control: control, backend: backend);
      case "HapticFeedback":
        return HapticFeedbackService(control: control, backend: backend);
      case "ShakeDetector":
        return ShakeDetectorService(control: control, backend: backend);
      case "SharedPreferences":
        return SharedPreferencesService(control: control, backend: backend);
      case "UrlLauncher":
        return UrlLauncherService(control: control, backend: backend);
      case "SemanticsService":
        return SemanticsServiceControl(control: control, backend: backend);
      default:
        return null;
    }
  }

  @override
  void ensureInitialized() {}
}
