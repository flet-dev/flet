import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/gradient.dart';
import 'colors.dart';
import 'numbers.dart';

FlGridData parseChartGridData(ThemeData theme, Control control,
    String horizPropName, String vertPropName) {
  var hv = control.get(horizPropName);
  var vv = control.get(vertPropName);
  if (hv == null && vv == null) {
    return const FlGridData(show: false);
  }

  var hLine = flineFromJSON(theme, hv);
  var vLine = flineFromJSON(theme, vv);

  return FlGridData(
    show: true,
    drawHorizontalLine: hv != null,
    horizontalInterval: hv != null && hv["interval"] != null
        ? parseDouble(hv["interval"])
        : null,
    getDrawingHorizontalLine:
        hLine == null ? defaultGridLine : (value) => hLine,
    drawVerticalLine: vv != null,
    verticalInterval: vv != null && vv["interval"] != null
        ? parseDouble(vv["interval"])
        : null,
    getDrawingVerticalLine: vLine == null ? defaultGridLine : (value) => vLine,
  );
}

FlLine? parseFlLine(dynamic value, ThemeData theme, [FlLine? defaultValue]) {
  if (value == null) return defaultValue;
  return flineFromJSON(theme, value);
}

FlLine? parseSelectedFlLine(
    dynamic value, ThemeData theme, Color? color, Gradient? gradient,
    [FlLine? defaultValue]) {
  if (value == null) return defaultValue;

  if (value == false) {
    return getInvisibleLine();
  } else if (value == true) {
    return FlLine(
        color: defaultGetPointColor(color, gradient, 0), strokeWidth: 3);
  }
  return FlLine(
      color: value['color'] != null
          ? parseColor(value['color'] as String, theme, Colors.black)!
          : defaultGetPointColor(color, gradient, 0),
      strokeWidth: parseDouble(value['width'], 2)!,
      dashArray: value['dash_pattern'] != null
          ? (value['dash_pattern'] as List)
              .map((e) => parseInt(e))
              .nonNulls
              .toList()
          : null);
}

FlLine? flineFromJSON(theme, j) {
  if (j == null ||
      (j['color'] == null && j['width'] == null && j['dash_pattern'] == null)) {
    return null;
  }
  return FlLine(
      color: parseColor(j['color'] as String?, theme, Colors.black)!,
      strokeWidth: parseDouble(j['width'], 2)!,
      dashArray: j['dash_pattern'] != null
          ? (j['dash_pattern'] as List)
              .map((e) => parseInt(e))
              .nonNulls
              .toList()
          : null);
}

FlDotPainter? parseChartDotPainter(dynamic value, ThemeData theme,
    Color? barColor, Gradient? barGradient, double percentage,
    [FlDotPainter? defaultValue]) {
  if (value == null) return defaultValue;

  if (value == false) {
    return getInvisiblePainter();
  } else if (value == true) {
    return getDefaultPainter(barColor, barGradient, percentage);
  }
  return chartDotPainterFromJSON(
      theme, value, barColor, barGradient, percentage, defaultValue);
}

FlDotPainter? parseChartSelectedDotPainter(dynamic value, ThemeData theme,
    Color? barColor, Gradient? barGradient, double percentage,
    [FlDotPainter? defaultValue]) {
  if (value == null) return defaultValue;

  if (value == false) {
    return getInvisiblePainter();
  } else if (value == true) {
    return getDefaultSelectedPainter(barColor, barGradient, percentage);
  }
  return chartDotPainterFromJSON(
      theme, value, barColor, barGradient, percentage);
}

FlDotPainter? chartDotPainterFromJSON(
    ThemeData theme,
    Map<dynamic, dynamic> json,
    Color? barColor,
    Gradient? barGradient,
    double percentage,
    [FlDotPainter? defaultValue]) {
  String type = json["type"];
  if (type == "circle") {
    return FlDotCirclePainter(
        color: json['color'] != null
            ? parseColor(json['color'] as String, theme) ?? Colors.green
            : defaultGetPointColor(barColor, barGradient, percentage),
        radius: parseDouble(json["radius"]),
        strokeColor: json['stroke_color'] != null
            ? parseColor(json['color'] as String, theme) ??
                const Color.fromRGBO(76, 175, 80, 1)
            : defaultGetDotStrokeColor(barColor, barGradient, percentage),
        strokeWidth: parseDouble(json["stroke_width"], 0.0)!);
  } else if (type == "square") {
    return FlDotSquarePainter(
        color: json['color'] != null
            ? parseColor(json['color'] as String, theme) ?? Colors.green
            : defaultGetPointColor(barColor, barGradient, percentage),
        size: parseDouble(json["size"], 4.0)!,
        strokeColor: json['stroke_color'] != null
            ? parseColor(json['color'] as String, theme) ??
                const Color.fromRGBO(76, 175, 80, 1)
            : defaultGetDotStrokeColor(barColor, barGradient, percentage),
        strokeWidth: parseDouble(json["stroke_width"], 1.0)!);
  } else if (type == "cross") {
    return FlDotCrossPainter(
      color: json['color'] != null
          ? parseColor(json['color'] as String, theme) ?? Colors.green
          : defaultGetDotStrokeColor(barColor, barGradient, percentage),
      size: parseDouble(json["size"], 8.0)!,
      width: parseDouble(json["width"], 2.0)!,
    );
  }
  return defaultValue;
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
