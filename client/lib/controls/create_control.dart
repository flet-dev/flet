import 'dart:convert';

import 'package:flet_view/controls/icon.dart';
import 'package:flet_view/controls/snack_bar.dart';
import 'package:flet_view/models/control_type.dart';
import 'package:flet_view/utils/colors.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../models/control.dart';
import '../models/control_view_model.dart';
import '../models/app_state.dart';
import '../utils/theme.dart';
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
        case ControlType.page:
          return PageControl(
              control: controlView.control, children: controlView.children);
        case ControlType.text:
          return TextControl(control: controlView.control);
        case ControlType.icon:
          return IconControl(control: controlView.control);
        case ControlType.elevatedButton:
          return ElevatedButtonControl(
              parent: parent,
              control: controlView.control,
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
        case ControlType.textField:
          return TextFieldControl(
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
        default:
          throw Exception("Unknown control type: ${controlView.control.type}");
      }
    },
  );
}

Widget commonControl(Widget widget, Control? parent, Control control) {
  return _expandable(widget, parent, control);
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

MainAxisAlignment parseMainAxisAlignment(
    Control control, String propName, MainAxisAlignment defValue) {
  return MainAxisAlignment.values.firstWhere(
      (e) => e.name.toLowerCase() == control.attrString(propName, ""),
      orElse: () => defValue);
}

CrossAxisAlignment parseCrossAxisAlignment(
    Control control, String propName, CrossAxisAlignment defValue) {
  return CrossAxisAlignment.values.firstWhere(
      (e) => e.name.toLowerCase() == control.attrString(propName, ""),
      orElse: () => defValue);
}

WrapAlignment parseWrapAlignment(
    Control control, String propName, WrapAlignment defValue) {
  return WrapAlignment.values.firstWhere(
      (e) => e.name.toLowerCase() == control.attrString(propName, ""),
      orElse: () => defValue);
}

WrapCrossAlignment parseWrapCrossAlignment(
    Control control, String propName, WrapCrossAlignment defValue) {
  return WrapCrossAlignment.values.firstWhere(
      (e) => e.name.toLowerCase() == control.attrString(propName, ""),
      orElse: () => defValue);
}

EdgeInsetsGeometry? parseEdgeInsets(Control control, String propName) {
  var d = control.attrDouble(propName, null);
  if (d == null) {
    return null;
  }
  return EdgeInsets.all(d);
}

Color? parseColor(Control control, String propName) {
  var c = control.attrString(propName, null);
  if (c == null) {
    return null;
  }

  return HexColor.fromString(c);
}

ThemeData? parseTheme(Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j1 = json.decode(v);
  return themeFromJson(j1);
}
