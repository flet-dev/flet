import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class DividerControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const DividerControl({super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Divider build: ${control.id}");

    var height = control.attrDouble("height");
    var thickness = control.attrDouble("thickness");
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);

    return baseControl(
        context,
        Divider(
          height: height,
          thickness: thickness,
          color: color,
        ),
        parent,
        control);
  }
}
