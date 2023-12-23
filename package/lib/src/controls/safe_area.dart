import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class SafeAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const SafeAreaControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("SafeArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        context,
        SafeArea(
            left: control.attrBool("left", true)!,
            top: control.attrBool("top", true)!,
            right: control.attrBool("right", true)!,
            bottom: control.attrBool("bottom", true)!,
            maintainBottomViewPadding:
                control.attrBool("maintainBottomViewPadding", false)!,
            minimum: parseEdgeInsets(control, "minimum") ?? EdgeInsets.zero,
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : const ErrorControl("SafeArea has no content.")),
        parent,
        control);
  }
}
