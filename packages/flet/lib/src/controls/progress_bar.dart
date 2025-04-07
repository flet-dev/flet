import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import '../utils/colors.dart';
import '../utils/numbers.dart';
import 'base_controls.dart';

class ProgressBarControl extends StatelessWidget {
  final Control control;

  const ProgressBarControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("ProgressBar build: ${control.id}");
    final indicator = LinearProgressIndicator(
      value: control.getDouble("value"),
      minHeight: control.getDouble("bar_height", 4)!,
      color: control.getColor("color", context),
      backgroundColor: control.getColor("bgcolor", context),
      semanticsLabel: control.getString("semantics_label"),
      semanticsValue: control.getDouble("semantics_value")?.toString(),
      borderRadius:
          control.getBorderRadius("border_radius", BorderRadius.zero)!,
      stopIndicatorColor: control.getColor("stop_indicator_color", context),
      stopIndicatorRadius: control.getDouble("stop_indicator_radius"),
      trackGap: control.getDouble("track_gap"),
      year2023: control.getBool(
          "year_2023"), // todo: deprecated and to be removed in future versions
    );
    return ConstrainedControl(control: control, child: indicator);
  }
}
