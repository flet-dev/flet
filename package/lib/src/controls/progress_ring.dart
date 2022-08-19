import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class ProgressRingControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressRingControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressRing build: ${control.id}");

    var value = control.attrDouble("value", null);
    var strokeWidth = control.attrDouble("strokeWidth", 4)!;
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);
    var bgColor = HexColor.fromString(
        Theme.of(context), control.attrString("bgColor", "")!);

    return constrainedControl(
        CircularProgressIndicator(
          value: value,
          strokeWidth: strokeWidth,
          color: color,
          backgroundColor: bgColor,
        ),
        parent,
        control);
  }
}
