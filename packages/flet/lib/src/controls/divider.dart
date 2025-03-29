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
      height: control.getDouble("height"),
      thickness: control.getDouble("thickness"),
      color: control.getColor("color", context),
      indent: control.getDouble("leadingIndent"),
      endIndent: control.getDouble("trailingIndent"),
    );
    return baseControl(context, divider, parent, control);
  }
}
