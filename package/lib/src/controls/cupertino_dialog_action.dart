import 'package:flutter/cupertino.dart';
import '../flet_app_services.dart';
import '../models/control.dart';
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

    CupertinoDialogAction? button;
    Widget child;

    if (contentCtrls.isNotEmpty) {
      child = createControl(widget.control, contentCtrls.first.id, disabled);
    } else {
      child = Text(text);
    }

    button = CupertinoDialogAction(
        onPressed: onPressed,
        isDefaultAction: isDefaultAction,
        isDestructiveAction: isDestructiveAction,
        child: child);

    return constrainedControl(context, button, widget.parent, widget.control);
  }
}
