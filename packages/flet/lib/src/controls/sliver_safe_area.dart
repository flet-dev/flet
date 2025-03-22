import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';
import 'error.dart';

class SliverSafeAreaControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const SliverSafeAreaControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("SliverSafeArea build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;
    var safeArea = SliverSafeArea(
        left: control.attrBool("left", true)!,
        top: control.attrBool("top", true)!,
        right: control.attrBool("right", true)!,
        bottom: control.attrBool("bottom", true)!,
        minimum: parseEdgeInsets(control, "minimumPadding") ??
            parseEdgeInsets(control, "minimum") ??
            EdgeInsets.zero,
        sliver: contentCtrls.isNotEmpty
            ? createControl(control, contentCtrls.first.id, disabled,
                parentAdaptive: adaptive)
            : const ErrorControl(
                "SliverSafeArea.content must be provided and visible"));

    return constrainedControl(context, safeArea, parent, control);
  }
}
