import 'dart:math';

import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../control_factory.dart';
import '../flet_app_services.dart';
import '../flet_server.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/page_media_view_model.dart';
import '../utils/animations.dart';
import '../utils/theme.dart';
import '../utils/transforms.dart';
import 'alert_dialog.dart';
import 'animated_switcher.dart';
import 'audio.dart';
import 'badge.dart';
import 'banner.dart';
import 'barchart.dart';
import 'bottom_app_bar.dart';
import 'bottom_sheet.dart';
import 'canvas.dart';
import 'card.dart';
import 'checkbox.dart';
import 'chip.dart';
import 'circle_avatar.dart';
import 'clipboard.dart';
import 'column.dart';
import 'container.dart';
import 'cupertino_alert_dialog.dart';
import 'cupertino_button.dart';
import 'cupertino_checkbox.dart';
import 'cupertino_dialog_action.dart';
import 'cupertino_list_tile.dart';
import 'cupertino_navigation_bar.dart';
import 'cupertino_radio.dart';
import 'cupertino_slider.dart';
import 'cupertino_switch.dart';
import 'cupertino_textfield.dart';
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
import 'linechart.dart';
import 'list_tile.dart';
import 'list_view.dart';
import 'markdown.dart';
import 'menu_bar.dart';
import 'menu_item_button.dart';
import 'navigation_bar.dart';
import 'navigation_rail.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'pagelet.dart';
import 'piechart.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'radio_group.dart';
import 'range_slider.dart';
import 'responsive_row.dart';
import 'row.dart';
import 'safe_area.dart';
import 'search_anchor.dart';
import 'segmented_button.dart';
import 'selection_area.dart';
import 'semantics.dart';
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
import 'tooltip.dart';
import 'transparent_pointer.dart';
import 'vertical_divider.dart';
import 'webview.dart';
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
            parentDisabled,
            parentAdaptive));
        if (widget != null) {
          break;
        }
      }

      // try creating Flet built-in widget
      widget ??= createWidget(controlKey, controlView, parent, parentDisabled,
          parentAdaptive, nextChild, FletAppServices.of(context).server);

      // no theme defined? return widget!
      if (id == "page" || controlView.control.attrString("theme") == null) {
        return widget;
      }

      // wrap into theme widget
      var themeMode = ThemeMode.values.firstWhereOrNull((t) =>
          t.name.toLowerCase() ==
          controlView.control.attrString("themeMode", "")!.toLowerCase());

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
    FletServer server) {
  switch (controlView.control.type) {
    case "page":
      return PageControl(
          control: controlView.control,
          children: controlView.children,
          dispatch: controlView.dispatch);
    case "text":
      return TextControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "icon":
      return IconControl(
          key: key, parent: parent, control: controlView.control);
    case "filepicker":
      return FilePickerControl(
        parent: parent,
        control: controlView.control,
        nextChild: nextChild,
      );
    case "markdown":
      return MarkdownControl(
          key: key, parent: parent, control: controlView.control);
    case "fletapp":
      return FletAppControl(
          key: key, parent: parent, control: controlView.control);
    case "image":
      return ImageControl(
          key: key,
          parent: parent,
          children: controlView.children,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "audio":
      return AudioControl(
          parent: parent, control: controlView.control, nextChild: nextChild);
    case "divider":
      return DividerControl(
          key: key, parent: parent, control: controlView.control);
    case "badge":
      return BadgeControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "selectionarea":
      return SelectionAreaControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "clipboard":
      return ClipboardControl(
          parent: parent, control: controlView.control, nextChild: nextChild);
    case "hapticfeedback":
      return HapticFeedbackControl(
          parent: parent, control: controlView.control, nextChild: nextChild);
    case "shakedetector":
      return ShakeDetectorControl(
          parent: parent, control: controlView.control, nextChild: nextChild);
    case "verticaldivider":
      return VerticalDividerControl(
          key: key, parent: parent, control: controlView.control);
    case "circleavatar":
      return CircleAvatarControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "chip":
      return ChipControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "pagelet":
      return PageletControl(
        key: key,
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
        parentAdaptive: parentAdaptive,
      );
    case "progressring":
      return ProgressRingControl(
          key: key, parent: parent, control: controlView.control);
    case "progressbar":
      return ProgressBarControl(
          key: key, parent: parent, control: controlView.control);
    case "elevatedbutton":
      return ElevatedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinobutton":
      return CupertinoButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "outlinedbutton":
      return OutlinedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "textbutton":
      return TextButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "cupertinodialogaction":
      return CupertinoDialogActionControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "iconbutton":
      return IconButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "floatingactionbutton":
      return FloatingActionButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "popupmenubutton":
      return PopupMenuButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "column":
      return ColumnControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "row":
      return RowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "responsiverow":
      return ResponsiveRowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
          parentDisabled: parentDisabled);
    case "menuitembutton":
      return MenuItemButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "segmentedbutton":
      return SegmentedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "expansionpanellist":
      return ExpansionPanelListControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
          parentAdaptive: parentAdaptive);
    case "datepicker":
      return DatePickerControl(
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
      );
    case "timepicker":
      return TimePickerControl(
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
      );
    case "draggable":
      return DraggableControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "dragtarget":
      return DragTargetControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
          parentDisabled: parentDisabled);
    case "tooltip":
      return TooltipControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
      );
    case "semantics":
      return SemanticsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
          parentAdaptive: parentAdaptive);
    case "cupertinolisttile":
      return CupertinoListTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "expansiontile":
      return ExpansionTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "listview":
      return ListViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "gridview":
      return GridViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "textfield":
      return TextFieldControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinotextfield":
      return CupertinoTextFieldControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "searchbar":
      return SearchAnchorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "checkbox":
      return CheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinocheckbox":
      return CupertinoCheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "switch":
      return SwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinoswitch":
      return CupertinoSwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "slider":
      return SliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinoslider":
      return CupertinoSliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "rangeslider":
      return RangeSliderControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
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
          parentAdaptive: parentAdaptive);
    case "cupertinoradio":
      return CupertinoRadioControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    case "dropdown":
      return DropdownControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "snackbar":
      return SnackBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild);
    case "dismissible":
      return DismissibleControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "alertdialog":
      return AlertDialogControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild);
    case "cupertinoalertdialog":
      return CupertinoAlertDialogControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild);
    case "bottomsheet":
      return BottomSheetControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild);
    case "banner":
      return BannerControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive,
          nextChild: nextChild);
    case "tabs":
      return TabsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "navigationrail":
      return NavigationRailControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "navigationbar":
      return NavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "cupertinonavigationbar":
      return CupertinoNavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
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
          parentDisabled: parentDisabled);
    case "barchart":
      return BarChartControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "piechart":
      return PieChartControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "canvas":
      return CanvasControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          parentAdaptive: parentAdaptive);
    case "webview":
      return WebViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    default:
      return ErrorControl("Unknown control: ${controlView.control.type}");
  }
}

Widget baseControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  return _expandable(
      _tooltip(_opacity(context, widget, parent, control), parent, control),
      parent,
      control);
}

Widget constrainedControl(
    BuildContext context, Widget widget, Control? parent, Control control) {
  return _expandable(
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
                              _tooltip(
                                  _opacity(context, widget, parent, control),
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
              FletAppServices.of(context).server.sendPageEvent(
                  eventTarget: control.id,
                  eventName: "animation_end",
                  eventData: "opacity");
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

Widget _tooltip(Widget widget, Control? parent, Control control) {
  var tooltip = control.attrString("tooltip");
  return tooltip != null &&
          !["iconbutton", "floatingactionbutton", "popupmenubutton"]
              .contains(control.type)
      ? Tooltip(
          message: tooltip,
          padding: const EdgeInsets.all(4.0),
          waitDuration: const Duration(milliseconds: 800),
          child: widget,
        )
      : widget;
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
                FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "animation_end",
                    eventData: "rotation");
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
                FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "animation_end",
                    eventData: "scale");
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
  var offsetDetails = parseOffset(control, "offset");
  var animation = parseAnimation(control, "animateOffset");
  if (offsetDetails != null && animation != null) {
    return AnimatedSlide(
        offset: Offset(offsetDetails.x, offsetDetails.y),
        duration: animation.duration,
        curve: animation.curve,
        onEnd: control.attrBool("onAnimationEnd", false)!
            ? () {
                FletAppServices.of(context).server.sendPageEvent(
                    eventTarget: control.id,
                    eventName: "animation_end",
                    eventData: "offset");
              }
            : null,
        child: widget);
  } else if (offsetDetails != null) {
    return FractionalTranslation(
        translation: Offset(offsetDetails.x, offsetDetails.y), child: widget);
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
              FletAppServices.of(context).server.sendPageEvent(
                  eventTarget: control.id,
                  eventName: "animation_end",
                  eventData: "position");
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
  var width = control.attrDouble("width", null);
  var height = control.attrDouble("height", null);
  if (width != null || height != null) {
    if (control.type != "container" && control.type != "image") {
      widget = ConstrainedBox(
        constraints: BoxConstraints.tightFor(width: width, height: height),
        child: widget,
      );
    }
  }
  var animation = parseAnimation(control, "animateSize");
  if (animation != null) {
    return AnimatedSize(
        duration: animation.duration, curve: animation.curve, child: widget);
  }
  return widget;
}

Widget _expandable(Widget widget, Control? parent, Control control) {
  if (parent != null &&
      (parent.type == "view" ||
          parent.type == "column" ||
          //parent.type == "container" ||
          parent.type == "row")) {
    //debugPrint("Expandable ${control.id}");
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
