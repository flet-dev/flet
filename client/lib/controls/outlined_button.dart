import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../web_socket_client.dart';
import 'create_control.dart';

class OutlinedButtonControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const OutlinedButtonControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Button build: ${control.id}");

    String text = control.attrString("text", "")!;
    IconData? icon = getMaterialIcon(control.attrString("icon", "")!);
    Color? iconColor = HexColor.fromString(
        Theme.of(context), control.attrString("iconColor", "")!);
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

    OutlinedButton? button;

    if (icon != null) {
      button = OutlinedButton.icon(
          autofocus: autofocus,
          onPressed: onPressed,
          icon: Icon(
            icon,
            color: iconColor,
          ),
          label: Text(text));
    } else if (contentCtrls.isNotEmpty) {
      button = OutlinedButton(
          autofocus: autofocus,
          onPressed: onPressed,
          child: createControl(control, contentCtrls.first.id, disabled));
    } else {
      button = OutlinedButton(onPressed: onPressed, child: Text(text));
    }

    return constrainedControl(button, parent, control);
  }
}
