import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/icons.dart';
import '../utils/images.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class IconControl extends StatelessWidget {
  final Control control;

  const IconControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("Icon build: ${control.id}");

    return LayoutControl(
        control: control,
        child: Icon(
          control.getIconData("icon"),
          size: control.getDouble("size"),
          color: control.getColor("color", context),
          blendMode: control.getBlendMode("blend_mode"),
          semanticLabel: control.getString("semantics_label"),
          applyTextScaling: control.getBool("apply_text_scaling"),
          fill: control.getDouble("fill"),
          grade: control.getDouble("grade"),
          weight: control.getDouble("weight"),
          opticalSize: control.getDouble("optical_size"),
          shadows: control.getBoxShadows("shadows", Theme.of(context)),
        ));
  }
}
