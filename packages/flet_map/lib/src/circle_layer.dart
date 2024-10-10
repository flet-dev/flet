import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class CircleLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;

  const CircleLayerControl(
      {super.key,
      required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleLayerControl build: ${control.id}");

    return withControls(control.childIds, (context, circlesView) {
      debugPrint("CircleLayerControlState build: ${control.id}");

      var circles = circlesView.controlViews
          .where((c) =>
              c.control.type == "map_circle_marker" && c.control.isVisible)
          .map((circle) {
        return CircleMarker(
            point: parseLatLng(circle.control, "coordinates")!,
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

      return CircleLayer(circles: circles);
    });
  }
}
