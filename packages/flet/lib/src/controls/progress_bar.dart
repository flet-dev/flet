import 'package:flet/src/extensions/control.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import 'base_controls.dart';

class ProgressBarControl extends StatelessWidget {
  //final Control? parent;
  final Control control;

  const ProgressBarControl({
    super.key,
    //required this.parent,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressBar build: ${control.id}");

    return ConstrainedControl(
      control: control,
      child: LinearProgressIndicator(
        value: control.getDouble("value"),
        minHeight: control.getDouble("bar_height", 4)!,
        color: control.getColor("color", context),
        backgroundColor: control.getColor("bgcolor", context),
        semanticsLabel: control.getString("semantics_label"),
        semanticsValue: control.getDouble("semantics_value")?.toString(),
        borderRadius:
            parseBorderRadius(control, "borderRadius", BorderRadius.zero)!,
      ),
    );
  }
}
