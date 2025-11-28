import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class PolylineLayerControl extends StatelessWidget with FletStoreMixin {
  final Control control;

  const PolylineLayerControl({super.key, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("PolylineLayerControl build: ${control.id}");

    var polylines = control
        .children("polylines")
        .where((c) => c.type == "PolylineMarker")
        .map((polyline) {
      return Polyline(
          borderStrokeWidth: polyline.getDouble("border_stroke_width", 0)!,
          borderColor:
              polyline.getColor("border_color", context, Colors.yellow)!,
          color: polyline.getColor("color", context, Colors.yellow)!,
          pattern: parseStrokePattern(
              polyline.get("stroke_pattern"), const StrokePattern.solid())!,
          strokeCap: polyline.getStrokeCap("stroke_cap", StrokeCap.round)!,
          strokeJoin: polyline.getStrokeJoin("stroke_join", StrokeJoin.round)!,
          strokeWidth: polyline.getDouble("stroke_width", 1.0)!,
          useStrokeWidthInMeter:
              polyline.getBool("use_stroke_width_in_meter", false)!,
          colorsStop: polyline
              .get("colors_stop", [])!
              .map((e) => parseDouble(e))
              .nonNulls
              .toList(),
          gradientColors: polyline
              .get("gradient_colors", [])!
              .map((e) => parseColor(e, Theme.of(context)))
              .nonNulls
              .toList(),
          points: polyline
              .get("coordinates", [])!
              .map((c) => parseLatLng(c))
              .nonNulls
              .toList());
    }).toList();

    return PolylineLayer(
      polylines: polylines,
      cullingMargin: control.getDouble("culling_margin", 10.0)!,
      minimumHitbox: control.getDouble("min_hittable_radius", 10.0)!,
      simplificationTolerance:
          control.getDouble("simplification_tolerance", 0.3)!,
    );
  }
}
