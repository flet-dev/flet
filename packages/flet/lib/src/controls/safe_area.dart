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
  final bool? parentAdaptive;

  const SafeAreaControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("SafeArea build: ${control.id}");

    var contentCtrls = children.where((c) => c.name == "content" && c.visible);
    bool disabled = control.disabled || parentDisabled;
    bool? adaptive = control.getBool("adaptive") ?? parentAdaptive;
    var safeArea = SafeArea(
        left: control.getBool("left", true)!,
        top: control.getBool("top", true)!,
        right: control.getBool("right", true)!,
        bottom: control.getBool("bottom", true)!,
        maintainBottomViewPadding:
            control.getBool("maintainBottomViewPadding", false)!,
        minimum: parseEdgeInsets(control, "minimumPadding") ??
            parseEdgeInsets(control, "minimum") ??
            EdgeInsets.zero,
        child: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : const ErrorControl(
                "SafeArea.content must be provided and visible"));

    return constrainedControl(context, safeArea, parent, control);
  }
}
