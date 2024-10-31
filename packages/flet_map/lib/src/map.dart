import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:flutter_map_animations/flutter_map_animations.dart';
import 'package:latlong2/latlong.dart';

import 'utils/map.dart';

class MapControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const MapControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<MapControl> createState() => _MapControlState();
}

class _MapControlState extends State<MapControl>
    with FletStoreMixin, TickerProviderStateMixin {
  late final _animatedMapController = AnimatedMapController(vsync: this);

  @override
  void dispose() {
    _animatedMapController.dispose();
    super.dispose();
  }

  Duration? durationFromString(String? duration, [Duration? defaultValue]) {
    return duration != null
        ? durationFromJSON(json.decode(duration), defaultValue)
        : defaultValue;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("Map build: ${widget.control.id} (${widget.control.hashCode})");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;
    List<String> acceptedChildrenTypes = [
      "map_circle_layer",
      "map_tile_layer",
      "map_polygon_layer",
      "map_polyline_layer",
      "map_marker_layer",
      "map_rich_attribution",
      "map_simple_attribution"
    ];
    var ctrls = widget.children
        .where((c) => c.isVisible && (acceptedChildrenTypes.contains(c.type)))
        .toList();

    Curve? defaultAnimationCurve;
    Duration? defaultAnimationDuration;
    var configuration = parseConfiguration(widget.control, "configuration",
        widget.backend, Theme.of(context), const MapOptions())!;

    Widget map = FlutterMap(
      mapController: _animatedMapController.mapController,
      options: configuration,
      children: ctrls
          .map((c) => createControl(widget.control, c.id, disabled))
          .toList(),
    );

    () async {
      widget.backend.subscribeMethods(widget.control.id,
          (methodName, args) async {
        switch (methodName) {
          case "rotate_from":
            var degree = parseDouble(args["degree"]);
            if (degree != null) {
              _animatedMapController.animatedRotateFrom(
                degree,
                curve: parseCurve(args["curve"]) ?? defaultAnimationCurve,
              );
            }
          case "reset_rotation":
            _animatedMapController.animatedRotateReset(
                curve: parseCurve(args["curve"], defaultAnimationCurve),
                duration: durationFromString(
                    args["duration"], defaultAnimationDuration));
          case "zoom_in":
            _animatedMapController.animatedZoomIn(
                curve: parseCurve(args["curve"], defaultAnimationCurve),
                duration: durationFromString(
                    args["duration"], defaultAnimationDuration));
          case "zoom_out":
            _animatedMapController.animatedZoomOut(
                curve: parseCurve(args["curve"], defaultAnimationCurve),
                duration: durationFromString(
                    args["duration"], defaultAnimationDuration));
          case "zoom_to":
            var zoom = parseDouble(args["zoom"]);
            if (zoom != null) {
              _animatedMapController.animatedZoomTo(zoom,
                  curve: parseCurve(args["curve"], defaultAnimationCurve),
                  duration: durationFromString(
                      args["duration"], defaultAnimationDuration));
            }
          case "move_to":
            var zoom = parseDouble(args["zoom"]);
            var lat = parseDouble(args["lat"]);
            var long = parseDouble(args["long"]);
            var ox = parseDouble(args["ox"]);
            var oy = parseDouble(args["oy"]);
            _animatedMapController.animateTo(
              zoom: zoom,
              curve: parseCurve(args["curve"], defaultAnimationCurve),
              rotation: parseDouble(args["rot"]),
              duration: durationFromString(
                  args["duration"], defaultAnimationDuration),
              dest: (lat != null && long != null) ? LatLng(lat, long) : null,
              offset: (ox != null && oy != null) ? Offset(ox, oy) : Offset.zero,
            );
          case "center_on":
            var zoom = parseDouble(args["zoom"]);
            var lat = parseDouble(args["lat"]);
            var long = parseDouble(args["long"]);
            if (lat != null && long != null) {
              _animatedMapController.centerOnPoint(
                LatLng(lat, long),
                zoom: zoom,
                curve: parseCurve(args["curve"], defaultAnimationCurve),
                duration: durationFromString(
                    args["duration"], defaultAnimationDuration),
              );
            }
        }
        return null;
      });
    }();

    return constrainedControl(context, map, widget.parent, widget.control);
  }
}
