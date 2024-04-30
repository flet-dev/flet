import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class CircleLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const CircleLayerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleLayerControl build: ${control.id} (${control.hashCode})");

    return withControls(control.childIds, (context, circlesView) {
      debugPrint("CircleLayerControlState build: ${control.id}");

      var circles = circlesView.controlViews
          .where((c) => c.control.type == "mapcircle" && c.control.isVisible)
          .map((circle) {
        return CircleMarker(
            point: parseLatLng(circle.control, "location")!,
            color: circle.control
                .attrColor("color", context, const Color(0xFF00FF00))!,
            borderColor: circle.control
                .attrColor("borderColor", context, const Color(0xFFFFFF00))!,
            borderStrokeWidth:
                circle.control.attrDouble("borderStrokeWidth", 0.0)!,
            useRadiusInMeter:
                circle.control.attrBool("useRadiusInMeter", false)!,
            radius: circle.control.attrDouble("radius", 10)!);
      }).toList();

      Widget layer = CircleLayer(circles: circles);

      return constrainedControl(context, layer, parent, control);
    });
  }
}
