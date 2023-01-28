import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_view_model.dart';
import '../utils/animations.dart';
import '../utils/transforms.dart';
import 'alert_dialog.dart';
import 'animated_switcher.dart';
import 'audio.dart';
import 'banner.dart';
import 'bottom_sheet.dart';
import 'card.dart';
import 'checkbox.dart';
import 'circle_avatar.dart';
import 'clipboard.dart';
import 'column.dart';
import 'container.dart';
import 'datatable.dart';
import 'date_picker.dart';
import 'divider.dart';
import 'drag_target.dart';
import 'draggable.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'error.dart';
import 'file_picker.dart';
import 'flet_app_control.dart';
import 'floating_action_button.dart';
import 'gesture_detector.dart';
import 'grid_view.dart';
import 'haptic_feedback.dart';
import 'icon.dart';
import 'icon_button.dart';
import 'image.dart';
import 'list_tile.dart';
import 'list_view.dart';
import 'markdown.dart';
import 'navigation_bar.dart';
import 'navigation_rail.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'radio_group.dart';
import 'responsive_row.dart';
import 'row.dart';
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
import 'tooltip.dart';
import 'transparent_pointer.dart';
import 'vertical_divider.dart';
import 'window_drag_area.dart';

Widget createControl(Control? parent, String id, bool parentDisabled) {
  //debugPrint("createControl(): $id");
  return StoreConnector<AppState, ControlViewModel>(
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
      //debugPrint("createControl builder(): $id");
      switch (controlView.control.type) {
        case "page":
          return PageControl(
              control: controlView.control,
              children: controlView.children,
              dispatch: controlView.dispatch);
        case "text":
          return TextControl(parent: parent, control: controlView.control);
        case "icon":
          return IconControl(parent: parent, control: controlView.control);
        case "filepicker":
          return FilePickerControl(
              parent: parent, control: controlView.control);
        case "markdown":
          return MarkdownControl(parent: parent, control: controlView.control);
        case "fletapp":
          return FletAppControl(parent: parent, control: controlView.control);
        case "image":
          return ImageControl(parent: parent, control: controlView.control);
        case "audio":
          return AudioControl(parent: parent, control: controlView.control);
        case "divider":
          return DividerControl(parent: parent, control: controlView.control);
        case "clipboard":
          return ClipboardControl(parent: parent, control: controlView.control);
        case "hapticfeedback":
          return HapticFeedbackControl(
              parent: parent, control: controlView.control);
        case "shakedetector":
          return ShakeDetectorControl(
              parent: parent, control: controlView.control);
        case "verticaldivider":
          return VerticalDividerControl(
              parent: parent, control: controlView.control);
        case "circleavatar":
          return CircleAvatarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "progressring":
          return ProgressRingControl(
              parent: parent, control: controlView.control);
        case "progressbar":
          return ProgressBarControl(
              parent: parent, control: controlView.control);
        case "elevatedbutton":
          return ElevatedButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "outlinedbutton":
          return OutlinedButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "textbutton":
          return TextButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "iconbutton":
          return IconButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "floatingactionbutton":
          return FloatingActionButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "popupmenubutton":
          return PopupMenuButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "column":
          return ColumnControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "row":
          return RowControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "responsiverow":
          return ResponsiveRowControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "stack":
          return StackControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "container":
          return ContainerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "draggable":
          return DraggableControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "dragtarget":
          return DragTargetControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "card":
          return CardControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "datatable":
          return DataTableControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "date_picker":
          return DatePickerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "tooltip":
          return TooltipControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "transparentpointer":
          return TransparentPointerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "gesturedetector":
          return GestureDetectorControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "semantics":
          return SemanticsControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "shadermask":
          return ShaderMaskControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "animatedswitcher":
          return AnimatedSwitcherControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "listtile":
          return ListTileControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "listview":
          return ListViewControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "gridview":
          return GridViewControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "textfield":
          return TextFieldControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "checkbox":
          return CheckboxControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case "switch":
          return SwitchControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case "slider":
          return SliderControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case "radiogroup":
          return RadioGroupControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "radio":
          return RadioControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case "dropdown":
          return DropdownControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case "snackbar":
          return SnackBarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "alertdialog":
          return AlertDialogControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "bottomsheet":
          return BottomSheetControl(
            parent: parent,
            control: controlView.control,
            children: controlView.children,
            parentDisabled: parentDisabled,
            dispatch: controlView.dispatch,
          );
        case "banner":
          return BannerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "tabs":
          return TabsControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "navigationrail":
          return NavigationRailControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "navigationbar":
          return NavigationBarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "windowdragarea":
          return WindowDragAreaControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        default:
          throw Exception("Unknown control type: ${controlView.control.type}");
      }
    },
  );
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
