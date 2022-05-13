import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../web_socket_client.dart';
import 'create_control.dart';
import 'error.dart';

class IconButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const IconButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    Color? iconColor =
        HexColor.fromString(context, control.attrString("iconColor", "")!);
    Color? bgColor =
        HexColor.fromString(context, control.attrString("bgColor", "")!);
    double? iconSize = control.attrDouble("iconSize");
    var contentCtrls = children.where((c) => c.name == "content");
    bool autofocus = control.attrBool("autofocus", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = disabled
        ? null
        : () {
            debugPrint("Button ${control.id} clicked!");
            ws.pageEventFromWeb(
                eventTarget: control.id,
                eventName: "click",
                eventData: control.attrs["data"] ?? "");
          };

    Widget? button;

    if (icon != null) {
      button = IconButton(
          autofocus: autofocus,
          icon: Icon(
            icon,
            color: iconColor,
          ),
          iconSize: iconSize,
          onPressed: onPressed);
    } else if (contentCtrls.isNotEmpty) {
      button = IconButton(
          autofocus: autofocus,
          onPressed: onPressed,
          iconSize: iconSize,
          icon: createControl(control, contentCtrls.first.id, disabled));
    } else {
      return const ErrorControl(
          "Icon button does not have an icon neither content specified.");
    }

    if (bgColor != null) {
      button = Container(
        decoration:
            ShapeDecoration(color: bgColor, shape: const CircleBorder()),
        child: button,
      );
    }

    return constrainedControl(button, parent, control);
  }
}
