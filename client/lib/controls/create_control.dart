import 'package:flet_view/controls/snack_bar.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/app_state.dart';
import 'row.dart';
import 'textfield.dart';
import 'dropdown.dart';
import 'elevated_button.dart';
import 'page.dart';
import 'stack.dart';
import 'text.dart';
import 'column.dart';

Widget createControl(Control? parent, String id, bool parentDisabled) {
  return StoreConnector<AppState, ControlViewModel>(
    distinct: true,
    converter: (store) {
      //debugPrint("ControlViewModel $id converter");
      return ControlViewModel.fromStore(store, id);
    },
    onWillChange: (prev, next) {
      //debugPrint("${next.type} $id will change");
    },
    builder: (context, controlView) {
      //debugPrint("${control.type} ${control.id} builder");
      switch (controlView.control.type) {
        case "page":
          return PageControl(
              control: controlView.control, children: controlView.children);
        case "text":
          return TextControl(control: controlView.control);
        case "elevatedbutton":
          return ElevatedButtonControl(
              parent: parent,
              control: controlView.control,
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
        case "stack":
          return StackControl(
              parent: parent,
              control: controlView.control,
              children: controlView.children,
              parentDisabled: parentDisabled);
        case "textbox":
          return TextFieldControl(
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
        default:
          throw Exception("Unknown control type: ${controlView.control.type}");
      }
    },
  );
}

Widget expandable(Widget widget, Control control) {
  int? expand = control.attrInt("expand");
  return expand != null ? Expanded(child: widget, flex: expand) : widget;
}
