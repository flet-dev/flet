import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class DividerControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const DividerControl({super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Divider build: ${control.id}");

    var height = control.attrDouble("height");
    var leadingIndent = control.attrDouble("leadingIndent");
    var trailingIndent = control.attrDouble("trailingIndent");
    var thickness = control.attrDouble("thickness");
    var color = control.attrColor("color", context);

    return baseControl(
        context,
        Divider(
          height: height,
          thickness: thickness,
          color: color,
          indent: leadingIndent,
          endIndent: trailingIndent,
        ),
        parent,
        control);
  }
}
