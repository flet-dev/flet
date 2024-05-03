import 'dart:async';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
// import 'package:flet_geolocator/flet_geolocator.dart';
import 'package:geolocator/geolocator.dart';
import 'package:permission_handler/permission_handler.dart';

// import 'utils/geolocator.dart';

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
  // Geolocator? recorder;
  // void Function(RecordState)? _onStateChanged;
  // StreamSubscription? _onStateChangedSubscription;

  @override
  void initState() {
    debugPrint("Geolocator.initState($hashCode)");
    // recorder = widget.control.state["recorder"];
    // if (recorder == null) {
    //   recorder = Geolocator();
    //   recorder = widget.control.state["recorder"] = recorder;
    // }
    //
    // _onStateChangedSubscription = recorder?.onStateChanged().listen((state) {
    //   _onStateChanged?.call(state);
    // });

    widget.control.onRemove.clear();
    widget.control.onRemove.add(_onRemove);
    super.initState();
  }

  void _onRemove() {
    debugPrint("Geolocator.remove($hashCode)");
    // widget.control.state["recorder"]?.dispose();
    widget.backend.unsubscribeMethods(widget.control.id);
  }

  @override
  void deactivate() {
    debugPrint("Geolocator.deactivate($hashCode)");
    // _onStateChangedSubscription?.cancel();
    super.deactivate();
  }

  // Future<String?> stopRecording() async {
  //   debugPrint("Geolocator.stopRecording($hashCode)");
  //   final path = await recorder!.stop();
  //   return path;
  // }

  @override
  Widget build(BuildContext context) {
    debugPrint(
        "Geolocator build: ${widget.control.id} (${widget.control.hashCode})");
    LocationAccuracy locationAccuracy = LocationAccuracy.best;
    // Geolocator geoLocator = Geolocator();
    // int bitRate = widget.control.attrInt("bitRate", 128000)!;
    // int sampleRate = widget.control.attrInt("sampleRate", 44100)!;
    // int numChannels = widget.control.attrInt("channels", 2)!;
    // bool autoGain = widget.control.attrBool("autoGain", false)!;
    // bool cancelEcho = widget.control.attrBool("cancelEcho", false)!;
    // bool suppressNoise = widget.control.attrBool("suppressNoise", false)!;
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
          case "test":
            debugPrint('Print from Test Case');
            return 'GEOLOCATOR TEST';
          case "getLocation":
            Future<bool> locationHandler =
                Permission.location.request().isGranted;
            return locationHandler.then((value) async {
              debugPrint('HERE');
              if (value == true) {
                Position location = await Geolocator.getCurrentPosition(
                    desiredAccuracy: locationAccuracy);
                debugPrint('TRUE');
                return 'latitude.${location.latitude},longitude.${location.longitude},altitude.${location.altitude},speed.${location.speed},timestamp.${location.timestamp}';
              } else {
                debugPrint('FALSE');
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
