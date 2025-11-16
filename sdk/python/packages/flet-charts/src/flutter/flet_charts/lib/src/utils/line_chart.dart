import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

class LineChartEventData extends Equatable {
  final String eventType;
  final List<LineChartEventDataSpot> barSpots;

  const LineChartEventData({required this.eventType, required this.barSpots});

  factory LineChartEventData.fromDetails(
      FlTouchEvent event, LineTouchResponse? response) {
    return LineChartEventData(
        eventType: resolveFlTouchEventType(event),
        barSpots: response != null && response.lineBarSpots != null
            ? response.lineBarSpots!
                .map((bs) => LineChartEventDataSpot(
                    barIndex: bs.barIndex, spotIndex: bs.spotIndex))
                .toList()
            : []);
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'spots': barSpots,
      };

  @override
  List<Object?> get props => [eventType, barSpots];
}

class LineChartEventDataSpot extends Equatable {
  final int barIndex;
  final int spotIndex;

  const LineChartEventDataSpot(
      {required this.barIndex, required this.spotIndex});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'bar_index': barIndex,
        'spot_index': spotIndex,
      };

  @override
  List<Object?> get props => [barIndex, spotIndex];
}

LineTooltipItem? parseLineTooltipItem(
    Control dataPoint, LineBarSpot spot, BuildContext context) {
  if (!dataPoint.getBool("show_tooltip", true)!) return null;

  var tooltip = dataPoint.internals?["tooltip"];
  if (tooltip == null) return null;

  final theme = Theme.of(context);
  var style = parseTextStyle(tooltip["text_style"], theme, const TextStyle())!;
  if (style.color == null) {
    style = style.copyWith(
        color: spot.bar.gradient?.colors.first ??
            spot.bar.color ??
            Colors.blueGrey);
  }
  return LineTooltipItem(
      tooltip["text"] ?? dataPoint.getDouble("y", 0)!.toString(), style,
      textAlign: parseTextAlign(tooltip["text_align"], TextAlign.center)!,
      textDirection: parseBool(tooltip["rtl"], false)!
          ? TextDirection.rtl
          : TextDirection.ltr,
      children: tooltip["text_spans"] != null
          ? parseTextSpans(tooltip["text_spans"], theme, (s, eventName,
              [eventData]) {
              s.triggerEvent(eventName, eventData);
            })
          : null);
}

LineTouchTooltipData? parseLineTouchTooltipData(
    BuildContext context, Control control,
    [LineTouchTooltipData? defaultValue]) {
  final tooltip = control.get("tooltip");
  if (tooltip == null) return defaultValue;

  final theme = Theme.of(context);

  return LineTouchTooltipData(
    getTooltipColor: (LineBarSpot spot) => parseColor(
        tooltip["bgcolor"], theme, const Color.fromRGBO(96, 125, 139, 1))!,
    tooltipBorderRadius: parseBorderRadius(tooltip["border_radius"]),
    tooltipMargin: parseDouble(tooltip["margin"], 16)!,
    tooltipPadding: parsePadding(tooltip["padding"],
        const EdgeInsets.symmetric(horizontal: 16, vertical: 8))!,
    maxContentWidth: parseDouble(tooltip["max_width"], 120)!,
    rotateAngle: parseDouble(tooltip["rotation"], 0.0)!,
    tooltipHorizontalOffset: parseDouble(tooltip["horizontal_offset"], 0)!,
    tooltipBorder: parseBorderSide(tooltip["border_side"], theme,
        defaultValue: BorderSide.none)!,
    fitInsideHorizontally:
        parseBool(tooltip["fit_inside_horizontally"], false)!,
    fitInsideVertically: parseBool(tooltip["fit_inside_vertically"], false)!,
    showOnTopOfTheChartBoxArea:
        parseBool(tooltip["show_on_top_of_chart_box_area"], false)!,
    tooltipHorizontalAlignment: parseFLHorizontalAlignment(
        tooltip["horizontal_alignment"], FLHorizontalAlignment.center)!,
    getTooltipItems: (List<LineBarSpot> touchedSpots) {
      return touchedSpots
          .map((LineBarSpot spot) => parseLineTooltipItem(
              control
                  .children("data_series")[spot.barIndex]
                  .children("points")[spot.spotIndex],
              spot,
              context))
          .nonNulls
          .toList();
    },
  );
}

LineChartBarData parseLineChartBarData(
    Control parent,
    Control chartData,
    bool interactiveChart,
    BuildContext context,
    Map<int, List<FlSpot>> barSpots) {
  final theme = Theme.of(context);

  var aboveLineBgcolor = chartData.getColor("above_line_bgcolor", context);
  var aboveLineGradient = chartData.getGradient("above_line_gradient", theme);
  var belowLineBgcolor = chartData.getColor("below_line_bgcolor", context);
  var belowLineGradient = chartData.getGradient("below_line_gradient", theme);
  var dashPattern = chartData.get("dash_pattern");
  var barColor = chartData.getColor("color", context, Colors.cyan)!;
  var barGradient = chartData.getGradient("gradient", theme);
  var aboveLine = parseFlLine(chartData.get("above_line"), Theme.of(context));
  var belowLine = parseFlLine(chartData.get("below_line"), Theme.of(context));
  var aboveLineCutoffY = chartData.getDouble("above_line_cutoff_y");
  var belowLineCutoffY = chartData.getDouble("below_line_cutoff_y");
  var stepDirection = chartData.getDouble("step_direction");

  Map<FlSpot, Control> spots = {
    for (var e in chartData.children("points"))
      FlSpot(e.getDouble("x", 0)!, e.getDouble("y", 0)!): e
  };
  return LineChartBarData(
      preventCurveOverShooting:
          chartData.getBool("prevent_curve_over_shooting", false)!,
      preventCurveOvershootingThreshold:
          chartData.getDouble("prevent_curve_over_shooting_threshold", 10.0)!,
      spots: barSpots[chartData.id] ?? [],
      curveSmoothness: chartData.getDouble("curve_smoothness", 0.35)!,
      show: chartData.visible,
      isStepLineChart: stepDirection != null,
      lineChartStepData: LineChartStepData(stepDirection: stepDirection ?? 0.5),
      showingIndicators: chartData
          .children("points")
          .asMap()
          .entries
          .where(
              (dp) => !interactiveChart && dp.value.getBool("selected", false)!)
          .map((e) => e.key)
          .toList(),
      isCurved: chartData.getBool("curved", false)!,
      isStrokeCapRound: chartData.getBool("rounded_stroke_cap", false)!,
      isStrokeJoinRound: chartData.getBool("rounded_stroke_join", false)!,
      barWidth: chartData.getDouble("stroke_width", 2.0)!,
      dashArray: dashPattern != null
          ? (dashPattern as List).map((e) => parseInt(e)).nonNulls.toList()
          : null,
      shadow: parseBoxShadow(chartData.get("shadow"), Theme.of(context)) ??
          const Shadow(color: Colors.transparent),
      dotData: FlDotData(
          show: true,
          getDotPainter: (spot, percent, barData, index) {
            var allDotsPainter = parseChartDotPainter(
                chartData.get("point"), theme, percent, barColor, barGradient);
            var dotPainter = parseChartDotPainter(
                chartData.children("points")[index].get("point"),
                theme,
                percent,
                barColor,
                barGradient);
            return dotPainter ?? allDotsPainter ?? invisibleDotPainter;
          }),
      aboveBarData: aboveLineBgcolor != null ||
              aboveLineGradient != null ||
              aboveLine != null
          ? BarAreaData(
              show: true,
              color: aboveLineBgcolor,
              gradient: aboveLineGradient,
              applyCutOffY: aboveLineCutoffY != null,
              cutOffY: aboveLineCutoffY ?? 0,
              spotsLine: BarAreaSpotsLine(
                show: aboveLine != null,
                flLineStyle: aboveLine ?? const FlLine(),
                checkToShowSpotLine: (spot) =>
                    spots[spot]!.getBool("show_above_line", true)!,
              ))
          : null,
      belowBarData: belowLineBgcolor != null ||
              belowLineGradient != null ||
              belowLine != null
          ? BarAreaData(
              show: true,
              color: belowLineBgcolor,
              gradient: belowLineGradient,
              applyCutOffY: belowLineCutoffY != null,
              cutOffY: belowLineCutoffY ?? 0,
              spotsLine: BarAreaSpotsLine(
                show: belowLine != null,
                flLineStyle: belowLine ?? const FlLine(),
                checkToShowSpotLine: (spot) =>
                    spots[spot]!.getBool("show_below_line", true)!,
              ))
          : null,
      color: barColor,
      gradient: barGradient);
}
