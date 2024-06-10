import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';
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

class _MapControlState extends State<MapControl> with FletStoreMixin {
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

    return withControls(widget.control.childIds, (context, configurationsView) {
      var configuration = configurationsView.controlViews
          .where((c) => c.control.type == "map_configuration")
          .map((config) {
        var onTap = config.control.attrBool("onTap", false)!;
        var onLongPress = config.control.attrBool("onLongPress", false)!;
        var onSecondaryTap = config.control.attrBool("onSecondaryTap", false)!;
        var onMapEvent = config.control.attrBool("onEvent", false)!;
        var onInit = config.control.attrBool("onInit", false)!;
        var onPointerDown = config.control.attrBool("onPointerDown", false)!;
        var onPointerCancel =
            config.control.attrBool("onPointerCancel", false)!;
        var onPointerUp = config.control.attrBool("onPointerUp", false)!;
        var onPositionChange =
            config.control.attrBool("onPositionChange", false)!;

        return MapOptions(
          initialCenter: parseLatLng(
              config.control, "initialCenter", const LatLng(50.5, 30.51))!,
          backgroundColor: config.control
              .attrColor("backgroundColor", context, const Color(0x00000000))!,
          initialRotation: config.control.attrDouble("initialRotation", 0.0)!,
          initialZoom: config.control.attrDouble("initialZoom", 13.0)!,
          keepAlive: config.control.attrBool("keepAlive", false)!,
          maxZoom: config.control.attrDouble("maxZoom"),
          minZoom: config.control.attrDouble("minZoom"),
          onTap: onTap
              ? (TapPosition pos, LatLng latlng) {
                  triggerEvent(config.control, "tap", {
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
                  triggerEvent(config.control, "long_press", {
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
                  triggerEvent(config.control, "position_change", {
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
                  triggerEvent(config.control, "pointer_down", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                  });
                }
              : null,
          onPointerCancel: onPointerCancel
              ? (PointerCancelEvent e, LatLng latlng) {
                  triggerEvent(config.control, "pointer_cancel", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                  });
                }
              : null,
          onPointerUp: onPointerUp
              ? (PointerUpEvent e, LatLng latlng) {
                  triggerEvent(config.control, "pointer_up", {
                    "lat": latlng.latitude,
                    "long": latlng.longitude,
                  });
                }
              : null,
          onSecondaryTap: onSecondaryTap
              ? (TapPosition pos, LatLng latlng) {
                  triggerEvent(config.control, "secondary_tap", {
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
                  triggerEvent(config.control, "event", {
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
                  widget.backend.triggerControlEvent(config.control.id, "init");
                }
              : null,
        );
      });

      Widget map = FlutterMap(
        options: configuration.first,
        children: ctrls
            .map((c) => createControl(widget.control, c.id, disabled))
            .toList(),
      );

      return constrainedControl(context, map, widget.parent, widget.control);
    });
  }
}
