import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/launch_url.dart';
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

    String? text = control.attrString("text");
    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    String url = control.attrString("url", "")!;
    String? urlTarget = control.attrString("urlTarget");
    Color? bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);
    OutlinedBorder? shape = parseOutlinedBorder(control, "shape");
    var contentCtrls = children.where((c) => c.name == "content");
    var tooltip = control.attrString("tooltip");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool mini = control.attrBool("mini", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("FloatingActionButtonControl ${control.id} clicked!");
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            FletAppServices.of(context).server.sendPageEvent(
                eventTarget: control.id, eventName: "click", eventData: "");
          };

    if (text == null && icon == null && contentCtrls.isEmpty) {
      return const ErrorControl(
          "FAB doesn't have a text, nor icon, nor content.");
    }

    Widget button;
    if (contentCtrls.isNotEmpty) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          backgroundColor: bgColor,
          tooltip: tooltip,
          shape: shape,
          mini: mini,
          child: createControl(control, contentCtrls.first.id, disabled));
    } else if (icon != null && text == null) {
      button = FloatingActionButton(
          heroTag: control.id,
          autofocus: autofocus,
          onPressed: onPressed,
          backgroundColor: bgColor,
          tooltip: tooltip,
          shape: shape,
          mini: mini,
          child: Icon(icon));
    } else if (icon == null && text != null) {
      button = FloatingActionButton(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        backgroundColor: bgColor,
        tooltip: tooltip,
        shape: shape,
        mini: mini,
        child: Text(text),
      );
    } else if (icon != null && text != null) {
      button = FloatingActionButton.extended(
        heroTag: control.id,
        autofocus: autofocus,
        onPressed: onPressed,
        label: Text(text),
        icon: Icon(icon),
        backgroundColor: bgColor,
        tooltip: tooltip,
        shape: shape,
      );
    } else {
      return const ErrorControl("FAB doesn't have a text, nor icon.");
    }

    return constrainedControl(context, button, parent, control);
  }
}
