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
          case "has_permission":
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
            return "false";
          case "open_location_settings":
            if (!kIsWeb) {
              var opened = await Geolocator.openLocationSettings();
              return opened.toString();
            }
            return "false";
          case "get_last_known_position":
            if (!kIsWeb) {
              Position? position = await Geolocator.getLastKnownPosition();
              return positionToJson(position);
            }
            return null;
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
