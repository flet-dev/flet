import 'package:flet/src/utils/box.dart';
import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/icons.dart';
import '../utils/images.dart';
import 'base_controls.dart';

class IconControl extends StatelessWidget {
  final Control control;

  const IconControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Icon build: ${control.id}");

    return ConstrainedControl(
        control: control,
        child: Icon(
          parseIcon(control.getString("name", "")!),
          size: control.getDouble("size"),
          color: control.getColor("color", context),
          blendMode: parseBlendMode(control.getString("blend_mode")),
          semanticLabel: control.getString("semantics_label"),
          applyTextScaling: control.getBool("apply_text_scaling"),
          fill: control.getDouble("fill"),
          grade: control.getDouble("grade"),
          weight: control.getDouble("weight"),
          opticalSize: control.getDouble("optical_size"),
          shadows: parseBoxShadow(Theme.of(context), control, "shadows"),
        ));
  }
}
