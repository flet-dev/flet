import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import 'create_control.dart';

class CardControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const CardControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("Card build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);
    var clipBehavior = Clip.values.firstWhereOrNull(
      (e) =>
          e.name.toLowerCase() ==
          control.attrString("clipBehavior", "")!.toLowerCase(),
    );
    bool disabled = control.isDisabled || parentDisabled;
    bool? adaptive = control.attrBool("adaptive") ?? parentAdaptive;

    return constrainedControl(
        context,
        Card(
            elevation: control.attrDouble("elevation"),
            shape: parseOutlinedBorder(control, "shape"),
            margin: parseEdgeInsets(control, "margin"),
            semanticContainer: control.attrBool("semanticContainer", true)!,
            borderOnForeground: control.attrBool("borderOnForeground", true)!,
            clipBehavior: clipBehavior,
            color: HexColor.fromString(
                Theme.of(context), control.attrString("color", "")!),
            shadowColor: HexColor.fromString(
                Theme.of(context), control.attrString("shadowColor", "")!),
            surfaceTintColor: HexColor.fromString(
                Theme.of(context), control.attrString("surfaceTintColor", "")!),
            child: contentCtrls.isNotEmpty
                ? createControl(control, contentCtrls.first.id, disabled,
                    parentAdaptive: adaptive)
                : null),
        parent,
        control);
  }
}
