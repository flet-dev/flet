import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/text.dart';
import 'create_control.dart';

class CupertinoDialogActionControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CupertinoDialogActionControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${control.id}");

    final server = FletAppServices.of(context).server;

    String text = control.attrString("text", "")!;
    var contentCtrls = children.where((c) => c.name == "content");
    bool isDefaultAction = control.attrBool("isDefaultAction", false)!;
    bool isDestructiveAction = control.attrBool("isDestructiveAction", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("CupertinoDialogAction ${control.id} clicked!");
            server.sendPageEvent(
                eventTarget: control.id, eventName: "click", eventData: "");
          }
        : null;

    CupertinoDialogAction? cupertinoDialogAction;

    cupertinoDialogAction = CupertinoDialogAction(
        onPressed: onPressed,
        isDefaultAction: isDefaultAction,
        isDestructiveAction: isDestructiveAction,
        textStyle: parseTextStyle(Theme.of(context), control, "textStyle"),
        child: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled)
            : Text(text));

    return baseControl(context, cupertinoDialogAction, parent, control);
  }
}
