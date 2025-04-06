import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/misc.dart';
import 'base_controls.dart';

class ProgressRingControl extends StatelessWidget {
  final Control control;

  const ProgressRingControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressRing build: ${control.id}");
    final indicator = CircularProgressIndicator(
      value: control.getDouble("value"),
      strokeWidth: control.getDouble("stroke_width", 4)!,
      color: control.getColor("color", context),
      backgroundColor: control.getColor("bgcolor", context),
      semanticsLabel: control.getString("semantics_label"),
      strokeCap: parseStrokeCap(control.getString("stroke_cap")),
      semanticsValue: control.getDouble("semantics_value")?.toString(),
      strokeAlign: control.getDouble("stroke_align", 0)!,
      trackGap: control.getDouble("track_gap"),
      constraints: control.getBoxConstraints("size_constraints"),
      padding: control.getEdgeInsets("padding"),
      year2023: control.getBool(
          "year2023"), // todo: deprecated and to be removed in future versions
    );
    return ConstrainedControl(control: control, child: indicator);
  }
}
