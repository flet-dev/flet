import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/gradient.dart';
import 'colors.dart';
import 'numbers.dart';

FlGridData parseChartGridData(ThemeData theme, Control control,
    String horizPropName, String vertPropName) {
  var hv = control.attrString(horizPropName, null);
  var vv = control.attrString(vertPropName, null);
  if (hv == null && vv == null) {
    return const FlGridData(show: false);
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
    getDrawingHorizontalLine:
        hLine == null ? defaultGridLine : (value) => hLine,
    drawVerticalLine: vv != null,
    verticalInterval: vj != null && vj["interval"] != null
        ? parseDouble(vj["interval"])
        : null,
    getDrawingVerticalLine: vLine == null ? defaultGridLine : (value) => vLine,
  );
}

FlLine? parseFlLine(ThemeData theme, Control control, String propName) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j = json.decode(v);
  return flineFromJSON(theme, j);
}

FlLine? parseSelectedFlLine(ThemeData theme, Control control, String propName,
    Color? color, Gradient? gradient) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j = json.decode(v);
  if (j == false) {
    return getInvisibleLine();
  } else if (j == true) {
    return FlLine(
        color: defaultGetPointColor(color, gradient, 0), strokeWidth: 3);
  }
  return FlLine(
      color: j['color'] != null
          ? parseColor(theme, j['color'] as String, Colors.black)!
          : defaultGetPointColor(color, gradient, 0),
      strokeWidth: parseDouble(j['width'], 2)!,
      dashArray: j['dash_pattern'] != null
          ? (j['dash_pattern'] as List)
              .map((e) => parseInt(e))
              .whereNotNull()
              .toList()
          : null);
}

FlLine? flineFromJSON(theme, j) {
  if (j == null ||
      (j['color'] == null && j['width'] == null && j['dash_pattern'] == null)) {
    return null;
  }
  return FlLine(
      color: j['color'] != null
          ? parseColor(theme, j['color'] as String) ?? Colors.black
          : Colors.black,
      strokeWidth: parseDouble(j['width'], 2)!,
      dashArray: j['dash_pattern'] != null
          ? (j['dash_pattern'] as List)
              .map((e) => parseInt(e))
              .whereNotNull()
              .toList()
          : null);
}

FlDotPainter? parseChartDotPainter(
    ThemeData theme,
    Control control,
    String propName,
    Color? barColor,
    Gradient? barGradient,
    double percentage) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j = json.decode(v);
  if (j == false) {
    return getInvisiblePainter();
  } else if (j == true) {
    return getDefaultPainter(barColor, barGradient, percentage);
  }
  return chartDotPainterFromJSON(theme, j, barColor, barGradient, percentage);
}

FlDotPainter? parseChartSelectedDotPainter(
    ThemeData theme,
    Control control,
    String propName,
    Color? barColor,
    Gradient? barGradient,
    double percentage) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return null;
  }

  final j = json.decode(v);
  if (j == false) {
    return getInvisiblePainter();
  } else if (j == true) {
    return getDefaultSelectedPainter(barColor, barGradient, percentage);
  }
  return chartDotPainterFromJSON(theme, j, barColor, barGradient, percentage);
}

FlDotPainter? chartDotPainterFromJSON(
    ThemeData theme,
    Map<String, dynamic> json,
    Color? barColor,
    Gradient? barGradient,
    double percentage) {
  String type = json["type"];
  if (type == "circle") {
    return FlDotCirclePainter(
        color: json['color'] != null
            ? parseColor(theme, json['color'] as String) ?? Colors.green
            : defaultGetPointColor(barColor, barGradient, percentage),
        radius: parseDouble(json["radius"]),
        strokeColor: json['stroke_color'] != null
            ? parseColor(theme, json['color'] as String) ??
                const Color.fromRGBO(76, 175, 80, 1)
            : defaultGetDotStrokeColor(barColor, barGradient, percentage),
        strokeWidth: parseDouble(json["stroke_width"], 1.0)!);
  } else if (type == "square") {
    return FlDotSquarePainter(
        color: json['color'] != null
            ? parseColor(theme, json['color'] as String) ?? Colors.green
            : defaultGetPointColor(barColor, barGradient, percentage),
        size: parseDouble(json["size"], 4.0)!,
        strokeColor: json['stroke_color'] != null
            ? parseColor(theme, json['color'] as String) ??
                const Color.fromRGBO(76, 175, 80, 1)
            : defaultGetDotStrokeColor(barColor, barGradient, percentage),
        strokeWidth: parseDouble(json["stroke_width"], 1.0)!);
  } else if (type == "cross") {
    return FlDotCrossPainter(
      color: json['color'] != null
          ? parseColor(theme, json['color'] as String) ?? Colors.green
          : defaultGetDotStrokeColor(barColor, barGradient, percentage),
      size: parseDouble(json["size"], 8.0)!,
      width: parseDouble(json["width"], 2.0)!,
    );
  }
  return null;
}

FlDotPainter getInvisiblePainter() {
  return FlDotCirclePainter(radius: 0, strokeWidth: 0);
}

FlLine getInvisibleLine() {
  return const FlLine(strokeWidth: 0);
}

FlDotPainter getDefaultPainter(
    Color? barColor, Gradient? barGradient, double percentage) {
  return FlDotCirclePainter(
      radius: 4,
      color: defaultGetPointColor(barColor, barGradient, percentage),
      strokeColor: defaultGetDotStrokeColor(barColor, barGradient, percentage),
      strokeWidth: 1);
}

FlDotPainter getDefaultSelectedPainter(
    Color? barColor, Gradient? barGradient, double percentage) {
  return FlDotCirclePainter(
      radius: 8,
      color: defaultGetPointColor(barColor, barGradient, percentage),
      strokeColor: defaultGetDotStrokeColor(barColor, barGradient, percentage),
      strokeWidth: 2);
}

Color defaultGetPointColor(
    Color? barColor, Gradient? barGradient, double percentage) {
  if (barGradient != null && barGradient is LinearGradient) {
    return lerpGradient(
        barGradient.colors, barGradient.getSafeColorStops(), percentage / 100);
  }
  return barGradient?.colors.first ?? barColor ?? Colors.blueGrey;
}

Color defaultGetDotStrokeColor(
    Color? barColor, Gradient? barGradient, double percentage) {
  Color color;
  if (barGradient != null && barGradient is LinearGradient) {
    color = lerpGradient(
        barGradient.colors, barGradient.getSafeColorStops(), percentage / 100);
  } else {
    color = barGradient?.colors.first ?? barColor ?? Colors.blueGrey;
  }
  return color.darken();
}
