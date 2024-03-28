import 'package:collection/collection.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'create_control.dart';

class ProgressRingControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressRingControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressRing build: ${control.id}");

    var value = control.attrDouble("value");
    var semanticsValue = control.attrDouble("semanticsValue");
    var strokeAlign = control.attrDouble("strokeAlign", 0)!;
    var semanticsLabel = control.attrString("semanticsLabel");
    var strokeCap = StrokeCap.values.firstWhereOrNull((e) =>
        e.name.toLowerCase() ==
        control.attrString("strokeCap", "")!.toLowerCase());
    var strokeWidth = control.attrDouble("strokeWidth", 4)!;
    var color = control.attrColor("color", context);
    var bgColor = control.attrColor("bgColor", context);

    return constrainedControl(
        context,
        CircularProgressIndicator(
          value: value,
          strokeWidth: strokeWidth,
          color: color,
          backgroundColor: bgColor,
          semanticsLabel: semanticsLabel,
          strokeCap: strokeCap,
          semanticsValue: semanticsValue.toString(),
          strokeAlign: strokeAlign,
        ),
        parent,
        control);
  }
}
