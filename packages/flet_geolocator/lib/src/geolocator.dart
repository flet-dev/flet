import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

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
    debugPrint("Geolocator.initState($hashCode)");
    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
    super.initState();
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
    LocationAccuracy locationAccuracy = LocationAccuracy.best;

    String locationAccuracyString =
        widget.control.attrString("locationAccuracy", 'best')!;
    switch (locationAccuracyString) {
      case "best":
        locationAccuracy = LocationAccuracy.best;
      case "bestForNavigation":
        locationAccuracy = LocationAccuracy.bestForNavigation;
      case "high":
        locationAccuracy = LocationAccuracy.high;
      case "medium":
        locationAccuracy = LocationAccuracy.medium;
      case "low":
        locationAccuracy = LocationAccuracy.low;
      case "lowest":
        locationAccuracy = LocationAccuracy.lowest;
      case "reduced":
        locationAccuracy = LocationAccuracy.reduced;
    }

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "getLocation":
            Future<bool> locationHandler =
                Permission.location.request().isGranted;
            return locationHandler.then((value) async {

              if (value == true) {
                Position location = await Geolocator.getCurrentPosition(
                    desiredAccuracy: locationAccuracy);

                return 'latitude.${location.latitude},longitude.${location.longitude},altitude.${location.altitude},speed.${location.speed},timestamp.${location.timestamp}';
              } else {

                return 'latitude null,longitude null,altitude null,speed null,timestamp null';
              }
            });
        }
        return null;
      });
    }();

    return const SizedBox.shrink();
  }
}
