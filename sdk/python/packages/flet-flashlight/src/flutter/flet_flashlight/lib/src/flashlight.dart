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
      Map<String, String?>? errorInfo;
      switch (name) {
        case "on":
          try {
            await TorchLight.enableTorch();
            return true;
          } catch (e) {
            if (e is EnableTorchExistentUserException) {
              errorInfo = {
                "error_type": "EnableTorchExistentUserException",
                "error_msg": e.message
              };
            } else if (e is EnableTorchNotAvailableException) {
              errorInfo = {
                "error_type": "EnableTorchNotAvailableException",
                "error_msg": e.message
              };
            } else {
              errorInfo = {
                "error_type": "EnableTorchException",
                "error_msg": (e as EnableTorchException).message
              };
            }
            control.triggerEvent("error", errorInfo);
            debugPrint(
                "Error enabling Flashlight: ${errorInfo["error_type"]}(${errorInfo["error_msg"]})");
            return errorInfo;
          }
        case "off":
          try {
            await TorchLight.disableTorch();
            return true;
          } catch (e) {
            if (e is DisableTorchExistentUserException) {
              errorInfo = {
                "error_type": "DisableTorchExistentUserException",
                "error_msg": e.message
              };
            } else if (e is DisableTorchNotAvailableException) {
              errorInfo = {
                "error_type": "DisableTorchNotAvailableException",
                "error_msg": e.message
              };
            } else {
              errorInfo = {
                "error_type": "DisableTorchException",
                "error_msg": (e as DisableTorchException).message
              };
            }
            control.triggerEvent("error", errorInfo);
            debugPrint(
                "Error disabling Flashlight: ${errorInfo["error_type"]}(${errorInfo["error_msg"]})");
            return errorInfo;
          }
        case "is_available":
          try {
            final available = await TorchLight.isTorchAvailable();
            return available;
          } on EnableTorchException catch (e) {
            errorInfo = {
              "error_type": "EnableTorchException",
              "error_msg": e.message
            };
            control.triggerEvent("error", errorInfo);
            debugPrint(
                "Error checking Flashlight availability: EnableTorchException(${e.message})");
            return errorInfo;
          }
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
