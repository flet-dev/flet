import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

class MyControl extends StatelessWidget {
  late final Control? parent;
  late final Control control;
  late final List<Control> children;
  late final bool parentDisabled;
  late final bool? parentAdaptive;

  MyControl(CreateControlArgs args, {super.key}) {
    parent = args.parent;
    control = args.control;
    children = args.children;
    parentDisabled = args.parentDisabled;
    parentAdaptive = args.parentAdaptive;
  }

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
                ? createControl(control, contentCtrls.first.id, disabled,
                    parentAdaptive: parentAdaptive)
                : null),
        parent,
        control);
  }
}
