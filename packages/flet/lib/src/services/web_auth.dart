import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';

import '../flet_service.dart';

/// Opens a sign-in URL and returns the redirect callback URL (no OAuth logic).
class WebAuthService extends FletService {
  static const _channel = MethodChannel('dev.flet/web_auth');

  WebAuthService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("WebAuthService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("WebAuthService.$name($args)");
    switch (name) {
      case "authenticate":
        if (kIsWeb) {
          return {
            "error": "unsupported_platform",
            "error_description": "WebAuth is not available on web in this release.",
          };
        }
        try {
          final result = await _channel.invokeMethod<Map>("authenticate", {
            "url": args["url"],
            "redirect_url": args["redirect_url"],
            "callback_scheme": args["callback_scheme"],
            "ephemeral": args["ephemeral"] == true,
            "timeout": args["timeout"],
          });
          if (result == null) {
            return {
              "error": "authenticate_failed",
              "error_description": "Native WebAuth returned null.",
            };
          }
          return Map<String, dynamic>.from(result);
        } on PlatformException catch (e) {
          return {
            "error": e.code,
            "error_description": e.message ?? e.code,
          };
        }
      case "cancel":
        try {
          await _channel.invokeMethod("cancel");
        } catch (_) {}
        return null;
      default:
        throw Exception("Unknown WebAuth method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("WebAuthService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
