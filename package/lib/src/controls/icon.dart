import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import 'create_control.dart';

class IconControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const IconControl({super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Icon build: ${control.id}");

    var name = control.attrString("name", "")!;
    var size = control.attrDouble("size", null);
    var color = HexColor.fromString(
        Theme.of(context), control.attrString("color", "")!);

    return constrainedControl(
        context,
        Icon(
          getMaterialIcon(name),
          size: size,
          color: color,
        ),
        parent,
        control);
  }
}
