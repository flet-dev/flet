import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';
import 'error.dart';

class FloatingActionButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const FloatingActionButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("FloatingActionButtonControl build: ${control.id}");

    final ws = FletAppServices.of(context).ws;

    String? text = control.attrString("text");
    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    Color? bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    var contentCtrls = children.where((c) => c.name == "content");
    var tooltip = control.attrString("tooltip");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("FloatingActionButtonControl ${control.id} clicked!");
            ws.pageEventFromWeb(
                eventTarget: control.id, eventName: "click", eventData: "");
          };

    if (text == null && icon == null && contentCtrls.isEmpty) {
      return const ErrorControl(
          "FAB doesn't have a text, nor icon, nor content.");
    }

    Widget button;
    if (contentCtrls.isNotEmpty) {
      button = FloatingActionButton(
          autofocus: autofocus,
          onPressed: onPressed,
          backgroundColor: bgColor,
          tooltip: tooltip,
          child: createControl(control, contentCtrls.first.id, disabled));
    } else if (icon != null && text == null) {
      button = FloatingActionButton(
          autofocus: autofocus,
          onPressed: onPressed,
          child: Icon(icon),
          backgroundColor: bgColor,
          tooltip: tooltip);
    } else if (icon == null && text != null) {
      button = FloatingActionButton(
        autofocus: autofocus,
        onPressed: onPressed,
        child: Text(text),
        backgroundColor: bgColor,
        tooltip: tooltip,
      );
    } else if (icon != null && text != null) {
      button = FloatingActionButton.extended(
        autofocus: autofocus,
        onPressed: onPressed,
        label: Text(text),
        icon: Icon(icon),
        backgroundColor: bgColor,
        tooltip: tooltip,
      );
    } else {
      return const ErrorControl("FAB doesn't have a text, nor icon.");
    }

    return constrainedControl(button, parent, control);
  }
}
