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
    _onPositionChangedSubscription = Geolocator.getPositionStream(
      locationSettings: parseLocationSettings(
        control.get("configuration"),
        // Theme.of(context),
      ),
    ).listen(
      (Position? position) {
        if (position != null) {
          control.updateProperties({"position": position.toMap()});
          control
              .triggerEvent("position_change", {"position": position.toMap()});
        }
      },
      onError: (Object error, StackTrace stackTrace) {
        control.triggerEvent("error", error.toString());
      },
      onDone: () {
        // done
      },
    );
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Geolocator.$name($args)");
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
        break;
      case "open_location_settings":
        if (!kIsWeb) {
          return await Geolocator.openLocationSettings();
        }
        break;
      case "get_last_known_position":
        if (!kIsWeb) {
          return (await Geolocator.getLastKnownPosition())?.toMap();
        }
        break;
      case "get_current_position":
        try {
          Position currentPosition = await Geolocator.getCurrentPosition(
            locationSettings: parseLocationSettings(args["settings"]),
          );
          return currentPosition.toMap();
        } catch (error) {
          control.triggerEvent("error", error.toString());
          break;
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
        break;
      default:
        throw Exception("Unknown Geolocator method: $name");
    }
  }

  @override
  void dispose() {
    debugPrint("Geolocator(${control.id}).dispose()");
    control.removeInvokeMethodListener(_invokeMethod);
    _onPositionChangedSubscription?.cancel();
    super.dispose();
  }
}
