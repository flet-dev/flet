import 'package:flet/src/utils/box.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/icons.dart';
import 'create_control.dart';

class IconControl extends StatelessWidget {
  final Control? parent;
  final Control control;

  const IconControl({super.key, required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Icon build: ${control.id}");

    return constrainedControl(
        context,
        Icon(
          parseIcon(control.attrString("name", "")!),
          size: control.attrDouble("size"),
          color: control.attrColor("color", context),
          semanticLabel: control.attrString("semanticsLabel"),
          applyTextScaling: control.attrBool("applyTextScaling"),
          fill: control.attrDouble("fill"),
          grade: control.attrDouble("grade"),
          weight: control.attrDouble("weight"),
          opticalSize: control.attrDouble("opticalSize"),
          shadows: parseBoxShadow(Theme.of(context), control, "shadows"),
        ),
        parent,
        control);
  }
}
