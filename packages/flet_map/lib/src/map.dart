import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/widgets.dart';
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

    void triggerEvent(Control ctrl, String eventName, dynamic eventData) {
      var d = "";
      if (eventData is String) {
        d = eventData;
      } else if (eventData is Map) {
        d = json.encode(eventData);
      }

      widget.backend.triggerControlEvent(ctrl.id, eventName, d);
    }

    Curve? defaultAnimationCurve;
    Duration? defaultAnimationDuration;
    var onTap = widget.control.attrBool("onTap", false)!;
    var onLongPress = widget.control.attrBool("onLongPress", false)!;
    var onSecondaryTap = widget.control.attrBool("onSecondaryTap", false)!;
    var onMapEvent = widget.control.attrBool("onEvent", false)!;
    var onInit = widget.control.attrBool("onInit", false)!;
    var onPointerDown = widget.control.attrBool("onPointerDown", false)!;
    var onPointerHover = widget.control.attrBool("onHover", false)!;
    var onPointerCancel = widget.control.attrBool("onPointerCancel", false)!;
    var onPointerUp = widget.control.attrBool("onPointerUp", false)!;
    var onPositionChange = widget.control.attrBool("onPositionChange", false)!;

    return withControls(widget.control.childIds, (context, configurationsView) {
      var configuration = configurationsView.controlViews
          .where((c) => c.control.type == "map_configuration")
          .map((config) {
        defaultAnimationCurve =
            parseCurve(config.control.attrString("animationCurve"));
        defaultAnimationDuration =
            parseDuration(config.control, "animationDuration");
        return MapOptions(
          initialCenter: parseLatLng(
              config.control, "initialCenter", const LatLng(50.5, 30.51))!,
          interactionOptions: parseInteractionOptions(config.control,
              "interactionConfiguration", const InteractionOptions())!,
          backgroundColor: config.control
              .attrColor("backgroundColor", context, const Color(0x00000000))!,
          initialRotation: config.control.attrDouble("initialRotation", 0.0)!,
          initialZoom: config.control.attrDouble("initialZoom", 13.0)!,
          keepAlive: config.control.attrBool("keepAlive", false)!,
          maxZoom: config.control.attrDouble("maxZoom"),
          minZoom: config.control.attrDouble("minZoom"),
          onPointerHover: onPointerHover
              ? (PointerHoverEvent e, LatLng latlng) {
                  triggerEvent(widget.control, "hover", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": e.position.dx,
                    "gy": e.position.dy,
                    "lx": e.localPosition.dx,
                    "ly": e.localPosition.dy,
                    "kind": e.kind.name,
                  });
                }
              : null,
          onTap: onTap
              ? (TapPosition pos, LatLng latlng) {
                  triggerEvent(widget.control, "tap", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": pos.global.dx,
                    "gy": pos.global.dy,
                    "lx": pos.relative?.dx,
                    "ly": pos.relative?.dy,
                  });
                }
              : null,
          onLongPress: onLongPress
              ? (TapPosition pos, LatLng latlng) {
                  triggerEvent(widget.control, "long_press", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": pos.global.dx,
                    "gy": pos.global.dy,
                    "lx": pos.relative?.dx,
                    "ly": pos.relative?.dy,
                  });
                }
              : null,
          onPositionChanged: onPositionChange
              ? (MapCamera camera, bool hasGesture) {
                  triggerEvent(widget.control, "position_change", {
                    "lat": camera.center.latitude,
                    "long": camera.center.longitude,
                    "min_zoom": camera.minZoom,
                    "max_zoom": camera.maxZoom,
                    "rot": camera.rotation,
                  });
                }
              : null,
          onPointerDown: onPointerDown
              ? (PointerDownEvent e, LatLng latlng) {
                  triggerEvent(widget.control, "pointer_down", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": e.position.dx,
                    "gy": e.position.dy,
                    "kind": e.kind.name,
                  });
                }
              : null,
          onPointerCancel: onPointerCancel
              ? (PointerCancelEvent e, LatLng latlng) {
                  triggerEvent(widget.control, "pointer_cancel", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": e.position.dx,
                    "gy": e.position.dy,
                    "kind": e.kind.name,
                  });
                }
              : null,
          onPointerUp: onPointerUp
              ? (PointerUpEvent e, LatLng latlng) {
                  triggerEvent(widget.control, "pointer_up", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": e.position.dx,
                    "gy": e.position.dy,
                    "kind": e.kind.name,
                  });
                }
              : null,
          onSecondaryTap: onSecondaryTap
              ? (TapPosition pos, LatLng latlng) {
                  triggerEvent(widget.control, "secondary_tap", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                    "gx": pos.global.dx,
                    "gy": pos.global.dy,
                    "lx": pos.relative?.dx,
                    "ly": pos.relative?.dy,
                  });
                }
              : null,
          onMapEvent: onMapEvent
              ? (MapEvent e) {
                  triggerEvent(widget.control, "event", {
                    "src": e.source.name,
                    "c_lat": e.camera.center.latitude,
                    "c_long": e.camera.center.longitude,
                    "zoom": e.camera.zoom,
                    "min_zoom": e.camera.minZoom,
                    "max_zoom": e.camera.maxZoom,
                    "rot": e.camera.rotation,
                  });
                }
              : null,
          onMapReady: onInit
              ? () {
                  debugPrint("Map ${widget.control.id} init");
                  widget.backend.triggerControlEvent(widget.control.id, "init");
                }
              : null,
        );
      });

      Widget map = FlutterMap(
        mapController: _animatedMapController.mapController,
        options: configuration.first,
        children: ctrls
            .map((c) => createControl(widget.control, c.id, disabled))
            .toList(),
      );

      Duration? durationFromString(String? duration, [Duration? defaultValue]) {
        if (duration != null) {
          return durationFromJSON(json.decode(duration), defaultValue);
        }
        return null;
      }

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
                offset:
                    (ox != null && oy != null) ? Offset(ox, oy) : Offset.zero,
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
    });
  }
}
