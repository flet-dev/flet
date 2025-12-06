import 'package:flutter/foundation.dart';
import 'package:wakelock_plus/wakelock_plus.dart';

import '../flet_service.dart';

class WakelockService extends FletService {
  WakelockService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("WakelockService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    switch (name) {
      case "enable":
        return WakelockPlus.enable();
      case "disable":
        return WakelockPlus.disable();
      case "is_enabled":
        return WakelockPlus.enabled;
      default:
        throw Exception("Unknown Wakelock method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("WakelockService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
