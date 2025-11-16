import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

FlDotPainter invisibleDotPainter =
    FlDotCirclePainter(radius: 0, strokeWidth: 0);
FlLine invisibleLine = const FlLine(strokeWidth: 0);

FlGridData parseChartGridData(
    dynamic horizontal, dynamic vertical, ThemeData theme) {
  if (horizontal == null && vertical == null) {
    return const FlGridData(show: false);
  }

  var hLine = parseFlLine(horizontal, theme);
  var vLine = parseFlLine(vertical, theme);

  return FlGridData(
    show: true,
    drawHorizontalLine: horizontal != null,
    horizontalInterval:
        horizontal != null ? parseDouble(horizontal["interval"]) : null,
    getDrawingHorizontalLine:
        hLine == null ? defaultGridLine : (value) => hLine,
    drawVerticalLine: vertical != null,
    verticalInterval:
        vertical != null ? parseDouble(vertical["interval"]) : null,
    getDrawingVerticalLine: vLine == null ? defaultGridLine : (value) => vLine,
  );
}

FlLine? parseFlLine(dynamic value, ThemeData theme, [FlLine? defaultValue]) {
  if (value == null ||
      (value['color'] == null &&
          value['width'] == null &&
          value['gradient'] == null &&
          value['dash_pattern'] == null)) {
    return defaultValue;
  }

  return FlLine(
      color: parseColor(value['color'], theme, Colors.black)!,
      strokeWidth: parseDouble(value['width'], 2)!,
      gradient: parseGradient(value['gradient'], theme),
      dashArray: (value['dash_pattern'] as List?)
          ?.map((e) => parseInt(e))
          .nonNulls
          .toList());
}

FlLine? parseSelectedFlLine(
    dynamic value, ThemeData theme, Color? color, Gradient? gradient,
    [FlLine? defaultValue]) {
  if (value == null) return defaultValue;

  if (value == false) {
    return invisibleLine;
  } else if (value == true) {
    return FlLine(
        color: getDefaultPointColor(0, color, gradient), strokeWidth: 3);
  }

  return parseFlLine(value, theme, defaultValue)?.copyWith(
      color: parseColor(
          value['color'], theme, defaultGetDotStrokeColor(0, color, gradient)));
}

FlDotPainter? parseChartDotPainter(dynamic value, ThemeData theme,
    double percentage, Color? barColor, Gradient? barGradient,
    {FlDotPainter? defaultValue, bool selected = false}) {
  if (value == null) {
    return defaultValue;
  } else if (value == false) {
    return invisibleDotPainter;
  } else if (value == true) {
    return getDefaultDotPainter(percentage, barColor, barGradient,
        selected: selected);
  }
  var type = value["_type"];
  var strokeWidth = parseDouble(value["stroke_width"]);
  var size = parseDouble(value["size"]);
  var color = parseColor(value['color'], theme);
  var strokeColor = parseColor(value['stroke_color'], theme,
      defaultGetDotStrokeColor(percentage, barColor, barGradient))!;

  if (type == "ChartCirclePoint") {
    return FlDotCirclePainter(
        color: color ?? getDefaultPointColor(percentage, barColor, barGradient),
        radius: parseDouble(value["radius"]),
        strokeColor: strokeColor,
        strokeWidth: strokeWidth ?? 0.0);
  } else if (type == "ChartSquarePoint") {
    return FlDotSquarePainter(
        color: color ?? getDefaultPointColor(percentage, barColor, barGradient),
        size: size ?? 4.0,
        strokeColor: strokeColor,
        strokeWidth: strokeWidth ?? 1.0);
  } else if (type == "ChartCrossPoint") {
    return FlDotCrossPainter(
      color:
          color ?? defaultGetDotStrokeColor(percentage, barColor, barGradient),
      size: size ?? 8.0,
      width: parseDouble(value["width"], 2.0)!,
    );
  }
  return defaultValue;
}

FlDotPainter getDefaultDotPainter(
    double percentage, Color? barColor, Gradient? barGradient,
    {bool selected = false}) {
  return FlDotCirclePainter(
    radius: selected ? 8 : 4,
    strokeWidth: selected ? 2 : 1,
    color: getDefaultPointColor(percentage, barColor, barGradient),
    strokeColor: defaultGetDotStrokeColor(percentage, barColor, barGradient),
  );
}

Color getDefaultPointColor(
    double percentage, Color? barColor, Gradient? barGradient) {
  if (barGradient != null && barGradient is LinearGradient) {
    return lerpGradient(
        barGradient.colors, barGradient.getSafeColorStops(), percentage / 100);
  }
  return barGradient?.colors.first ?? barColor ?? Colors.blueGrey;
}

Color defaultGetDotStrokeColor(double percentage,
    [Color? barColor, Gradient? barGradient]) {
  Color color = getDefaultPointColor(percentage, barColor, barGradient);
  return color.darken();
}

AxisTitles parseAxisTitles(Control? control) {
  if (control == null) {
    return const AxisTitles(sideTitles: SideTitles(showTitles: false));
  }

  return AxisTitles(
      axisNameWidget: control.buildWidget("title"),
      axisNameSize: control.getDouble("title_size", 16)!,
      sideTitles: SideTitles(
        showTitles: control.getBool("show_labels", true)!,
        reservedSize: control.getDouble("label_size", 22)!,
        interval: control.getDouble("label_spacing"),
        minIncluded: control.getBool("show_min", true)!,
        maxIncluded: control.getBool("show_max", true)!,
        getTitlesWidget: control.children("labels").isEmpty
            ? defaultGetTitle
            : (double value, TitleMeta meta) {
                var label = control
                    .children("labels")
                    .firstWhereOrNull((l) => l.getDouble("value") == value);
                return label?.buildTextOrWidget("label") ??
                    const SizedBox.shrink();
              },
      ));
}

FLHorizontalAlignment? parseFLHorizontalAlignment(String? value,
    [FLHorizontalAlignment? defaultValue]) {
  if (value == null) return defaultValue;
  return FLHorizontalAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

String resolveFlTouchEventType(FlTouchEvent event) {
  if (event is FlPointerEnterEvent) return "pointerEnter";
  if (event is FlPointerExitEvent) return "pointerExit";
  if (event is FlPointerHoverEvent) return "pointerHover";
  if (event is FlPanCancelEvent) return "panCancel";
  if (event is FlPanDownEvent) return "panDown";
  if (event is FlPanEndEvent) return "panEnd";
  if (event is FlPanStartEvent) return "panStart";
  if (event is FlPanUpdateEvent) return "panUpdate";
  if (event is FlLongPressEnd) return "longPressEnd";
  if (event is FlLongPressMoveUpdate) return "longPressMoveUpdate";
  if (event is FlLongPressStart) return "longPressStart";
  if (event is FlTapCancelEvent) return "tapCancel";
  if (event is FlTapDownEvent) return "tapDown";
  if (event is FlTapUpEvent) return "tapUp";
  return "undefined";
}
