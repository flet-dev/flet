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
          value: control.getDouble("value"),
          strokeWidth: control.getDouble("strokeWidth", 4)!,
          color: control.getColor("color", context),
          backgroundColor: control.getColor("bgColor", context),
          semanticsLabel: control.getString("semanticsLabel"),
          strokeCap: parseStrokeCap(control.getString("strokeCap")),
          semanticsValue: control.getDouble("semanticsValue")?.toString(),
          strokeAlign: control.getDouble("strokeAlign", 0)!,
        ),
        parent,
        control);
  }
}
