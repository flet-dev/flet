import 'package:flet/src/utils/borders.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class ProgressBarControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressBarControl(
      {super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressBar build: ${control.id}");

    var value = control.attrDouble("value");
    var semanticsValue = control.attrDouble("semanticsValue");
    var semanticsLabel = control.attrString("semanticsLabel");
    var barHeight = control.attrDouble("barHeight", 4)!;
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);

    return constrainedControl(
        context,
        LinearProgressIndicator(
          value: value,
          minHeight: barHeight,
          color: color,
          backgroundColor: bgColor,
          semanticsLabel: semanticsLabel,
          semanticsValue: semanticsValue.toString(),
          borderRadius:
              parseBorderRadius(control, "borderRadius") ?? BorderRadius.zero,
        ),
        parent,
        control);
  }
}
