import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoActionSheetButtonControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoActionSheetButtonControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  State<CupertinoActionSheetButtonControl> createState() =>
      _CupertinoActionSheetButtonControlState();
}

class _CupertinoActionSheetButtonControlState
    extends State<CupertinoActionSheetButtonControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetButtonControl build: ${widget.control.id}");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var contentCtrls =
        widget.children.where((c) => c.name == "content" && c.isVisible);
    if (contentCtrls.isEmpty) {
      return ErrorControl(
          "CupertinoActionSheetButton must have a content control!");
    }

    return constrainedControl(
        context,
        CupertinoActionSheetAction(
          isDefaultAction: widget.control.attrBool("default", false)!,
          isDestructiveAction: widget.control.attrBool("destructive", false)!,
          onPressed: () {
            widget.backend.triggerControlEvent(widget.control.id, "click", "");
          },
          child: createControl(widget.control, contentCtrls.first.id, disabled,
              parentAdaptive: widget.parentAdaptive),
        ),
        widget.parent,
        widget.control);
  }
}
