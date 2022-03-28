import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:flet_view/controls/dropdown.dart';
import 'package:flet_view/models/control_view_model.dart';
import '../models/app_state.dart';
import 'textfield.dart';

import 'button.dart';
import 'page.dart';
import 'stack.dart';
import 'text.dart';
import 'column.dart';

Widget createControl(String id) {
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
        case "button":
          return ButtonControl(control: controlView.control);
        case "column":
          return ColumnControl(
              control: controlView.control, children: controlView.children);
        case "stack":
          return StackControl(
              control: controlView.control, children: controlView.children);
        case "textbox":
          return TextFieldControl(control: controlView.control);
        case "dropdown":
          return DropdownControl(control: controlView.control);
        default:
          throw Exception("Unknown control type: ${controlView.control.type}");
      }
    },
  );
}
