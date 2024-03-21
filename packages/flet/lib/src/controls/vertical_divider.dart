import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class VerticalDividerControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const VerticalDividerControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("VerticalDivider build: ${control.id}");

    var width = control.attrDouble("width");
    var thickness = control.attrDouble("thickness");
    var leadingIndent = control.attrDouble("leadingIndent");
    var trailingIndent = control.attrDouble("trailingIndent");
    var color = control.attrColor("color", context);

    return baseControl(
        context,
        VerticalDivider(
          width: width,
          thickness: thickness,
          color: color,
          indent: leadingIndent,
          endIndent: trailingIndent,
        ),
        parent,
        control);
  }
}
