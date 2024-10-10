import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class PolylineLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;
  final List<Control> children;

  const PolylineLayerControl(
      {super.key,
      required this.parent,
      required this.control,
      required this.children});

  @override
  Widget build(BuildContext context) {
    debugPrint("PolylineLayerControl build: ${control.id}");

    return withControls(control.childIds, (context, polylinesView) {
      debugPrint("PolylineLayerControlState build: ${control.id}");

      var polylines = polylinesView.controlViews
          .where((c) =>
              c.control.type == "map_polyline_marker" && c.control.isVisible)
          .map<Polyline>((polyline) {
        var coordinates = polyline.control.attrString("coordinates");
        var colorsStop = polyline.control.attrString("colorsStop");
        var gradientColors = polyline.control.attrString("gradientColors");
        return Polyline(
            borderStrokeWidth:
                polyline.control.attrDouble("borderStrokeWidth", 0)!,
            borderColor: polyline.control
                .attrColor("borderColor", context, const Color(0xFFFFFF00))!,
            color: polyline.control
                .attrColor("color", context, const Color(0xFF00FF00))!,
            pattern: parseStrokePattern(polyline.control, "strokePattern") ??
                const StrokePattern.solid(),
            strokeCap: parseStrokeCap(
                polyline.control.attrString("strokeCap"), StrokeCap.round)!,
            strokeJoin: parseStrokeJoin(
                polyline.control.attrString("strokeJoin"), StrokeJoin.round)!,
            strokeWidth: polyline.control.attrDouble("strokeWidth", 1.0)!,
            useStrokeWidthInMeter:
                polyline.control.attrBool("useStrokeWidthInMeter", false)!,
            colorsStop: colorsStop != null
                ? (jsonDecode(colorsStop) as List)
                    .map((e) => parseDouble(e))
                    .whereNotNull()
                    .toList()
                : null,
            gradientColors: gradientColors != null
                ? (jsonDecode(gradientColors) as List)
                    .map((e) => parseColor(Theme.of(context), e))
                    .whereNotNull()
                    .toList()
                : null,
            points: coordinates != null
                ? (jsonDecode(coordinates) as List)
                    .map((e) => latLngFromJson(e))
                    .whereNotNull()
                    .toList()
                : []);
      }).toList();

      return PolylineLayer(
        polylines: polylines,
        cullingMargin: control.attrDouble("cullingMargin", 10)!,
        minimumHitbox: control.attrDouble("minHittableRadius", 10)!,
        simplificationTolerance:
            control.attrDouble("simplificationTolerance", 0.4)!,
      );
    });
  }
}
