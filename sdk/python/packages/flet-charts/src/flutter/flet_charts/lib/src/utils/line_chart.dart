import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';

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
        'spots': barSpots.map((spot) => spot.toMap()).toList(),
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

LineChartBarData parseLineChartBarData(Control chartData, bool interactiveChart,
    BuildContext context, List<Control> points, List<FlSpot> spots) {
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

  return LineChartBarData(
      preventCurveOverShooting:
          chartData.getBool("prevent_curve_over_shooting", false)!,
      preventCurveOvershootingThreshold:
          chartData.getDouble("prevent_curve_over_shooting_threshold", 10.0)!,
      spots: spots,
      curveSmoothness: chartData.getDouble("curve_smoothness", 0.35)!,
      show: chartData.visible,
      isStepLineChart: stepDirection != null,
      lineChartStepData: LineChartStepData(stepDirection: stepDirection ?? 0.5),
      showingIndicators: points
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
            var dotPainter = parseChartDotPainter(points[index].get("point"),
                theme, percent, barColor, barGradient);
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
              spotsLine: _parseAreaSpotsLine(
                  aboveLine, points, spots, "show_above_line"))
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
              spotsLine: _parseAreaSpotsLine(
                  belowLine, points, spots, "show_below_line"))
          : null,
      color: barColor,
      gradient: barGradient);
}

/// Builds the spots of a series from its point controls.
List<FlSpot> parseLineChartSpots(List<Control> points) => [
      for (final point in points)
        FlSpot(point.getDouble("x")!, point.getDouble("y")!)
    ];

BarAreaSpotsLine _parseAreaSpotsLine(FlLine? style, List<Control> points,
    List<FlSpot> spots, String visibilityProperty) {
  if (style == null) return const BarAreaSpotsLine();
  if (points.every((point) => point.getBool(visibilityProperty, true)!)) {
    return BarAreaSpotsLine(
      show: true,
      flLineStyle: style,
      checkToShowSpotLine: (spot) => spot.isNotNull(),
    );
  }

  // Only built when some point hides its line, to keep streaming cheap.
  final indexes = Map<FlSpot, int>.identity();
  for (final (index, spot) in spots.indexed) {
    indexes[spot] = index;
  }
  var next = 0;
  return BarAreaSpotsLine(
    show: true,
    flLineStyle: style,
    checkToShowSpotLine: (spot) {
      // Spots of a settled chart are the ones parsed from the points, so their
      // index is known. While an animation runs, fl_chart paints interpolated
      // copies, in list order and paired by index with the destination list,
      // so count on from the last spot seen. The count resyncs on every known
      // spot, so a missed or extra call cannot misplace flags for good.
      final index = indexes[spot] ?? next % points.length;
      next = index + 1;
      return index < points.length &&
          points[index].getBool(visibilityProperty, true)! &&
          spot.isNotNull();
    },
  );
}
