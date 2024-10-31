import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/others.dart';
import 'create_control.dart';

class ProgressRingControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressRingControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressRing build: ${control.id}");

    return constrainedControl(
        context,
        CircularProgressIndicator(
          value: control.attrDouble("value"),
          strokeWidth: control.attrDouble("strokeWidth", 4)!,
          color: control.attrColor("color", context),
          backgroundColor: control.attrColor("bgColor", context),
          semanticsLabel: control.attrString("semanticsLabel"),
          strokeCap: parseStrokeCap(control.attrString("strokeCap")),
          semanticsValue: control.attrDouble("semanticsValue")?.toString(),
          strokeAlign: control.attrDouble("strokeAlign", 0)!,
        ),
        parent,
        control);
  }
}
