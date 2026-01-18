import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:screen_brightness/screen_brightness.dart';

import '../flet_service.dart';
import '../utils/numbers.dart';
import '../utils/platform.dart';

class ScreenBrightnessService extends FletService {
  final ScreenBrightness _screenBrightness = ScreenBrightness();
  StreamSubscription<double>? _systemSubscription;
  StreamSubscription<double>? _applicationSubscription;

  ScreenBrightnessService({required super.control});

  @override
  void init() {
    super.init();
    debugPrint("ScreenBrightnessService(${control.id}).init");
    control.addInvokeMethodListener(_invokeMethod);
    _updateListeners();
  }

  @override
  void update() {
    _updateListeners();
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    if (isWebPlatform()) {
      return null;
    }

    switch (name) {
      case "get_system_screen_brightness":
        return _screenBrightness.system;
      case "can_change_system_screen_brightness":
        return _screenBrightness.canChangeSystemBrightness;
      case "set_system_screen_brightness":
        final brightness = parseDouble(args["value"]);
        if (brightness == null) {
          throw ArgumentError.notNull("value");
        }
        return _screenBrightness.setSystemScreenBrightness(brightness);
      case "get_application_screen_brightness":
        return _screenBrightness.application;
      case "set_application_screen_brightness":
        final brightness = parseDouble(args["value"]);
        if (brightness == null) {
          throw ArgumentError.notNull("value");
        }
        return _screenBrightness.setApplicationScreenBrightness(brightness);
      case "reset_application_screen_brightness":
        return _screenBrightness.resetApplicationScreenBrightness();
      case "is_animate":
        return _screenBrightness.isAnimate;
      case "set_animate":
        final isAnimate = parseBool(args["value"]);
        if (isAnimate == null) {
          throw ArgumentError.notNull("value");
        }
        return _screenBrightness.setAnimate(isAnimate);
      case "is_auto_reset":
        return _screenBrightness.isAutoReset;
      case "set_auto_reset":
        final isAutoReset = parseBool(args["value"]);
        if (isAutoReset == null) {
          throw ArgumentError.notNull("value");
        }
        return _screenBrightness.setAutoReset(isAutoReset);
      default:
        throw Exception("Unknown ScreenBrightness method: $name");
    }
  }

  void _updateListeners() {
    if (isWebPlatform()) {
      _disposeSubscriptions();
      return;
    }

    final listenSystem =
        control.getBool("on_system_screen_brightness_change") == true;
    final listenApplication =
        control.getBool("on_application_screen_brightness_change") == true;

    if (listenSystem && _systemSubscription == null) {
      _systemSubscription = _screenBrightness.onSystemScreenBrightnessChanged
          .listen((value) {
        control.triggerEvent(
            "system_screen_brightness_change", {"brightness": value});
      }, onError: (error) {
        debugPrint(
            "ScreenBrightnessService: error listening for system changes: $error");
      });
    } else if (!listenSystem && _systemSubscription != null) {
      _systemSubscription?.cancel();
      _systemSubscription = null;
    }

    if (listenApplication && _applicationSubscription == null) {
      _applicationSubscription =
          _screenBrightness.onApplicationScreenBrightnessChanged.listen(
        (value) {
          control.triggerEvent(
              "application_screen_brightness_change", {"brightness": value});
        },
        onError: (error) {
          debugPrint(
              "ScreenBrightnessService: error listening for application changes: $error");
        },
      );
    } else if (!listenApplication && _applicationSubscription != null) {
      _applicationSubscription?.cancel();
      _applicationSubscription = null;
    }
  }

  void _disposeSubscriptions() {
    _systemSubscription?.cancel();
    _systemSubscription = null;
    _applicationSubscription?.cancel();
    _applicationSubscription = null;
  }

  @override
  void dispose() {
    debugPrint("ScreenBrightnessService(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _disposeSubscriptions();
    super.dispose();
  }
}
