import 'package:flutter/widgets.dart';
import 'package:shake/shake.dart';

import '../flet_app_services.dart';
import '../models/control.dart';

class ShakeDetectorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final Widget? nextChild;

  const ShakeDetectorControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.nextChild});

  @override
  State<ShakeDetectorControl> createState() => _ShakeDetectorControlState();
}

class _ShakeDetectorControlState extends State<ShakeDetectorControl> {
  ShakeDetector? _shakeDetector;
  int? _minimumShakeCount;
  int? _shakeSlopTimeMs;
  int? _shakeCountResetTimeMs;
  double? _shakeThresholdGravity;

  @override
  void dispose() {
    _shakeDetector?.stopListening();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("ShakeDetector build: ${widget.control.id}");

    var minimumShakeCount = widget.control.attrInt("minimumShakeCount", 1)!;
    var shakeSlopTimeMs = widget.control.attrInt("shakeSlopTimeMs", 500)!;
    var shakeCountResetTimeMs =
        widget.control.attrInt("shakeCountResetTimeMs", 3000)!;
    var shakeThresholdGravity =
        widget.control.attrDouble("shakeThresholdGravity", 2.7)!;

    if (minimumShakeCount != _minimumShakeCount ||
        shakeSlopTimeMs != _shakeSlopTimeMs ||
        shakeCountResetTimeMs != _shakeCountResetTimeMs ||
        shakeThresholdGravity != _shakeThresholdGravity) {
      _minimumShakeCount = minimumShakeCount;
      _shakeSlopTimeMs = shakeSlopTimeMs;
      _shakeCountResetTimeMs = shakeCountResetTimeMs;
      _shakeThresholdGravity = shakeThresholdGravity;

      _shakeDetector?.stopListening();
      _shakeDetector = ShakeDetector.autoStart(
        onPhoneShake: () {
          FletAppServices.of(context).server.sendPageEvent(
              eventTarget: widget.control.id,
              eventName: "shake",
              eventData: "");
        },
        minimumShakeCount: minimumShakeCount,
        shakeSlopTimeMS: shakeSlopTimeMs,
        shakeCountResetTime: shakeCountResetTimeMs,
        shakeThresholdGravity: shakeThresholdGravity,
      );
    }

    return widget.nextChild ?? const SizedBox.shrink();
  }
}
