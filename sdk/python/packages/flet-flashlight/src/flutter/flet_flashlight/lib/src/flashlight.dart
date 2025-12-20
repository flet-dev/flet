import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:torch_light/torch_light.dart';

class FlashlightControl extends FletService {
  FlashlightControl({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("Flashlight(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Flashlight.$name($args)");
    if (isMobilePlatform()) {
      switch (name) {
        case "on":
          await TorchLight.enableTorch();
        case "off":
          await TorchLight.disableTorch();
        case "is_available":
          return await TorchLight.isTorchAvailable();
        default:
          throw Exception("Unknown Flashlight method: $name");
      }
    } else {
      throw Exception(
          "Flashlight control is supported only on Android and iOS devices.");
    }
  }

  @override
  void dispose() {
    debugPrint("Flashlight(${control.id}).dispose");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
