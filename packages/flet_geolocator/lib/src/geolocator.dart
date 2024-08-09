import 'dart:async';
import 'dart:convert';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:geolocator/geolocator.dart';

import 'utils/geolocator.dart';

class GeolocatorControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final FletControlBackend backend;

  const GeolocatorControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.backend});

  @override
  State<GeolocatorControl> createState() => _GeolocatorControlState();
}

class _GeolocatorControlState extends State<GeolocatorControl>
    with FletStoreMixin {
  StreamSubscription<Position>? _positionStream;

  @override
  void initState() {
    super.initState();
    debugPrint("Geolocator.initState($hashCode)");
    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
  }

  void _onRemove() {
    debugPrint("Geolocator.remove($hashCode)");
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("Geolocator.deactivate($hashCode)");
    super.deactivate();
  }

  void _onPosition(Position position) {
    debugPrint("Geolocator onPosition: $position");
    final jsonData = jsonEncode({
      "latitude": position.latitude,
      "longitude": position.longitude,
    });
    widget.backend.triggerControlEvent(widget.control.id, "position", jsonData);
  }

  Future<bool> _enableLocationService() async {
    late LocationSettings locationSettings;
    if (defaultTargetPlatform == TargetPlatform.android) {
      locationSettings = AndroidSettings(
          accuracy: LocationAccuracy.high,
          distanceFilter: 0,
          forceLocationManager: true,
          intervalDuration: const Duration(seconds: 30),
          // Needs this or when app goes in background, background service stops working
          foregroundNotificationConfig: const ForegroundNotificationConfig(
            notificationText:
            "Location Updates",
            notificationTitle: "Running in Background",
            enableWakeLock: true,
          )
      );
    } else if (defaultTargetPlatform == TargetPlatform.iOS || defaultTargetPlatform == TargetPlatform.macOS) {
      locationSettings = AppleSettings(
        accuracy: LocationAccuracy.bestForNavigation,
        activityType: ActivityType.automotiveNavigation,
        distanceFilter: 0,
        pauseLocationUpdatesAutomatically: false,
        showBackgroundLocationIndicator: true,
        allowBackgroundLocationUpdates: true,
      );
    }
    // Can enable this block once all Flet has flutter package web:^1.0.0
    // Honestly it is so close to else statement below, not a big issue
    // else if (kIsWeb) {
    //   locationSettings = WebSettings(
    //     accuracy: LocationAccuracy.high,
    //     distanceFilter: 0,
    //     // maximumAge: Duration(minutes: 5)
    //     maximumAge: Duration.zero,
    //   );
    // }
    else {
      locationSettings = LocationSettings(
        accuracy: LocationAccuracy.high,
        distanceFilter: 0,
      );
    }

    _positionStream = Geolocator.getPositionStream(locationSettings: locationSettings,
    ).listen(
      (Position? position) {
        if (position != null) {
          _onPosition(position);
          debugPrint('Geolocator: ${position.latitude}, ${position.longitude}, ${position}');
        } else {
          debugPrint('Geolocator: Position is null.');
        }
      },
      onError: (e) {
        debugPrint('Geolocator: Error getting stream position: $e');
      },
    );
    return true;
  }

  Future<bool> _disableLocationService() async {
    await _positionStream?.cancel();
    return true;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Geolocator build: ${widget.control.id} (${widget.control.hashCode})");
    bool onPosition = widget.control.attrBool("onPosition", false)!;

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "request_permission":
            var permission = await Geolocator.requestPermission();
            return permission.name;
          case "get_permission_status":
            var permission = await Geolocator.checkPermission();
            return permission.name;
          case "is_location_service_enabled":
            var serviceEnabled = await Geolocator.isLocationServiceEnabled();
            return serviceEnabled.toString();
          case "service_enable":
            var serviceEnabled = false;
            if (onPosition) {
              serviceEnabled = await _enableLocationService();
            }
            return serviceEnabled.toString();
          case "service_disable":
            var serviceDisabled = await _disableLocationService();
            return serviceDisabled.toString();
          case "open_app_settings":
            if (!kIsWeb) {
              var opened = await Geolocator.openAppSettings();
              return opened.toString();
            }
            break;
          case "open_location_settings":
            if (!kIsWeb) {
              var opened = await Geolocator.openLocationSettings();
              return opened.toString();
            }
            break;
          case "get_last_known_position":
            if (!kIsWeb) {
              Position? position = await Geolocator.getLastKnownPosition();
              return positionToJson(position);
            }
            break;
          case "get_current_position":
            Position currentPosition = await Geolocator.getCurrentPosition(
              desiredAccuracy: parseLocationAccuracy(
                  args["accuracy"], LocationAccuracy.best)!,
            );
            return positionToJson(currentPosition)!;
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
