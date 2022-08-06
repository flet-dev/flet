import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class VerticalDividerControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const VerticalDividerControl(
      {Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("VerticalDivider build: ${control.id}");

    var width = control.attrDouble("width");
    var thickness = control.attrDouble("thickness");
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);

    return baseControl(
        VerticalDivider(
          width: width,
          thickness: thickness,
          color: color,
        ),
        parent,
        control);
  }
}
