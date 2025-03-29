import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import 'create_control.dart';

class ProgressBarControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressBarControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressBar build: ${control.id}");

    return constrainedControl(
        context,
        LinearProgressIndicator(
          value: control.getDouble("value"),
          minHeight: control.getDouble("minHeight", 4)!,
          color: control.getColor("color", context),
          backgroundColor: control.getColor("bgColor", context),
          semanticsLabel: control.getString("semanticsLabel"),
          semanticsValue: control.getDouble("semanticsValue")?.toString(),
          borderRadius:
              parseBorderRadius(control, "borderRadius", BorderRadius.zero)!,
        ),
        parent,
        control);
  }
}
