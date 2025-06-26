import 'package:flutter/material.dart';

import '../extensions/control.dart';
import '../models/control.dart';
import '../utils/edge_insets.dart';
import '../utils/numbers.dart';
import '../widgets/error.dart';
import 'base_controls.dart';

class SafeAreaControl extends StatelessWidget {
  final Control control;

  const SafeAreaControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("SafeArea build: ${control.id}");

    final safeArea = SafeArea(
        left: control.getBool("avoid_intrusions_left", true)!,
        top: control.getBool("avoid_intrusions_top", true)!,
        right: control.getBool("avoid_intrusions_right", true)!,
        bottom: control.getBool("avoid_intrusions_bottom", true)!,
        maintainBottomViewPadding:
            control.getBool("maintain_bottom_view_padding", false)!,
        minimum: control.getEdgeInsets("minimum_padding", EdgeInsets.zero)!,
        child: control.buildWidget("content") ??
            const ErrorControl(
                "SafeArea.content must be provided and visible"));

    return ConstrainedControl(control: control, child: safeArea);
  }
}
