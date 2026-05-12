import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';

import 'utils/geolocator.dart';

class GeolocatorService extends FletService {
  GeolocatorService({required super.control});

  StreamSubscription<Position>? _onPositionChangedSubscription;

  @override
  void init() {
    super.init();
    debugPrint("Geolocator(${control.id}).init: ${control.properties}");
    control.addInvokeMethodListener(_invokeMethod);
    registerEvents();
  }

  @override
  void update() {
    debugPrint("Geolocator(${control.id}).update: ${control.properties}");
    registerEvents();
  }

  void registerEvents() {
    _onPositionChangedSubscription?.cancel();
    _onPositionChangedSubscription = null;

    if (!control.hasEventHandler("position_change") &&
        !control.hasEventHandler("error")) {
      return;
    }

    _onPositionChangedSubscription = Geolocator.getPositionStream(
      locationSettings: parseLocationSettings(control.get("configuration")),
    ).listen(
      (Position? position) {
        if (position != null) {
          control.updateProperties({"position": position.toMap()});
          control
              .triggerEvent("position_change", {"position": position.toMap()});
        }
      },
      onError: (Object error, StackTrace stackTrace) {
        control.triggerEvent("error", _describeLocationError(error));
      },
    );
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Geolocator.$name($args)");
    try {
      switch (name) {
        case "request_permission":
          var permission = await Geolocator.requestPermission();
          return permission.name;
        case "get_permission_status":
          var permission = await Geolocator.checkPermission();
          return permission.name;
        case "is_location_service_enabled":
          var serviceEnabled = await Geolocator.isLocationServiceEnabled();
          return serviceEnabled;
        case "open_app_settings":
          if (!kIsWeb) {
            return await Geolocator.openAppSettings();
          }
          return false;
        case "open_location_settings":
          if (!kIsWeb) {
            return await Geolocator.openLocationSettings();
          }
          return false;
        case "get_last_known_position":
          if (!kIsWeb) {
            return (await Geolocator.getLastKnownPosition())?.toMap();
          }
          return null;
        case "get_current_position":
          {
            final settings = parseLocationSettings(args["configuration"],
                forSingleShot: true);
            // Workaround for geolocator_web 4.1.3: it passes
            // `timeout?.inMicroseconds` to the browser API instead of
            // `inMilliseconds`, so the configured timeLimit is effectively
            // ignored. Enforce it on the Dart side here.
            final positionFuture =
                Geolocator.getCurrentPosition(locationSettings: settings);
            final timeLimit = settings?.timeLimit;
            final currentPosition = kIsWeb && timeLimit != null
                ? await positionFuture.timeout(timeLimit,
                    onTimeout: () => throw TimeoutException(
                        "Browser did not return a position within "
                        "${timeLimit.inSeconds}s.",
                        timeLimit))
                : await positionFuture;
            return currentPosition.toMap();
          }
        case "distance_between":
          var p = [
            args["start_latitude"],
            args["start_longitude"],
            args["end_latitude"],
            args["end_longitude"]
          ];
          if (p.every((e) => e != null)) {
            return Geolocator.distanceBetween(p[0], p[1], p[2], p[3]);
          }
          return null;
        default:
          throw Exception("Unknown Geolocator method: $name");
      }
    } catch (error) {
      throw _GeolocatorException(_describeLocationError(error));
    }
  }

  String _describeLocationError(Object error) {
    if (error is LocationServiceDisabledException) {
      return "Location services are disabled. "
          "Enable them in the device or system settings.";
    }
    if (error is PermissionDeniedException) {
      return "Location permission denied: ${error.message ?? 'no message'}.";
    }
    if (error is PermissionDefinitionsNotFoundException) {
      return "Location permissions are not declared in the platform manifest "
          "(Info.plist / AndroidManifest.xml): ${error.message ?? ''}";
    }
    if (error is PermissionRequestInProgressException) {
      return "A location permission request is already in progress.";
    }
    if (error is PositionUpdateException) {
      return "Failed to obtain position: ${error.message ?? ''}";
    }
    if (error is TimeoutException) {
      return "Location request timed out.";
    }
    return error.toString();
  }

  @override
  void dispose() {
    debugPrint("Geolocator(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _onPositionChangedSubscription?.cancel();
    super.dispose();
  }
}

class _GeolocatorException implements Exception {
  final String message;
  const _GeolocatorException(this.message);

  @override
  String toString() => message;
}
