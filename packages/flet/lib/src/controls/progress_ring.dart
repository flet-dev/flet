import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/box.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/misc.dart';
import '../utils/numbers.dart';
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
      strokeWidth: control.getDouble("stroke_width"),
      color: control.getColor("color", context),
      backgroundColor: control.getColor("bgcolor", context),
      semanticsLabel: control.getString("semantics_label"),
      strokeCap: control.getStrokeCap("stroke_cap"),
      semanticsValue: control.getDouble("semantics_value")?.toString(),
      strokeAlign: control.getDouble("stroke_align"),
      trackGap: control.getDouble("track_gap"),
      constraints: control.getBoxConstraints("size_constraints"),
      padding: control.getPadding("padding"),
      // ignore: deprecated_member_use
      year2023: control.getBool(
          "year2023"), // todo: deprecated and to be removed in future versions
    );
    return LayoutControl(control: control, child: indicator);
  }
}
