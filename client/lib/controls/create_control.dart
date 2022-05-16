import 'card.dart';
import 'navigation_rail.dart';

import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/app_state.dart';
import '../models/control.dart';
import '../models/control_type.dart';
import '../models/control_view_model.dart';
import 'alert_dialog.dart';
import 'banner.dart';
import 'checkbox.dart';
import 'circle_avatar.dart';
import 'clipboard.dart';
import 'column.dart';
import 'container.dart';
import 'divider.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'floating_action_button.dart';
import 'grid_view.dart';
import 'icon.dart';
import 'icon_button.dart';
import 'image.dart';
import 'list_view.dart';
import 'outlined_button.dart';
import 'page.dart';
import 'popup_menu_button.dart';
import 'progress_bar.dart';
import 'progress_ring.dart';
import 'radio.dart';
import 'radio_group.dart';
import 'row.dart';
import 'slider.dart';
import 'snack_bar.dart';
import 'stack.dart';
import 'switch.dart';
import 'tabs.dart';
import 'text.dart';
import 'text_button.dart';
import 'textfield.dart';
import 'vertical_divider.dart';

// abstract class ControlWidget extends Widget {
//   const ControlWidget(
//       {Key? key,
//       required Control parent,
//       required Control control,
//       required List<Control> children,
//       required bool parentDisabled})
//       : super(key: key);
// }

Widget createControl(Control? parent, String id, bool parentDisabled) {
  //debugPrint("createControl(): $id");
  return StoreConnector<AppState, ControlViewModel>(
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
              control: controlView.control, children: controlView.children);
        case ControlType.text:
          return TextControl(control: controlView.control);
        case ControlType.icon:
          return IconControl(control: controlView.control);
        case ControlType.clipboard:
          return ClipboardControl(control: controlView.control);
        case ControlType.image:
          return ImageControl(parent: parent, control: controlView.control);
        case ControlType.divider:
          return DividerControl(control: controlView.control);
        case ControlType.verticalDivider:
          return VerticalDividerControl(control: controlView.control);
        case ControlType.circleAvatar:
          return CircleAvatarControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case ControlType.progressRing:
          return ProgressRingControl(control: controlView.control);
        case ControlType.progressBar:
          return ProgressBarControl(control: controlView.control);
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
        case ControlType.card:
          return CardControl(
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
      _sizedControl(
          _tooltip(_opacity(widget, parent, control), parent, control),
          parent,
          control),
      parent,
      control);
}

Widget _opacity(Widget widget, Control? parent, Control control) {
  var opacity = control.attrDouble("opacity");
  return opacity != null
      ? Opacity(
          opacity: opacity,
          child: widget,
        )
      : widget;
}

Widget _tooltip(Widget widget, Control? parent, Control control) {
  var tooltip = control.attrString("tooltip");
  return tooltip != null
      ? Tooltip(
          message: tooltip,
          padding: const EdgeInsets.all(4.0),
          child: widget,
          waitDuration: const Duration(milliseconds: 800),
        )
      : widget;
}

Widget _sizedControl(Widget widget, Control? parent, Control control) {
  var width = control.attrDouble("width", null);
  var height = control.attrDouble("height", null);
  if (width != null || height != null) {
    return ConstrainedBox(
      constraints: BoxConstraints.tightFor(width: width, height: height),
      child: widget,
    );
  }
  return widget;
}

Widget _expandable(Widget widget, Control? parent, Control control) {
  if (parent != null &&
      (parent.type == ControlType.page ||
          parent.type == ControlType.column ||
          parent.type == ControlType.row)) {
    int? expand = control.attrInt("expand");
    return expand != null ? Expanded(child: widget, flex: expand) : widget;
  }
  return widget;
}
