import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/text.dart';
import 'create_control.dart';

class CupertinoDialogActionControl extends StatefulWidget {
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
  State<CupertinoDialogActionControl> createState() =>
      _CupertinoDialogActionControlState();
}

class _CupertinoDialogActionControlState
    extends State<CupertinoDialogActionControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${widget.control.id}");

    final server = FletAppServices.of(context).server;

    String text = widget.control.attrString("text", "")!;
    var contentCtrls = widget.children.where((c) => c.name == "content");
    bool isDefaultAction = widget.control.attrBool("isDefaultAction", false)!;
    bool isDestructiveAction =
        widget.control.attrBool("isDestructiveAction", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("CupertinoDialogAction ${widget.control.id} clicked!");
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    CupertinoDialogAction? cupertinoDialogAction;

    cupertinoDialogAction = CupertinoDialogAction(
        onPressed: onPressed,
        isDefaultAction: isDefaultAction,
        isDestructiveAction: isDestructiveAction,
        textStyle:
            parseTextStyle(Theme.of(context), widget.control, "textStyle"),
        child: contentCtrls.isNotEmpty
            ? createControl(widget.control, contentCtrls.first.id, disabled)
            : Text(text));

    return baseControl(
        context, cupertinoDialogAction, widget.parent, widget.control);
  }
}
