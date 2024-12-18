import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class DividerControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const DividerControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Divider build: ${control.id}");

    var divider = Divider(
      height: control.attrDouble("height"),
      thickness: control.attrDouble("thickness"),
      color: control.attrColor("color", context),
      indent: control.attrDouble("leadingIndent"),
      endIndent: control.attrDouble("trailingIndent"),
    );
    return baseControl(context, divider, parent, control);
  }
}
