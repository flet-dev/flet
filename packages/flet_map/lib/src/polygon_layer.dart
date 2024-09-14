import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';

import 'utils/map.dart';

class PolygonLayerControl extends StatelessWidget with FletStoreMixin {
  final Control? parent;
  final Control control;

  const PolygonLayerControl(
      {super.key,
      required this.parent, required this.control});

  @override
  Widget build(BuildContext context) {
    debugPrint("PolygonLayerControl build: ${control.id}");

    return withControls(control.childIds, (context, polygonsView) {
      debugPrint("PolygonLayerControlState build: ${control.id}");

      var polygons = polygonsView.controlViews
          .where((c) =>
              c.control.type == "map_polygon_marker" && c.control.isVisible)
          .map((polygon) {
        var strokeCap = parseStrokeCap(
            polygon.control.attrString("strokeCap"), StrokeCap.round)!;
        var strokeJoin = parseStrokeJoin(
            polygon.control.attrString("strokeJoin"), StrokeJoin.round)!;
        var coordinates = polygon.control.attrString("coordinates");
        return Polygon(
            borderStrokeWidth:
                polygon.control.attrDouble("borderStrokeWidth", 0)!,
            borderColor: polygon.control.attrColor("borderColor", context) ??
                const Color(0xFFFFFF00),
            color: polygon.control.attrColor("color", context) ??
                const Color(0xFF00FF00),
            disableHolesBorder:
                polygon.control.attrBool("disableHolesBorder", false)!,
            rotateLabel: polygon.control.attrBool("rotateLabel", false)!,
            label: polygon.control.attrString("label"),
            labelStyle: parseTextStyle(
                    Theme.of(context), polygon.control, "labelTextStyle") ??
                const TextStyle(),
            strokeCap: strokeCap,
            strokeJoin: strokeJoin,
            points: coordinates != null
                ? (jsonDecode(coordinates) as List)
                    .map((e) => latLngFromJson(e))
                    .toList()
                : []);
      }).toList();

      return PolygonLayer(
        polygons: polygons,
        polygonCulling: control.attrBool("polygonCulling", false)!,
        polygonLabels: control.attrBool("polygonLabels", true)!,
        drawLabelsLast: control.attrBool("drawLabelsLast", false)!,
        simplificationTolerance:
            control.attrDouble("simplificationTolerance", 0.5)!,
        useAltRendering: control.attrBool("useAlternativeRendering", false)!,
      );
    });
  }
}
