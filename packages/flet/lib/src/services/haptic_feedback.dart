import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';

import '../flet_service.dart';

class HapticFeedbackService extends FletService {
  HapticFeedbackService({required super.control, required super.backend});

  @override
  void init() {
    super.init();
    debugPrint(
        "HapticFeedbackService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  @override
  void update() {
    debugPrint(
        "HapticFeedbackService(${control.id}).update: ${control.properties}");
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("HapticFeedbackService.$name($args)");
    switch (name) {
      case "heavy_impact":
        await HapticFeedback.heavyImpact();
        break;
      case "light_impact":
        await HapticFeedback.lightImpact();
        break;
      case "medium_impact":
        await HapticFeedback.mediumImpact();
        break;
      case "vibrate":
        await HapticFeedback.vibrate();
        break;
      case "selection_click":
        await HapticFeedback.selectionClick();
        break;
      default:
        throw Exception("Unknown HapticFeedback method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("HapticFeedbackService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
