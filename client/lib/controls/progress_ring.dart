import 'package:flet_view/controls/create_control.dart';
import 'package:flet_view/utils/colors.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';

class ProgressRingControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const ProgressRingControl({Key? key, this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressRing build: ${control.id}");

    var value = control.attrDouble("value", null);
    var strokeWidth = control.attrDouble("strokeWidth", 4)!;
    var color = HexColor.fromString(context, control.attrString("color", "")!);
    var bgColor =
        HexColor.fromString(context, control.attrString("bgColor", "")!);

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
