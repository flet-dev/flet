import '../utils/animations.dart';
import '../utils/transforms.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_type.dart';
import '../models/control_view_model.dart';
import 'alert_dialog.dart';
import 'animated_switcher.dart';
import 'banner.dart';
import 'card.dart';
import 'checkbox.dart';
import 'circle_avatar.dart';
import 'clipboard.dart';
import 'column.dart';
import 'container.dart';
import 'divider.dart';
import 'drag_target.dart';
import 'draggable.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'floating_action_button.dart';
import 'grid_view.dart';
import 'icon.dart';
import 'icon_button.dart';
import 'image.dart';
import 'launch_url.dart';
import 'list_tile.dart';
import 'list_view.dart';
import 'markdown.dart';
import 'navigation_rail.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'radio_group.dart';
import 'row.dart';
import 'semantics.dart';
import 'shader_mask.dart';
import 'slider.dart';
import 'snack_bar.dart';
import 'stack.dart';
import 'switch.dart';
import 'tabs.dart';
import 'text.dart';
import 'text_button.dart';
import 'textfield.dart';
import 'vertical_divider.dart';
import 'dart:math';

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
        case ControlType.page:
          return PageControl(
              control: controlView.control,
              children: controlView.children,
              dispatch: controlView.dispatch);
        case ControlType.text:
          return TextControl(parent: parent, control: controlView.control);
        case ControlType.icon:
          return IconControl(parent: parent, control: controlView.control);
        case ControlType.markdown:
          return MarkdownControl(parent: parent, control: controlView.control);
        case ControlType.clipboard:
          return ClipboardControl(parent: parent, control: controlView.control);
        case ControlType.launchUrl:
          return LaunchUrlControl(parent: parent, control: controlView.control);
        case ControlType.image:
          return ImageControl(parent: parent, control: controlView.control);
        case ControlType.divider:
          return DividerControl(parent: parent, control: controlView.control);
        case ControlType.verticalDivider:
          return VerticalDividerControl(
              parent: parent, control: controlView.control);
        case ControlType.circleAvatar:
          return CircleAvatarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.progressRing:
          return ProgressRingControl(
              parent: parent, control: controlView.control);
        case ControlType.progressBar:
          return ProgressBarControl(
              parent: parent, control: controlView.control);
        case ControlType.elevatedButton:
          return ElevatedButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.outlinedButton:
          return OutlinedButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.textButton:
          return TextButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.iconButton:
          return IconButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.floatingActionButton:
          return FloatingActionButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.popupMenuButton:
          return PopupMenuButtonControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.column:
          return ColumnControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.row:
          return RowControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.stack:
          return StackControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.container:
          return ContainerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.draggable:
          return DraggableControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.dragTarget:
          return DragTargetControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.card:
          return CardControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.semantics:
          return SemanticsControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.shaderMask:
          return ShaderMaskControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.animatedSwitcher:
          return AnimatedSwitcherControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.listTile:
          return ListTileControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.listView:
          return ListViewControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.gridView:
          return GridViewControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.textField:
          return TextFieldControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.checkbox:
          return CheckboxControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case ControlType.Switch:
          return SwitchControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case ControlType.slider:
          return SliderControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case ControlType.radioGroup:
          return RadioGroupControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.radio:
          return RadioControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case ControlType.dropdown:
          return DropdownControl(
              parent: parent,
              control: controlView.control,
              parentDisabled: parentDisabled);
        case ControlType.snackBar:
          return SnackBarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.alertDialog:
          return AlertDialogControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.banner:
          return BannerControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.tabs:
          return TabsControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.navigationRail:
          return NavigationRailControl(
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

Widget baseControl(Widget widget, Control? parent, Control control) {
  return _expandable(
      _tooltip(_opacity(widget, parent, control), parent, control),
      parent,
      control);
}

Widget constrainedControl(Widget widget, Control? parent, Control control) {
  return _expandable(
      _positionedControl(
          _offsetControl(
              _scaledControl(
                  _rotatedControl(
                      _sizedControl(
                          _tooltip(_opacity(widget, parent, control), parent,
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

Widget _opacity(Widget widget, Control? parent, Control control) {
  var opacity = control.attrDouble("opacity");
  var animation = parseAnimation(control, "animateOpacity");
  if (animation != null) {
    return AnimatedOpacity(
      duration: animation.duration,
      curve: animation.curve,
      opacity: opacity ?? 1.0,
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
          ![
            ControlType.iconButton,
            ControlType.floatingActionButton,
            ControlType.popupMenuButton
          ].contains(control.type)
      ? Tooltip(
          message: tooltip,
          padding: const EdgeInsets.all(4.0),
          child: widget,
          waitDuration: const Duration(milliseconds: 800),
        )
      : widget;
}

Widget _rotatedControl(Widget widget, Control? parent, Control control) {
  var rotationDetails = parseRotate(control, "rotate");
  var animation = parseAnimation(control, "animateRotation");
  if (animation != null) {
    return AnimatedRotation(
        turns: rotationDetails != null ? rotationDetails.angle / (2 * pi) : 0,
        alignment: rotationDetails?.alignment ?? Alignment.center,
        duration: animation.duration,
        curve: animation.curve,
        child: widget);
  } else if (rotationDetails != null) {
    return Transform.rotate(
        angle: rotationDetails.angle,
        alignment: rotationDetails.alignment,
        child: widget);
  }
  return widget;
}

Widget _scaledControl(Widget widget, Control? parent, Control control) {
  var scaleDetails = parseScale(control, "scale");
  var animation = parseAnimation(control, "animateScale");
  if (animation != null) {
    return AnimatedScale(
        scale: scaleDetails?.scale! ?? 1.0,
        alignment: scaleDetails?.alignment ?? Alignment.center,
        duration: animation.duration,
        curve: animation.curve,
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

Widget _offsetControl(Widget widget, Control? parent, Control control) {
  var offsetDetails = parseOffset(control, "offset");
  var animation = parseAnimation(control, "animateOffset");
  debugPrint("Animate offset: $offsetDetails $animation");
  if (offsetDetails != null && animation != null) {
    return AnimatedSlide(
        offset: Offset(offsetDetails.x, offsetDetails.y),
        duration: animation.duration,
        curve: animation.curve,
        child: widget);
  }
  return widget;
}

Widget _positionedControl(Widget widget, Control? parent, Control control) {
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
      child: widget,
    );
  } else if (left != null || top != null || right != null || bottom != null) {
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
    if (control.type != ControlType.container &&
        control.type != ControlType.image) {
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
      (parent.type == ControlType.view ||
          parent.type == ControlType.column ||
          parent.type == ControlType.row)) {
    debugPrint("Expandable ${control.id}");
    int? expand = control.attrInt("expand");
    return expand != null ? Expanded(child: widget, flex: expand) : widget;
  }
  return widget;
}
