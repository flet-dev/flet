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
    debugPrint(
        "PolylineLayerControl build: ${control.id} (${control.hashCode})");

    return withControls(control.childIds, (context, polylinesView) {
      debugPrint("PolylineLayerControlState build: ${control.id}");

      var polylines = polylinesView.controlViews
          .where((c) =>
              c.control.type == "mappolylinemarker" && c.control.isVisible)
          .map((polyline) {
        var strokeCap = StrokeCap.values.firstWhereOrNull((e) =>
            e.name.toLowerCase() ==
            control.attrString("strokeCap", "")!.toLowerCase());
        var strokeJoin = StrokeJoin.values.firstWhereOrNull((e) =>
            e.name.toLowerCase() ==
            control.attrString("strokeJoin", "")!.toLowerCase());
        var points = polyline.control.attrString("points");
        var colorsStop = polyline.control.attrString("colorsStop");
        var gradientColors = polyline.control.attrString("gradientColors");
        return Polyline(
            borderStrokeWidth:
                polyline.control.attrDouble("borderStrokeWidth", 0)!,
            borderColor: polyline.control.attrColor("borderColor", context) ??
                const Color(0xFFFFFF00),
            color: polyline.control.attrColor("color", context) ??
                const Color(0xFF00FF00),
            isDotted: polyline.control.attrBool("dotted", false)!,
            strokeCap: strokeCap ?? StrokeCap.round,
            strokeJoin: strokeJoin ?? StrokeJoin.round,
            strokeWidth: polyline.control.attrDouble("strokeWidth", 1.0)!,
            useStrokeWidthInMeter:
                polyline.control.attrBool("useStrokeWidthInMeter", false)!,
            colorsStop: colorsStop != null
                ? (jsonDecode(colorsStop) as List)
                    .map((e) => parseDouble(e))
                    .toList()
                : null,
            gradientColors: gradientColors != null
                ? (jsonDecode(gradientColors) as List)
                    .map((e) => parseColor(Theme.of(context), e))
                    .whereNotNull()
                    .toList()
                : null,
            points: points != null
                ? (jsonDecode(points) as List)
                    .map((e) => latLngFromJson(e))
                    .toList()
                : []);
      }).toList();

      return PolylineLayer(
        polylines: polylines,
        polylineCulling: control.attrBool("polylineCulling", false)!,
      );
    });
  }
}
