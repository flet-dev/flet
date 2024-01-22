import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class CardControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const CardControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled});

  @override
  Widget build(BuildContext context) {
    debugPrint("Card build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    bool disabled = control.isDisabled || parentDisabled;

    return constrainedControl(
        context,
        Card(
            elevation: control.attrDouble("elevation"),
            shape: parseOutlinedBorder(control, "shape"),
            margin: parseEdgeInsets(control, "margin"),
            color: HexColor.fromString(
                Theme.of(context), control.attrString("color", "")!),
            shadowColor: HexColor.fromString(
                Theme.of(context), control.attrString("shadowColor", "")!),
            surfaceTintColor: HexColor.fromString(
                Theme.of(context), control.attrString("surfaceTintColor", "")!),
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled)
                : null),
        parent,
        control);
  }
}
