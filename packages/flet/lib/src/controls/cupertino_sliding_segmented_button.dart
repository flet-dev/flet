import 'package:flutter/cupertino.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class CupertinoSlidingSegmentedButtonControl extends StatelessWidget {
  final Control control;

  const CupertinoSlidingSegmentedButtonControl(
      {super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CupertinoSlidingSegmentedButtonControl build: ${control.id}");

    var controls = control.buildWidgets("controls");

    if (controls.length < 2) {
      return const ErrorControl(
          "CupertinoSlidingSegmentedButton must have at minimum two visible controls");
    }

    var button = CupertinoSlidingSegmentedControl(
      groupValue: control.getInt("selected_index"),
      proportionalWidth: control.getBool("proportional_width", false)!,
      backgroundColor: control.getColor(
          "bgcolor", context, CupertinoColors.tertiarySystemFill)!,
      padding: control.getPadding(
          "padding", const EdgeInsets.symmetric(vertical: 2, horizontal: 3))!,
      thumbColor: control.getColor(
          "thumb_color",
          context,
          const CupertinoDynamicColor.withBrightness(
            color: Color(0xFFFFFFFF),
            darkColor: Color(0xFF636366),
          ))!,
      children: controls.asMap().map((i, c) => MapEntry(i, c)),
      onValueChanged: (int? index) {
        if (!control.disabled) {
          control
              .updateProperties({"selected_index": index ?? 0}, notify: true);
          control.triggerEvent("change", data: index);
        }
      },
    );

    return ConstrainedControl(control: control, child: button);
  }
}
