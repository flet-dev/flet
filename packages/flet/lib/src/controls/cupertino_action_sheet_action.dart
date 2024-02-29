import 'package:flutter/cupertino.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';
import 'create_control.dart';
import 'error.dart';

class CupertinoActionSheetActionControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;
  final FletControlBackend backend;

  const CupertinoActionSheetActionControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoActionSheetActionControl build: ${control.id}");
    bool disabled = control.isDisabled || parentDisabled;

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "CupertinoActionSheetAction must have a content control!");
    }

    return constrainedControl(
        context,
        CupertinoActionSheetAction(
          isDefaultAction: control.attrBool("default", false)!,
          isDestructiveAction: control.attrBool("destructive", false)!,
          onPressed: () {
            backend.triggerControlEvent(control.id, "click", "");
          },
          child: createControl(control, contentCtrls.first.id, disabled,
              parentAdaptive: parentAdaptive),
        ),
        parent,
        control);
  }
}
