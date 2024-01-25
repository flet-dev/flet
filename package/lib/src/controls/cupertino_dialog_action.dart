import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/text.dart';
import 'create_control.dart';
import 'flet_stateless_control.dart';

class CupertinoDialogActionControl extends StatelessWidget
    with FletStatelessControl {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CupertinoDialogActionControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${control.id}");

    String text = control.attrString("text", "")!;
    var contentCtrls = children.where((c) => c.name == "content");
    bool isDefaultAction = control.attrBool("isDefaultAction", false)!;
    bool isDestructiveAction = control.attrBool("isDestructiveAction", false)!;
    bool disabled = control.isDisabled || parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("CupertinoDialogAction ${control.id} clicked!");
            sendControlEvent(context, control.id, "click", "");
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
