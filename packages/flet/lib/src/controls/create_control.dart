import 'dart:math';

import 'package:collection/collection.dart';
import 'package:flet/src/utils/badge.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../control_factory.dart';
import '../flet_app_services.dart';
import '../flet_control_backend.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/page_media_view_model.dart';
import '../utils/animations.dart';
import '../utils/theme.dart';
import '../utils/tooltip.dart';
import '../utils/transforms.dart';
import 'alert_dialog.dart';
import 'animated_switcher.dart';
import 'auto_complete.dart';
import 'autofill_group.dart';
import 'banner.dart';
import 'barchart.dart';
import 'bottom_app_bar.dart';
import 'bottom_sheet.dart';
import 'canvas.dart';
import 'card.dart';
import 'checkbox.dart';
import 'chip.dart';
import 'circle_avatar.dart';
import 'column.dart';
import 'container.dart';
import 'cupertino_action_sheet.dart';
import 'cupertino_action_sheet_action.dart';
import 'cupertino_activity_indicator.dart';
import 'cupertino_alert_dialog.dart';
import 'cupertino_bottom_sheet.dart';
import 'cupertino_button.dart';
import 'cupertino_checkbox.dart';
import 'cupertino_context_menu.dart';
import 'cupertino_context_menu_action.dart';
import 'cupertino_date_picker.dart';
import 'cupertino_dialog_action.dart';
import 'cupertino_list_tile.dart';
import 'cupertino_navigation_bar.dart';
import 'cupertino_picker.dart';
import 'cupertino_radio.dart';
import 'cupertino_segmented_button.dart';
import 'cupertino_slider.dart';
import 'cupertino_sliding_segmented_button.dart';
import 'cupertino_switch.dart';
import 'cupertino_textfield.dart';
import 'cupertino_timer_picker.dart';
import 'datatable.dart';
import 'date_picker.dart';
import 'dismissible.dart';
import 'divider.dart';
import 'drag_target.dart';
import 'draggable.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'error.dart';
import 'expansion_panel.dart';
import 'expansion_tile.dart';
import 'file_picker.dart';
import 'flet_app_control.dart';
import 'floating_action_button.dart';
import 'gesture_detector.dart';
import 'grid_view.dart';
import 'haptic_feedback.dart';
import 'icon.dart';
import 'icon_button.dart';
import 'image.dart';
import 'interactive_viewer.dart';
import 'linechart.dart';
import 'list_tile.dart';
import 'list_view.dart';
import 'markdown.dart';
import 'menu_bar.dart';
import 'menu_item_button.dart';
import 'merge_semantics.dart';
import 'navigation_bar.dart';
import 'navigation_rail.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'pagelet.dart';
import 'piechart.dart';
import 'placeholder.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'radio_group.dart';
import 'range_slider.dart';
import 'reorderable_list_view.dart';
import 'responsive_row.dart';
import 'row.dart';
import 'safe_area.dart';
import 'search_anchor.dart';
import 'segmented_button.dart';
import 'selection_area.dart';
import 'semantics.dart';
import 'semantics_service.dart';
import 'shader_mask.dart';
import 'shake_detector.dart';
import 'slider.dart';
import 'snack_bar.dart';
import 'stack.dart';
import 'submenu_button.dart';
import 'switch.dart';
import 'tabs.dart';
import 'text.dart';
import 'text_button.dart';
import 'textfield.dart';
import 'time_picker.dart';
import 'transparent_pointer.dart';
import 'vertical_divider.dart';
import 'window_drag_area.dart';

Widget createControl(Control? parent, String id, bool parentDisabled,
    {Widget? nextChild, bool? parentAdaptive}) {
  //debugPrint("createControl(): $id");
  return StoreConnector<AppState, ControlViewModel?>(
    key: ValueKey<String>(id),
    distinct: true,
    converter: (store) {
      //debugPrint("ControlViewModel $id converter");
      return ControlViewModel.fromStore(store, id);
    },
    // onWillChange: (prev, next) {
    //   debugPrint("onWillChange() $id: $prev, $next");
    // },
    ignoreChange: (state) {
      //debugPrint("ignoreChange: $id");
      return state.controls[id] == null;
    },
    builder: (context, controlView) {
      if (controlView == null) {
        return const SizedBox.shrink();
      }

      Key? controlKey;
      var key = controlView.control.attrString("key", "")!;
      if (key != "") {
        if (key.startsWith("test:")) {
          controlKey = Key(key.substring(5));
        } else {
          var globalKey = controlKey = GlobalKey();
          FletAppServices.of(context).globalKeys[key] = globalKey;
        }
      }

      Widget? widget;

      for (var createControlFactory
          in FletAppServices.of(context).createControlFactories) {
        widget = createControlFactory(CreateControlArgs(
            controlKey,
            parent,
            controlView.control,
            controlView.children,
            nextChild,
            parentDisabled,
            parentAdaptive,
            FletAppServices.of(context).server));
        if (widget != null) {
          break;
        }
      }

      // try creating Flet built-in widget
      widget ??= createWidget(controlKey, controlView, parent, parentDisabled,
          parentAdaptive, nextChild, FletAppServices.of(context).server);

      // no theme defined? return widget!
      var themeMode = ThemeMode.values.firstWhereOrNull((t) =>
          t.name.toLowerCase() ==
          controlView.control.attrString("themeMode", "")!.toLowerCase());
      if (id == "page" ||
          (controlView.control.attrString("theme") == null &&
              themeMode == null)) {
        return widget;
      }

      // wrap into theme widget
      ThemeData? parentTheme = (themeMode == null) ? Theme.of(context) : null;

      buildTheme(Brightness? brightness) {
        return Theme(
            data: parseTheme(controlView.control, "theme", brightness,
                parentTheme: parentTheme),
            child: widget!);
      }

      if (themeMode == ThemeMode.system) {
        return StoreConnector<AppState, PageMediaViewModel>(
            distinct: true,
            converter: (store) => PageMediaViewModel.fromStore(store),
            builder: (context, media) {
              return buildTheme(media.displayBrightness);
            });
      } else {
        return buildTheme((themeMode == ThemeMode.light)
            ? Brightness.light
            : ((themeMode == ThemeMode.dark) ? Brightness.dark : null));
      }
    },
  );
}

Widget createWidget(
    Key? key,
    ControlViewModel controlView,
    Control? parent,
    bool parentDisabled,
    bool? parentAdaptive,
    Widget? nextChild,
    FletControlBackend backend) {
  switch (controlView.control.type.toLowerCase()) {
    case "page":
      return PageControl(
          control: controlView.control,
          children: controlView.children,
          dispatch: controlView.dispatch,
          backend: backend);
    case "text":
      return TextControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "icon":
      return IconControl(
          key: key, parent: parent, control: controlView.control);
    case "filepicker":
      return FilePickerControl(
          parent: parent,
          control: controlView.control,
          nextChild: nextChild,
          backend: backend);
    case "markdown":
      return MarkdownControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "fletapp":
      return FletAppControl(
          key: key, parent: parent, control: controlView.control);
    case "image":
      return ImageControl(
          key: key,
          parent: parent,
          children: controlView.children,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "divider":
      return DividerControl(
          key: key, parent: parent, control: controlView.control);
    case "selectionarea":
      return SelectionAreaControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "hapticfeedback":
      return HapticFeedbackControl(
          parent: parent,
          control: controlView.control,
          nextChild: nextChild,
          backend: backend);
    case "shakedetector":
      return ShakeDetectorControl(
          parent: parent,
          control: controlView.control,
          nextChild: nextChild,
          backend: backend);
    case "verticaldivider":
      return VerticalDividerControl(
          key: key, parent: parent, control: controlView.control);
    case "circleavatar":
      return CircleAvatarControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "chip":
      return ChipControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "pagelet":
      return PageletControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "progressring":
      return ProgressRingControl(
          key: key, parent: parent, control: controlView.control);
    case "progressbar":
      return ProgressBarControl(
          key: key, parent: parent, control: controlView.control);
    case "elevatedbutton":
    case "filledbutton":
    case "filledtonalbutton":
      return ElevatedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinobutton":
      return CupertinoButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "outlinedbutton":
      return OutlinedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "textbutton":
      return TextButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinodialogaction":
      return CupertinoDialogActionControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "iconbutton":
      return IconButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "floatingactionbutton":
      return FloatingActionButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "popupmenubutton":
      return PopupMenuButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "column":
      return ColumnControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "row":
      return RowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "responsiverow":
      return ResponsiveRowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "menubar":
      return MenuBarControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "submenubutton":
      return SubMenuButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "menuitembutton":
      return MenuItemButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "placeholder":
      return PlaceholderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinoslidingsegmentedbutton":
      return CupertinoSlidingSegmentedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentAdaptive: parentAdaptive,
          parentDisabled: parentDisabled,
          backend: backend);
    case "segmentedbutton":
      return SegmentedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "cupertinosegmentedbutton":
      return CupertinoSegmentedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentAdaptive: parentAdaptive,
          parentDisabled: parentDisabled,
          backend: backend);
    case "expansionpanellist":
      return ExpansionPanelListControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "stack":
      return StackControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "container":
      return ContainerControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "datepicker":
      return DatePickerControl(
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "cupertinodatepicker":
      return CupertinoDatePickerControl(
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "timepicker":
      return TimePickerControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "cupertinotimerpicker":
      return CupertinoTimerPickerControl(
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "cupertinopicker":
      return CupertinoPickerControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentAdaptive: parentAdaptive,
          parentDisabled: parentDisabled,
          backend: backend);
    case "cupertinobottomsheet":
      return CupertinoBottomSheetControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentAdaptive: parentAdaptive,
          parentDisabled: parentDisabled,
          nextChild: nextChild,
          backend: backend);
    case "draggable":
      return DraggableControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "dragtarget":
      return DragTargetControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "card":
      return CardControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "safearea":
      return SafeAreaControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "datatable":
      return DataTableControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "transparentpointer":
      return TransparentPointerControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "gesturedetector":
      return GestureDetectorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "semantics":
      return SemanticsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "mergesemantics":
      return MergeSemanticsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "semanticsservice":
      return SemanticsServiceControl(
          parent: parent, control: controlView.control, backend: backend);
    case "shadermask":
      return ShaderMaskControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "animatedswitcher":
      return AnimatedSwitcherControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "listtile":
      return ListTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "interactiveviewer":
      return InteractiveViewerControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinolisttile":
      return CupertinoListTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoactionsheet":
      return CupertinoActionSheetControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoactionsheetaction":
      return CupertinoActionSheetActionControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "expansiontile":
      return ExpansionTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "listview":
      return ListViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "reorderablelistview":
      return ReorderableListViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "gridview":
      return GridViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "autocomplete":
      return AutoCompleteControl(
          key: key,
          parent: parent,
          control: controlView.control,
          backend: backend);
    case "textfield":
      return TextFieldControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinotextfield":
      return CupertinoTextFieldControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "searchbar":
      return SearchAnchorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "checkbox":
      return CheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinocheckbox":
      return CupertinoCheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "switch":
      return SwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoswitch":
      return CupertinoSwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "slider":
      return SliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoslider":
      return CupertinoSliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "rangeslider":
      return RangeSliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "radiogroup":
      return RadioGroupControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "radio":
      return RadioControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "autofillgroup":
      return AutofillGroupControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinoradio":
      return CupertinoRadioControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "dropdown":
      return DropdownControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "snackbar":
      return SnackBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild,
          backend: backend);
    case "dismissible":
      return DismissibleControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoactivityindicator":
      return CupertinoActivityIndicatorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          backend: backend);
    case "alertdialog":
      return AlertDialogControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild,
          backend: backend);
    case "cupertinocontextmenu":
      return CupertinoContextMenuControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinocontextmenuaction":
      return CupertinoContextMenuActionControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinoalertdialog":
      return CupertinoAlertDialogControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild,
          backend: backend);
    case "bottomsheet":
      return BottomSheetControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild,
          backend: backend);
    case "banner":
      return BannerControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild,
          backend: backend);
    case "tabs":
      return TabsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "navigationrail":
      return NavigationRailControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "navigationbar":
      return NavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "cupertinonavigationbar":
      return CupertinoNavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    case "bottomappbar":
      return BottomAppBarControl(
        parent: parent,
        control: controlView.control,
        parentDisabled: parentDisabled,
        parentAdaptive: parentAdaptive,
        children: controlView.children,
      );
    case "windowdragarea":
      return WindowDragAreaControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "linechart":
      return LineChartControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "barchart":
      return BarChartControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "piechart":
      return PieChartControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          backend: backend);
    case "canvas":
      return CanvasControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          backend: backend);
    default:
      return ErrorControl("Unknown control: ${controlView.control.type}");
  }
}

Widget baseControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  return _expandable(
      _directionality(
          _tooltip(
            _opacity(context, widget, parent, control),
            Theme.of(context),
            parent,
            control,
          ),
          parent,
          control),
      parent,
      control);
}

Widget constrainedControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  return _expandable(
      _badge(
          _positionedControl(
              context,
              _aspectRatio(
                  _offsetControl(
                      context,
                      _scaledControl(
                          context,
                          _rotatedControl(
                              context,
                              _sizedControl(
                                  _directionality(
                                      _tooltip(
                                          _opacity(
                                              context, widget, parent, control),
                                          Theme.of(context),
                                          parent,
                                          control),
                                      parent,
                                      control),
                                  parent,
                                  control),
                              parent,
                              control),
                          parent,
                          control),
                      parent,
                      control),
                  parent,
                  control),
              parent,
              control),
          Theme.of(context),
          parent,
          control),
      parent,
      control);
}

Widget _opacity(
    BuildContext context, Widget widget, Control? parent, Control control) {
  var opacity = control.attrDouble("opacity");
  var animation = parseAnimation(control, "animateOpacity");
  if (animation != null) {
    return AnimatedOpacity(
      duration: animation.duration,
      curve: animation.curve,
      opacity: opacity ?? 1.0,
      onEnd: control.attrBool("onAnimationEnd", false)!
          ? () {
              FletAppServices.of(context)
                  .server
                  .triggerControlEvent(control.id, "animation_end", "opacity");
            }
          : null,
      child: widget,
    );
  } else if (opacity != null) {
    return Opacity(
      opacity: opacity,
      child: widget,
    );
  }
  return widget;
}

Widget _tooltip(
    Widget widget, ThemeData theme, Control? parent, Control control) {
  var tooltip = parseTooltip(control, "tooltip", widget, theme);
  return tooltip ?? widget;
}

Widget _badge(
    Widget widget, ThemeData theme, Control? parent, Control control) {
  var badge = parseBadge(control, "badge", widget, theme);
  return badge ?? widget;
}

Widget _aspectRatio(Widget widget, Control? parent, Control control) {
  var aspectRatio = control.attrDouble("aspectRatio");
  return aspectRatio != null
      ? AspectRatio(
          aspectRatio: aspectRatio,
          child: widget,
        )
      : widget;
}

Widget _rotatedControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  var rotationDetails = parseRotate(control, "rotate");
  var animation = parseAnimation(control, "animateRotation");
  if (animation != null) {
    return AnimatedRotation(
        turns: rotationDetails != null ? rotationDetails.angle / (2 * pi) : 0,
        alignment: rotationDetails?.alignment ?? Alignment.center,
        duration: animation.duration,
        curve: animation.curve,
        onEnd: control.attrBool("onAnimationEnd", false)!
            ? () {
                FletAppServices.of(context).server.triggerControlEvent(
                    control.id, "animation_end", "rotation");
              }
            : null,
        child: widget);
  } else if (rotationDetails != null) {
    return Transform.rotate(
        angle: rotationDetails.angle,
        alignment: rotationDetails.alignment,
        child: widget);
  }
  return widget;
}

Widget _scaledControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  var scaleDetails = parseScale(control, "scale");
  var animation = parseAnimation(control, "animateScale");
  if (animation != null) {
    return AnimatedScale(
        scale: scaleDetails?.scale! ?? 1.0,
        alignment: scaleDetails?.alignment ?? Alignment.center,
        duration: animation.duration,
        curve: animation.curve,
        onEnd: control.attrBool("onAnimationEnd", false)!
            ? () {
                FletAppServices.of(context)
                    .server
                    .triggerControlEvent(control.id, "animation_end", "scale");
              }
            : null,
        child: widget);
  } else if (scaleDetails != null) {
    return Transform.scale(
        scale: scaleDetails.scale,
        scaleX: scaleDetails.scaleX,
        scaleY: scaleDetails.scaleY,
        alignment: scaleDetails.alignment,
        child: widget);
  }
  return widget;
}

Widget _offsetControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  var offset = parseOffset(control, "offset");
  var animation = parseAnimation(control, "animateOffset");
  if (offset != null && animation != null) {
    return AnimatedSlide(
        offset: offset,
        duration: animation.duration,
        curve: animation.curve,
        onEnd: control.attrBool("onAnimationEnd", false)!
            ? () {
                FletAppServices.of(context)
                    .server
                    .triggerControlEvent(control.id, "animation_end", "offset");
              }
            : null,
        child: widget);
  } else if (offset != null) {
    return FractionalTranslation(translation: offset, child: widget);
  }
  return widget;
}

Widget _positionedControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  var left = control.attrDouble("left", null);
  var top = control.attrDouble("top", null);
  var right = control.attrDouble("right", null);
  var bottom = control.attrDouble("bottom", null);

  var animation = parseAnimation(control, "animatePosition");
  if (animation != null) {
    if (left == null && top == null && right == null && bottom == null) {
      left = 0;
      top = 0;
    }

    return AnimatedPositioned(
      duration: animation.duration,
      curve: animation.curve,
      left: left,
      top: top,
      right: right,
      bottom: bottom,
      onEnd: control.attrBool("onAnimationEnd", false)!
          ? () {
              FletAppServices.of(context)
                  .server
                  .triggerControlEvent(control.id, "animation_end", "position");
            }
          : null,
      child: widget,
    );
  } else if (left != null || top != null || right != null || bottom != null) {
    if (parent?.type != "stack" && parent?.type != "page") {
      return ErrorControl("Error displaying ${control.type}",
          description:
              "Control can be positioned absolutely with \"left\", \"top\", \"right\" and \"bottom\" properties inside Stack control only.");
    }
    return Positioned(
      left: left,
      top: top,
      right: right,
      bottom: bottom,
      child: widget,
    );
  }
  return widget;
}

Widget _sizedControl(Widget widget, Control? parent, Control control) {
  var width = control.attrDouble("width");
  var height = control.attrDouble("height");
  if ((width != null || height != null) &&
      !["container", "image"].contains(control.type)) {
    widget = ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: width, height: height),
      child: widget,
    );
  }
  var animation = parseAnimation(control, "animateSize");
  if (animation != null) {
    return AnimatedSize(
        duration: animation.duration, curve: animation.curve, child: widget);
  }
  return widget;
}

Widget _expandable(Widget widget, Control? parent, Control control) {
  if (parent != null && ["view", "column", "row"].contains(parent.type)) {
    int? expand = control.attrInt("expand");
    var expandLoose = control.attrBool("expandLoose");
    return expand != null
        ? (expandLoose == true)
            ? Flexible(flex: expand, child: widget)
            : Expanded(flex: expand, child: widget)
        : widget;
  }
  return widget;
}

Widget _directionality(Widget widget, Control? parent, Control control) {
  bool rtl = control.attrBool("rtl", false)!;
  return rtl
      ? Directionality(textDirection: TextDirection.rtl, child: widget)
      : widget;
}
