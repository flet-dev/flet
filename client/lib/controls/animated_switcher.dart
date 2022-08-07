import 'package:flet_view/controls/error.dart';
import 'package:flet_view/utils/animations.dart';
import 'package:flet_view/utils/gradient.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/borders.dart';
import 'create_control.dart';

class AnimatedSwitcherControl extends StatelessWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const AnimatedSwitcherControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    debugPrint("AnimatedSwitcher build: ${control.id}");

    var contentCtrls =
        children.where((c) => c.name == "content" && c.isVisible);

    var switchInCurve = parseCurve(control.attrString("switchInCurve", "")!);
    var switchOutCurve = parseCurve(control.attrString("switchOutCurve", "")!);
    var duration = control.attrInt("duration", 1000)!;
    var reverseDuration = control.attrInt("reverseDuration", 1000)!;
    bool disabled = control.isDisabled || parentDisabled;

    if (contentCtrls.isEmpty) {
      return const ErrorControl("Content is not set.");
    }

    var child = createControl(control, contentCtrls.first.id, disabled);

    return constrainedControl(
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
