import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../models/control.dart';
import 'flet_control_stateful_mixin.dart';

class HapticFeedbackControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;

  const HapticFeedbackControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild});

  @override
  State<HapticFeedbackControl> createState() => _HapticFeedbackControlState();
}

class _HapticFeedbackControlState extends State<HapticFeedbackControl>
    with FletControlStatefulMixin {
  @override
  void deactivate() {
    unsubscribeMethods(widget.control.id);
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("HapticFeedback build: ${widget.control.id}");

    subscribeMethods(widget.control.id, (methodName, args) async {
      switch (methodName) {
        case "heavy_impact":
          HapticFeedback.heavyImpact();
          break;
        case "light_impact":
          HapticFeedback.lightImpact();
          break;
        case "medium_impact":
          HapticFeedback.mediumImpact();
          break;
        case "vibrate":
          HapticFeedback.vibrate();
          break;
      }
      return null;
    });

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
