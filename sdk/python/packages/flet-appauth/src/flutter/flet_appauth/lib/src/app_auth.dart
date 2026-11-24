import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_appauth/flutter_appauth.dart';

class AppAuthService extends FletService {
  AppAuthService({required super.control});

  final FlutterAppAuth _appAuth = FlutterAppAuth();

  @override
  void init() {
    super.init();
    debugPrint("AppAuthService(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("AppAuthService.$name($args)");
    if (!isMobilePlatform()) {
      throw Exception("AppAuth is supported on Android and iOS only.");
    }
    switch (name) {
      case "authorize":
        return await _authorize(args as Map);
      default:
        throw Exception("Unknown AppAuth method: $name");
    }
  }

  Future<Map<String, dynamic>> _authorize(Map args) async {
    final clientId = args["client_id"] as String;
    final redirectUrl = args["redirect_url"] as String;
    final authorizationEndpoint = args["authorization_endpoint"] as String;
    final tokenEndpoint = args["token_endpoint"] as String;
    final scopes = (args["scopes"] as List?)?.map((e) => e.toString()).toList();
    final additionalParameters = (args["additional_parameters"] as Map?)?.map(
      (key, value) => MapEntry(key.toString(), value.toString()),
    );
    final preferEphemeralSession =
        args["prefer_ephemeral_session"] == true;

    try {
      final result = await _appAuth.authorize(
        AuthorizationRequest(
          clientId,
          redirectUrl,
          serviceConfiguration: AuthorizationServiceConfiguration(
            authorizationEndpoint: authorizationEndpoint,
            tokenEndpoint: tokenEndpoint,
          ),
          scopes: scopes,
          additionalParameters: additionalParameters,
          externalUserAgent: preferEphemeralSession
              ? ExternalUserAgent.ephemeralAsWebAuthenticationSession
              : ExternalUserAgent.asWebAuthenticationSession,
        ),
      );

      final code = result.authorizationCode;
      if (code == null || code.isEmpty) {
        return {
          "error": "missing_authorization_code",
          "error_description":
              "AppAuth returned no authorization code.",
          "code_verifier": result.codeVerifier,
        };
      }
      return {
        "authorization_code": code,
        "code_verifier": result.codeVerifier,
      };
    } on FlutterAppAuthUserCancelledException catch (e) {
      return {
        "error": "cancelled",
        "error_description": e.message ?? "User cancelled authorization.",
      };
    } on FlutterAppAuthPlatformException catch (e) {
      return {
        "error": e.code,
        "error_description": e.message,
      };
    }
  }

  @override
  void dispose() {
    debugPrint("AppAuthService(${control.id}).dispose");
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
