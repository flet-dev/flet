import 'package:flutter/cupertino.dart';

import '../flet_app_services.dart';
import '../models/control.dart';
import '../utils/launch_url.dart';
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
  late final FocusNode _focusNode;
  String? _lastFocusValue;

  @override
  void initState() {
    super.initState();
    _focusNode = FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    _focusNode.dispose();
    super.dispose();
  }

  void _onFocusChange() {
    FletAppServices.of(context).server.sendPageEvent(
        eventTarget: widget.control.id,
        eventName: _focusNode.hasFocus ? "focus" : "blur",
        eventData: "");
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoDialogAction build: ${widget.control.id}");

    final server = FletAppServices.of(context).server;

    String text = widget.control.attrString("text", "")!;
    var contentCtrls = widget.children.where((c) => c.name == "content");
    String url = widget.control.attrString("url", "")!;
    String? urlTarget = widget.control.attrString("urlTarget");
    bool isDefaultAction = widget.control.attrBool("isDefaultAction", false)!;
    bool isDestructiveAction =
        widget.control.attrBool("isDefaultAction", false)!;
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    Function()? onPressed = !disabled
        ? () {
            debugPrint("Button ${widget.control.id} clicked!");
            if (url != "") {
              openWebBrowser(url, webWindowName: urlTarget);
            }
            server.sendPageEvent(
                eventTarget: widget.control.id,
                eventName: "click",
                eventData: "");
          }
        : null;

    CupertinoDialogAction? button;

    if (contentCtrls.isNotEmpty) {
      button = CupertinoDialogAction(
          onPressed: onPressed,
          isDefaultAction: isDefaultAction,
          isDestructiveAction: isDestructiveAction,
          child:
              createControl(widget.control, contentCtrls.first.id, disabled));
    } else {
      button = CupertinoDialogAction(
          onPressed: onPressed,
          isDefaultAction: isDefaultAction,
          isDestructiveAction: isDestructiveAction,
          child: Text(text));
    }

    var focusValue = widget.control.attrString("focus");
    if (focusValue != null && focusValue != _lastFocusValue) {
      _lastFocusValue = focusValue;
      _focusNode.requestFocus();
    }

    return constrainedControl(context, button, widget.parent, widget.control);
  }
}
