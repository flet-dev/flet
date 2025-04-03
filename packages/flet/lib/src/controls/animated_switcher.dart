import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/time.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class AnimatedSwitcherControl extends StatelessWidget {
  final Control control;

  const AnimatedSwitcherControl({
    super.key,
    required this.control,
  });

  @override
  Widget build(BuildContext context) {
    debugPrint("AnimatedSwitcher build: ${control.id}");

    var content =
        control.buildWidget("content", notifyParent: true, key: UniqueKey());

    if (content == null) {
      return const ErrorControl(
          "AnimatedSwitcher.content must be provided and visible");
    }
    final animatedSwitcher = AnimatedSwitcher(
      duration:
          parseDuration(control.get("duration"), const Duration(seconds: 1))!,
      reverseDuration: parseDuration(
          control.get("reverse_duration"), const Duration(seconds: 1))!,
      switchInCurve:
          parseCurve(control.getString("switch_in_curve"), Curves.linear)!,
      switchOutCurve:
          parseCurve(control.getString("switch_out_curve"), Curves.linear)!,
      transitionBuilder: (child, animation) {
        switch (control.getString("transition")?.toLowerCase()) {
          case "rotation":
            return RotationTransition(turns: animation, child: child);
          case "scale":
            return ScaleTransition(scale: animation, child: child);
          default:
            return FadeTransition(opacity: animation, child: child);
        }
      },
      child: content,
    );
    return ConstrainedControl(control: control, child: animatedSwitcher);
  }
}
