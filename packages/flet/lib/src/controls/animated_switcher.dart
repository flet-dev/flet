import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import 'create_control.dart';
import 'error.dart';

class AnimatedSwitcherControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final bool? parentAdaptive;

  const AnimatedSwitcherControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.parentAdaptive});

  @override
  Widget build(BuildContext context) {
    debugPrint("AnimatedSwitcher build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);

    var switchInCurve =
        parseCurve(control.attrString("switchInCurve"), Curves.linear)!;
    var switchOutCurve =
        parseCurve(control.attrString("switchOutCurve"), Curves.linear)!;
    var duration = control.attrInt("duration", 1000)!;
    var reverseDuration = control.attrInt("reverseDuration", 1000)!;
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl(
          "AnimatedSwitcher.content must be provided and visible");
    }

    var child = createControl(control, contentCtrls.first.id, disabled,
        parentAdaptive: parentAdaptive);

    return constrainedControl(
        context,
        AnimatedSwitcher(
            duration: Duration(milliseconds: duration),
            reverseDuration: Duration(milliseconds: reverseDuration),
            switchInCurve: switchInCurve,
            switchOutCurve: switchOutCurve,
            transitionBuilder: (child, animation) {
              switch (control.attrString("transition", "")!.toLowerCase()) {
                case "rotation":
                  return RotationTransition(turns: animation, child: child);
                case "scale":
                  return ScaleTransition(scale: animation, child: child);
                default:
                  return FadeTransition(opacity: animation, child: child);
              }
            },
            child: child),
        parent,
        control);
  }
}
