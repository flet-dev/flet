import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class SemanticsControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SemanticsControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Semantics build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var label = control.attrString("label");
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        Semantics(
            label: label,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : null),
        parent,
        control);
  }
}
