import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class CircleLayerControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const CircleLayerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("CircleLayerControl build: ${control.id}");

    var circles = control
        .children("circles")
        .where((c) => c.type == "CircleMarker")
        .map((circle) {
      return CircleMarker(
          point: parseLatLng(circle.get("coordinates"))!,
          color: circle.getColor("color", context, const Color(0xFF00FF00))!,
          borderColor: circle.getColor(
              "border_color", context, const Color(0xFFFFFF00))!,
          borderStrokeWidth: circle.getDouble("border_stroke_width", 0.0)!,
          useRadiusInMeter: circle.getBool("use_radius_in_meter", false)!,
          radius: circle.getDouble("radius", 10)!);
    }).toList();

    return CircleLayer(circles: circles);
  }
}
