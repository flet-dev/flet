import 'dart:math';

import 'package:collection/collection.dart';
import 'package:flet/src/controls/search_anchor.dart';
import 'package:flet/src/controls/segmented_button.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/page_media_view_model.dart';
import '../utils/animations.dart';
import '../utils/theme.dart';
import '../utils/transforms.dart';
import 'alert_dialog.dart';
import 'animated_switcher.dart';
import 'bottom_app_bar.dart';
import 'audio.dart';
import 'badge.dart';
import 'cupertino_navigation_bar.dart';
import 'cupertino_slider.dart';
import 'expansion_panel.dart';
import 'selection_area.dart';
import 'banner.dart';
import 'barchart.dart';
import 'bottom_sheet.dart';
import 'canvas.dart';
import 'card.dart';
import 'checkbox.dart';
import 'chip.dart';
import 'circle_avatar.dart';
import 'clipboard.dart';
import 'column.dart';
import 'container.dart';
import 'datatable.dart';
import 'date_picker.dart';
import 'dismissible.dart';
import 'divider.dart';
import 'drag_target.dart';
import 'draggable.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'error.dart';
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
import 'navigation_bar.dart';
import 'navigation_rail.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'piechart.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'cupertino_radio.dart';
import 'radio_group.dart';
import 'range_slider.dart';
import 'responsive_row.dart';
import 'row.dart';
import 'safe_area.dart';
import 'semantics.dart';
import 'shader_mask.dart';
import 'shake_detector.dart';
import 'slider.dart';
import 'snack_bar.dart';
import 'stack.dart';
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
import 'cupertino_checkbox.dart';
import 'cupertino_switch.dart';

Widget createControl(Control? parent, String id, bool parentDisabled,
    {Widget? nextChild}) {
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

      // create control widget
      var widget = createWidget(
          controlKey, controlView, parent, parentDisabled, nextChild);

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
            child: widget);
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

Widget createWidget(Key? key, ControlViewModel controlView, Control? parent,
    bool parentDisabled, Widget? nextChild) {
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
          parent: parent,
          control: controlView.control,
          dispatch: controlView.dispatch,
          nextChild: nextChild);
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
      );
    case "selectionarea":
      return SelectionAreaControl(
        key: key,
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
      );
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
          dispatch: controlView.dispatch);
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
          parentDisabled: parentDisabled);
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
    case "iconbutton":
      return IconButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "floatingactionbutton":
      return FloatingActionButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
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
        dispatch: controlView.dispatch,
      );
    case "row":
      return RowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "responsiverow":
      return ResponsiveRowControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "segmentedbutton":
      return SegmentedButtonControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "expansionpanellist":
      return ExpansionPanelListControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "stack":
      return StackControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "container":
      return ContainerControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "datepicker":
      return DatePickerControl(
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "timepicker":
      return TimePickerControl(
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "draggable":
      return DraggableControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "dragtarget":
      return DragTargetControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "card":
      return CardControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "safearea":
      return SafeAreaControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
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
          parentDisabled: parentDisabled);
    case "transparentpointer":
      return TransparentPointerControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "gesturedetector":
      return GestureDetectorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "semantics":
      return SemanticsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "shadermask":
      return ShaderMaskControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "animatedswitcher":
      return AnimatedSwitcherControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "listtile":
      return ListTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "expansiontile":
      return ExpansionTileControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "listview":
      return ListViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "gridview":
      return GridViewControl(
        key: key,
        parent: parent,
        control: controlView.control,
        children: controlView.children,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "textfield":
      return TextFieldControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "searchbar":
      return SearchAnchorControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "checkbox":
      return CheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "cupertinocheckbox":
      return CupertinoCheckboxControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "switch":
      return SwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "cupertinoswitch":
      return CupertinoSwitchControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "slider":
      return SliderControl(
        key: key,
        parent: parent,
        control: controlView.control,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "cupertinoslider":
      return CupertinoSliderControl(
        key: key,
        parent: parent,
        control: controlView.control,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "rangeslider":
      return RangeSliderControl(
        key: key,
        parent: parent,
        control: controlView.control,
        parentDisabled: parentDisabled,
        dispatch: controlView.dispatch,
      );
    case "radiogroup":
      return RadioGroupControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "radio":
      return RadioControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "cupertinoradio":
      return CupertinoRadioControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "dropdown":
      return DropdownControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "snackbar":
      return SnackBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          nextChild: nextChild);
    case "dismissible":
      return DismissibleControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
    case "alertdialog":
      return AlertDialogControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          nextChild: nextChild);
    case "bottomsheet":
      return BottomSheetControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch,
          nextChild: nextChild);
    case "banner":
      return BannerControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          nextChild: nextChild);
    case "tabs":
      return TabsControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "navigationrail":
      return NavigationRailControl(
          key: key,
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "navigationbar":
      return NavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "cupertinonavigationbar":
      return CupertinoNavigationBarControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled,
          dispatch: controlView.dispatch);
    case "bottomappbar":
      return BottomAppBarControl(
        parent: parent,
        control: controlView.control,
        parentDisabled: parentDisabled,
        children: controlView.children,
      );
    case "windowdragarea":
      return WindowDragAreaControl(
          parent: parent,
          control: controlView.control,
          children: controlView.children,
          parentDisabled: parentDisabled);
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
          parentDisabled: parentDisabled);
    case "webview":
      return WebViewControl(
          key: key,
          parent: parent,
          control: controlView.control,
          parentDisabled: parentDisabled);
    default:
      throw Exception("Unknown control type: ${controlView.control.type}");
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
          parent.type == "row")) {
    //debugPrint("Expandable ${control.id}");
    int? expand = control.attrInt("expand");
    return expand != null ? Expanded(flex: expand, child: widget) : widget;
  }
  return widget;
}
