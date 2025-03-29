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
          parseIcon(control.getString("name", "")!),
          size: control.getDouble("size"),
          color: control.getColor("color", context),
          semanticLabel: control.getString("semanticsLabel"),
          applyTextScaling: control.getBool("applyTextScaling"),
          fill: control.getDouble("fill"),
          grade: control.getDouble("grade"),
          weight: control.getDouble("weight"),
          opticalSize: control.getDouble("opticalSize"),
          shadows: parseBoxShadow(Theme.of(context), control, "shadows"),
        ),
        parent,
        control);
  }
}
