import 'dart:convert';

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'colors.dart';
import 'numbers.dart';

FlGridData parseChartGridData(ThemeData theme, Control control,
    String horizPropName, String vertPropName) {
  var hv = control.attrString(horizPropName, null);
  var vv = control.attrString(vertPropName, null);
  if (hv == null && vv == null) {
    return FlGridData(show: false);
  }

  var hj = hv != null ? json.decode(hv) : null;
  var vj = vv != null ? json.decode(vv) : null;
  var hLine = flineFromJSON(theme, hj);
  var vLine = flineFromJSON(theme, vj);

  return FlGridData(
    show: true,
    drawHorizontalLine: hv != null,
    horizontalInterval: hj != null && hj["interval"] != null
        ? parseDouble(hj["interval"])
        : null,
    getDrawingHorizontalLine: hLine == null ? null : (value) => hLine,
    drawVerticalLine: vv != null,
    verticalInterval: vj != null && vj["interval"] != null
        ? parseDouble(vj["interval"])
        : null,
    getDrawingVerticalLine: vLine == null ? null : (value) => vLine,
  );
}

FlLine? flineFromJSON(theme, j) {
  if (j == null ||
      (j['color'] == null && j['width'] == null && j['dash_pattern'] == null)) {
    return null;
  }
  return FlLine(
      color: j['color'] != null
          ? HexColor.fromString(theme, j['color'] as String)
          : null,
      strokeWidth: j['width'] != null ? parseDouble(j['width'], 1) : null,
      dashArray: j['dash_pattern'] != null
          ? (j['dash_pattern'] as List).map((e) => parseInt(e)).toList()
          : null);
}

FlDotPainter? parseChartDotPainter(
    ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j = json.decode(v);
  return chartDotPainterFromJSON(theme, j);
}

FlDotPainter? chartDotPainterFromJSON(
    ThemeData theme, Map<String, dynamic> json) {
  String type = json["type"];
  if (type == "circle") {
    return FlDotCirclePainter(
        color: json['color'] != null
            ? HexColor.fromString(theme, json['color'] as String)
            : null,
        radius: json["radius"] != null ? parseDouble(json["radius"]) : null,
        strokeColor: json['stroke_color'] != null
            ? HexColor.fromString(theme, json['color'] as String)
            : null,
        strokeWidth: json["stroke_width"] != null
            ? parseDouble(json["stroke_width"])
            : null);
  } else if (type == "square") {
    return FlDotSquarePainter(
        color: json['color'] != null
            ? HexColor.fromString(theme, json['color'] as String)
            : null,
        size: json["size"] != null ? parseDouble(json["size"]) : null,
        strokeColor: json['stroke_color'] != null
            ? HexColor.fromString(theme, json['color'] as String)
            : null,
        strokeWidth: json["stroke_width"] != null
            ? parseDouble(json["stroke_width"])
            : null);
  } else if (type == "cross") {
    return FlDotCrossPainter(
      color: json['color'] != null
          ? HexColor.fromString(theme, json['color'] as String)
          : null,
      size: json["size"] != null ? parseDouble(json["size"]) : null,
      width: json["width"] != null ? parseDouble(json["width"]) : null,
    );
  }
  return null;
}
