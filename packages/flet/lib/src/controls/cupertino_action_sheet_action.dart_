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
    bool disabled = control.disabled || parentDisabled;

    var text = control.getString("text");
    var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    if (contentCtrls.isEmpty && text == null) {
      return const ErrorControl(
          "CupertinoActionSheetAction must have at minimum text or (visible) content provided");
    }

    return constrainedControl(
        context,
        CupertinoActionSheetAction(
          isDefaultAction: control.getBool("isDefaultAction", false)!,
          isDestructiveAction: control.getBool("isDestructiveAction", false)!,
          onPressed: () {
            if (!disabled) {
              backend.triggerControlEvent(control.id, "click");
            }
          },
          child: contentCtrls.isNotEmpty
              ? createControl(control, contentCtrls.first.id, disabled,
                  parentAdaptive: parentAdaptive)
              : Text(text!),
        ),
        parent,
        control);
  }
}
