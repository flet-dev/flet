import 'dart:async';
import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
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
  StreamSubscription<Position>? _onPositionChangedSubscription;

  @override
  void initState() {
    super.initState();
    debugPrint("Geolocator.initState($hashCode)");
    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (widget.control.attrBool("onPositionChange", false)!) {
      _onPositionChangedSubscription = Geolocator.getPositionStream(
        locationSettings: parseLocationSettings(
            widget.control, "locationSettings", Theme.of(context)),
      ).listen(
        (Position? newPosition) {
          if (newPosition != null) {
            _onPositionChange(newPosition);
            debugPrint('Geolocator - $newPosition');
          } else {
            debugPrint('Geolocator: Position is null.');
          }
        },
        onError: (Object error, StackTrace stackTrace) {
          debugPrint('Geolocator Error getting stream position: $error');
          widget.backend.triggerControlEvent(
              widget.control.id, "error", error.toString());
        },
        onDone: () {
          debugPrint('Geolocator: Done getting stream position.');
        },
      );
    }
  }

  void _onRemove() {
    debugPrint("Geolocator.remove($hashCode)");
    _onPositionChangedSubscription?.cancel();
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("Geolocator.deactivate($hashCode)");
    _onPositionChangedSubscription?.cancel();
    super.deactivate();
  }

  void _onPositionChange(Position position) {
    debugPrint("Geolocator onPosition: $position");
    final jsonData = jsonEncode({
      "lat": position.latitude,
      "long": position.longitude,
    });
    widget.backend
        .triggerControlEvent(widget.control.id, "positionChange", jsonData);
  }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Geolocator build: ${widget.control.id} (${widget.control.hashCode})");

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
              locationSettings: locationSettingsFromJson(
                  args["location_settings"] != null
                      ? jsonDecode(args["location_settings"]!)
                      : null,
                  Theme.of(context)),
            );
            return positionToJson(currentPosition)!;
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
