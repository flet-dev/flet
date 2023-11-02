import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import 'create_control.dart';

class BadgeControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const BadgeControl({Key? key, required this.parent, required this.control})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("Badge build: ${control.id}");

    //var height = control.attrDouble("height");
    //var thickness = control.attrDouble("thickness");
    //var color = HexColor.fromString(
    //    Theme.of(context), control.attrString("color", "")!);

    return baseControl(
        context,
        // Divider(
        //   height: height,
        //   thickness: thickness,
        //   color: color,
        // ),
        Badge(
          child: Text("Badge"),
          label: Text('10'),
        ),
        parent,
        control);
  }
}
