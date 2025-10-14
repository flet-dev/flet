import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_animations/flutter_map_animations.dart';

import 'utils/map.dart';

class MapControl extends StatefulWidget {
  final Control control;

  const MapControl({super.key, required this.control});

  @override
  State<MapControl> createState() => _MapControlState();
}

class _MapControlState extends State<MapControl>
    with FletStoreMixin, TickerProviderStateMixin {
  late final _animatedMapController = AnimatedMapController(vsync: this);

  @override
  void initState() {
    super.initState();
    widget.control.addInvokeMethodListener(_invokeMethod);
  }

  Future<dynamic> _invokeMethod(String name, dynamic args) async {
    debugPrint("Map.$name($args)");
    var defaultAnimationCurve =
        widget.control.getCurve("animation_curve", Curves.fastOutSlowIn);
    var defaultAnimationDuration = widget.control
        .getDuration("animation_duration", const Duration(milliseconds: 500))!;
    var animationCurve = parseCurve(args["curve"], defaultAnimationCurve);
    var animationDuration =
        parseDuration(args["duration"], defaultAnimationDuration);
    var cancelPreviousAnimations = parseBool(args["cancel_ongoing_animations"]);
    var zoom = parseDouble(args["zoom"]);
    switch (name) {
      case "rotate_from":
        var degree = parseDouble(args["degree"]);
        if (degree != null) {
          await _animatedMapController.animatedRotateFrom(
            degree,
            curve: animationCurve,
            duration: animationDuration,
            cancelPreviousAnimations: cancelPreviousAnimations,
          );
        }
        break;
      case "reset_rotation":
        await _animatedMapController.animatedRotateReset(
          curve: animationCurve,
          duration: animationDuration,
          cancelPreviousAnimations: cancelPreviousAnimations,
        );
        break;
      case "zoom_in":
        await _animatedMapController.animatedZoomIn(
          curve: animationCurve,
          duration: animationDuration,
          cancelPreviousAnimations: cancelPreviousAnimations,
        );
        break;
      case "zoom_out":
        await _animatedMapController.animatedZoomOut(
          curve: animationCurve,
          duration: animationDuration,
          cancelPreviousAnimations: cancelPreviousAnimations,
        );
        break;
      case "zoom_to":
        if (zoom != null) {
          await _animatedMapController.animatedZoomTo(
            zoom,
            curve: animationCurve,
            duration: animationDuration,
            cancelPreviousAnimations: cancelPreviousAnimations,
          );
        }
        break;
      case "move_to":
        await _animatedMapController.animateTo(
          zoom: zoom,
          curve: animationCurve,
          rotation: parseDouble(args["rotation"]),
          duration: animationDuration,
          dest: parseLatLng(args["destination"]),
          offset: parseOffset(args["offset"], Offset.zero)!,
          cancelPreviousAnimations: cancelPreviousAnimations,
        );
        break;
      case "center_on":
        var point = parseLatLng(args["point"]);
        if (point != null) {
          await _animatedMapController.centerOnPoint(
            point,
            zoom: zoom,
            curve: animationCurve,
            duration: animationDuration,
            cancelPreviousAnimations: cancelPreviousAnimations,
          );
        }
        break;
      default:
        throw Exception("Unknown Map method: $name");
    }
  }

  @override
  void dispose() {
    _animatedMapController.dispose();
    widget.control.removeInvokeMethodListener(_invokeMethod);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Map build: ${widget.control.id} (${widget.control.hashCode})");

    Widget map = FlutterMap(
      mapController: _animatedMapController.mapController,
      options: parseConfiguration(widget.control, context, const MapOptions())!,
      children: widget.control.buildWidgets("layers"),
    );

    return ConstrainedControl(control: widget.control, child: map);
  }
}
