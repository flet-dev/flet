import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../flet_control_backend.dart';
import '../models/control.dart';

class HapticFeedbackControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;
  final FletControlBackend backend;

  const HapticFeedbackControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild,
      required this.backend});

  @override
  State<HapticFeedbackControl> createState() => _HapticFeedbackControlState();
}

class _HapticFeedbackControlState extends State<HapticFeedbackControl> {
  @override
  void deactivate() {
    widget.backend.unsubscribeMethods(widget.control.id);
    super.deactivate();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("HapticFeedback build: ${widget.control.id}");

    widget.backend.subscribeMethods(widget.control.id,
        (methodName, args) async {
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
