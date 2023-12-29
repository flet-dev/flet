import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class SemanticsControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SemanticsControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("Semantics build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var label = control.attrString("label");
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        context,
        Semantics(
            label: label,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : null),
        parent,
        control);
  }
}
