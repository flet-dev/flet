import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';

import 'utils/local_auth.dart';

class LocalAuthenticationService extends FletService {
  LocalAuthenticationService({required super.control});

  final LocalAuthentication _auth = LocalAuthentication();

  @override
  void init() {
    super.init();
    debugPrint(
      "LocalAuthenticationService(${control.id}).init: ${control.properties}",
    );
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("LocalAuthentication.$name($args)");
    switch (name) {
      case "is_device_supported":
        return await _auth.isDeviceSupported();
      case "can_check_biometrics":
        return await _auth.canCheckBiometrics;
      case "get_available_biometrics":
        return (await _auth.getAvailableBiometrics())
            .map(parseBiometricTypeName)
            .toList();
      case "authenticate":
        try {
          return await _auth.authenticate(
            localizedReason: args["reason"]!,
            authMessages: parseAuthMessages(args),
            biometricOnly: args["biometric_only"] as bool? ?? false,
            sensitiveTransaction:
                args["sensitive_transaction"] as bool? ?? true,
            persistAcrossBackgrounding:
                args["persist_across_backgrounding"] as bool? ?? false,
          );
        } on LocalAuthException catch (e) {
          return localAuthErrorMap(e);
        }
      case "stop_authentication":
        return await _auth.stopAuthentication();
      default:
        throw Exception("Unknown LocalAuthentication method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("LocalAuthenticationService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
