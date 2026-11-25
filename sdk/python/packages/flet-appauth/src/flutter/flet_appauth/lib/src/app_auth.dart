import 'dart:io' show Platform;

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show kDebugMode, kIsWeb;
import 'package:flutter/services.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_appauth/flutter_appauth.dart';

class AppAuthService extends FletService {
  AppAuthService({required super.control});

  final FlutterAppAuth _appAuth = FlutterAppAuth();
  static const MethodChannel _androidChannel =
      MethodChannel('dev.flet/flet_appauth');

  @override
  void init() {
    super.init();
    if (kDebugMode) {
      debugPrint("AppAuthService(${control.id}).init");
    }
    control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    if (kDebugMode) {
      debugPrint("AppAuthService.$name");
    }
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
    // Android: Chrome Auth Tab (custom-scheme redirect via callback).
    // iOS: flutter_appauth / ASWebAuthenticationSession.
    if (!kIsWeb && Platform.isAndroid) {
      return await _authorizeAndroidAuthTab(args);
    }
    return await _authorizeFlutterAppAuth(args);
  }

  Future<Map<String, dynamic>> _authorizeAndroidAuthTab(Map args) async {
    try {
      final raw = await _androidChannel.invokeMethod<dynamic>("authorize", {
        "client_id": args["client_id"],
        "redirect_url": args["redirect_url"],
        "authorization_endpoint": args["authorization_endpoint"],
        "token_endpoint": args["token_endpoint"],
        "scopes": args["scopes"] ?? [],
        "additional_parameters": args["additional_parameters"] ?? {},
        "prefer_ephemeral_session": args["prefer_ephemeral_session"] == true,
      });
      if (raw is Map) {
        return Map<String, dynamic>.from(raw);
      }
      return {
        "error": "invalid_response",
        "error_description":
            "Unexpected Android AppAuth result type: ${raw.runtimeType}",
      };
    } on PlatformException catch (e) {
      return {
        "error": e.code,
        "error_description": e.message,
      };
    }
  }

  Future<Map<String, dynamic>> _authorizeFlutterAppAuth(Map args) async {
    final clientId = args["client_id"] as String;
    final redirectUrl = args["redirect_url"] as String;
    final authorizationEndpoint = args["authorization_endpoint"] as String;
    final tokenEndpoint = args["token_endpoint"] as String;
    final scopes = (args["scopes"] as List?)?.map((e) => e.toString()).toList();
    final additionalParameters = Map<String, String>.from(
      (args["additional_parameters"] as Map?)?.map(
            (key, value) => MapEntry(key.toString(), value.toString()),
          ) ??
          {},
    );
    // prompt / login_hint are dedicated AuthorizationRequest fields on iOS.
    // max_age is not built-in — keep it in additionalParameters.
    final prompt = additionalParameters.remove("prompt");
    final loginHint = additionalParameters.remove("login_hint");
    final preferEphemeralSession =
        args["prefer_ephemeral_session"] == true;

    // Post-logout reauth: force interactive login when ephemeral was requested.
    final promptValues = () {
      if (prompt != null && prompt.isNotEmpty) {
        return prompt.split(RegExp(r'\s+'));
      }
      if (preferEphemeralSession) {
        return <String>['login'];
      }
      return null;
    }();

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
          loginHint: loginHint == null || loginHint.isEmpty ? null : loginHint,
          promptValues: promptValues,
          additionalParameters:
              additionalParameters.isEmpty ? null : additionalParameters,
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
    if (kDebugMode) {
      debugPrint("AppAuthService(${control.id}).dispose");
    }
    control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }
}
