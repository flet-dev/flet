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
    var divider = VerticalDivider(
      width: control.getDouble("width"),
      thickness: control.getDouble("thickness"),
      color: control.getColor("color", context),
      indent: control.getDouble("leadingIndent"),
      endIndent: control.getDouble("trailingIndent"),
    );

    return baseControl(context, divider, parent, control);
  }
}
