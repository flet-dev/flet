import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/box.dart';
import '../utils/charts.dart';
import '../utils/colors.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/numbers.dart';
import '../utils/text.dart';
import 'base_controls.dart';

class LineChartEventData extends Equatable {
  final String eventType;
  final List<LineChartEventDataSpot> barSpots;

  const LineChartEventData({required this.eventType, required this.barSpots});

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

class LineChartControl extends StatefulWidget {
  final Control control;

  LineChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl> {
  LineChartEventData? _eventData;

  final Map<int, List<FlSpot>> _barSpots = {};

  @override
  void initState() {
    debugPrint("LineChart.initState: ${widget.control.id}");
    super.initState();
    widget.control.addListener(_chartUpdated);
    _chartUpdated();
  }

  @override
  void dispose() {
    debugPrint("LineChart.dispose: ${widget.control.id}");
    widget.control.removeListener(_chartUpdated);
    super.dispose();
  }

  _chartUpdated() {
    debugPrint("LineChart._chartUpdated: ${widget.control.id}");
    setState(() {
      for (var lineBar in widget.control.children("data_series")) {
        lineBar.notifyParent = true;
        List<FlSpot> spots = [];
        if (_barSpots.containsKey(lineBar.id)) {
          spots = _barSpots[lineBar.id]!;
        } else {
          _barSpots[lineBar.id] = spots;
        }

        spots.clear();
        for (var spot in lineBar.children("data_points")) {
          spot.notifyParent = true;
          spots.add(FlSpot(spot.getDouble("x")!, spot.getDouble("y")!));
        }
      }

      // removed data series
      for (var lineBarId in _barSpots.keys.toList()) {
        if (!widget.control
            .children("data_series")
            .any((bar) => bar.id == lineBarId)) {
          _barSpots.remove(lineBarId);
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart build: ${widget.control.id}");

    var animate = widget.control.getAnimation("animate");
    var border = widget.control.getBorder("border", Theme.of(context));

    var leftTitles = getAxisTitles(widget.control.child("left_axis"));
    var topTitles = getAxisTitles(widget.control.child("top_axis"));
    var rightTitles = getAxisTitles(widget.control.child("right_axis"));
    var bottomTitles = getAxisTitles(widget.control.child("bottom_axis"));

    var interactive = widget.control.getBool("interactive", true)!;
    var pointLineStart = widget.control.getDouble("point_line_start");
    var pointLineEnd = widget.control.getDouble("point_line_end");

    List<LineChartBarData> barsData = [];
    List<LineBarSpot> selectedPoints = [];

    var barIndex = 0;
    for (var ds in widget.control.children("data_series")) {
      var barData =
          getBarData(Theme.of(context), widget.control, interactive, ds);
      barsData.add(barData);

      var spotIndex = 0;
      for (var p in ds.children("data_points")) {
        if (!interactive && p.getBool("selected", false)!) {
          selectedPoints
              .add(LineBarSpot(barData, barIndex, barData.spots[spotIndex]));
        }
        spotIndex++;
      }

      barIndex++;
    }

    var chart = LineChart(
      LineChartData(
          backgroundColor: widget.control.getColor("bgcolor", context),
          minX: widget.control.getDouble("min_x"),
          maxX: widget.control.getDouble("max_x"),
          minY: widget.control.getDouble("min_y"),
          maxY: widget.control.getDouble("max_y"),
          baselineX: widget.control.getDouble("baseline_x"),
          baselineY: widget.control.getDouble("baseline_y"),
          showingTooltipIndicators: groupBy(selectedPoints, (p) => p.x)
              .values
              .map((e) => ShowingTooltipIndicators(e))
              .toList(),
          titlesData: (leftTitles.sideTitles.showTitles ||
                  topTitles.sideTitles.showTitles ||
                  rightTitles.sideTitles.showTitles ||
                  bottomTitles.sideTitles.showTitles)
              ? FlTitlesData(
                  show: true,
                  leftTitles: leftTitles,
                  topTitles: topTitles,
                  rightTitles: rightTitles,
                  bottomTitles: bottomTitles,
                )
              : const FlTitlesData(show: false),
          borderData: border != null
              ? FlBorderData(show: true, border: border)
              : FlBorderData(show: false),
          gridData: parseChartGridData(widget.control, "horizontal_grid_lines",
              "vertical_grid_lines", Theme.of(context)),
          lineBarsData: barsData,
          lineTouchData: LineTouchData(
            enabled: interactive,
            getTouchLineStart: pointLineStart != null
                ? (barData, spotIndex) => pointLineStart
                : defaultGetTouchLineStart,
            getTouchLineEnd: pointLineEnd != null
                ? (barData, spotIndex) => pointLineEnd
                : defaultGetTouchLineEnd,
            getTouchedSpotIndicator:
                (LineChartBarData barData, List<int> spotIndexes) {
              var barIndex = interactive
                  ? barsData.indexWhere(
                      (b) => b == barData.copyWith(showingIndicators: []))
                  : barsData.indexWhere((b) => b == barData);

              return spotIndexes.map((index) {
                if (barIndex == -1) {
                  return null;
                }

                FlLine? allDotsLine = parseSelectedFlLine(
                    widget.control
                        .children("data_series")[barIndex]
                        .get("selected_below_line"),
                    Theme.of(context),
                    barData.color,
                    barData.gradient);

                FlLine? dotLine = parseSelectedFlLine(
                    widget.control
                        .children("data_series")[barIndex]
                        .children("data_points")[index]
                        .get("selected_below_line"),
                    Theme.of(context),
                    barData.color,
                    barData.gradient);

                return TouchedSpotIndicatorData(
                  dotLine ??
                      allDotsLine ??
                      FlLine(
                          color: defaultGetPointColor(
                              barData.color, barData.gradient, 0),
                          strokeWidth: 3),
                  FlDotData(
                    show: true,
                    getDotPainter: (spot, percent, barData, index) {
                      var allDotsPainter = parseChartSelectedDotPainter(
                          widget.control
                              .children("data_series")[barIndex]
                              .get("selected_point"),
                          Theme.of(context),
                          barData.color,
                          barData.gradient,
                          percent);
                      var dotPainter = parseChartSelectedDotPainter(
                          widget.control
                              .children("data_series")[barIndex]
                              .children("data_points")[index]
                              .get("selected_point"),
                          Theme.of(context),
                          barData.color,
                          barData.gradient,
                          percent);
                      return dotPainter ??
                          allDotsPainter ??
                          getDefaultSelectedPainter(
                              barData.color, barData.gradient, percent);
                    },
                  ),
                );
              }).toList();
            },
            touchTooltipData: LineTouchTooltipData(
              getTooltipColor: (LineBarSpot spot) => widget.control.getColor(
                  "tooltip_bgcolor",
                  context,
                  const Color.fromRGBO(96, 125, 139, 1))!,
              tooltipRoundedRadius:
                  widget.control.getDouble("tooltip_rounded_radius", 4)!,
              tooltipMargin: widget.control.getDouble("tooltip_margin", 16)!,
              tooltipPadding: widget.control.getPadding("tooltip_padding",
                  const EdgeInsets.symmetric(horizontal: 16, vertical: 8))!,
              maxContentWidth:
                  widget.control.getDouble("tooltip_max_content_width", 120)!,
              rotateAngle:
                  widget.control.getDouble("tooltip_rotate_angle", 0.0)!,
              tooltipHorizontalOffset:
                  widget.control.getDouble("tooltip_horizontal_offset", 0)!,
              tooltipBorder: widget.control.getBorderSide(
                      "tooltip_border_side", Theme.of(context)) ??
                  BorderSide.none,
              fitInsideHorizontally: widget.control
                  .getBool("tooltip_fit_inside_horizontally", false)!,
              fitInsideVertically: widget.control
                  .getBool("tooltip_fit_inside_vertically", false)!,
              showOnTopOfTheChartBoxArea: widget.control
                  .getBool("tooltip_show_on_top_of_chart_box_area", false)!,
              getTooltipItems: (touchedSpots) {
                return touchedSpots.map((spot) {
                  var dp = widget.control
                      .children("data_series")[spot.barIndex]
                      .children("data_points")[spot.spotIndex];
                  var tooltip = dp.getString("tooltip_text") ??
                      dp.getDouble("y").toString();
                  var tooltipStyle =
                      dp.getTextStyle("tooltip_style", Theme.of(context));
                  tooltipStyle ??= const TextStyle();
                  if (tooltipStyle.color == null) {
                    tooltipStyle = tooltipStyle.copyWith(
                        color: spot.bar.gradient?.colors.first ??
                            spot.bar.color ??
                            Colors.blueGrey);
                  }
                  TextAlign? tooltipAlign =
                      dp.getTextAlign("tooltip_align", TextAlign.center)!;
                  List<TextSpan>? spans = dp.get("tooltip_spans") != null
                      ? parseTextSpans(
                          Theme.of(context),
                          dp.children("tooltip_spans"),
                          dp.disabled,
                          (Control control, String eventName,
                              String eventData) {
                            control.triggerEvent(eventName, eventData);
                          },
                        )
                      : null;
                  return dp.getBool("show_tooltip", true)!
                      ? LineTooltipItem(tooltip, tooltipStyle,
                          textAlign: tooltipAlign, children: spans)
                      : null;
                }).toList();
              },
            ),
            touchCallback: widget.control.getBool("on_chart_event", false)!
                ? (evt, resp) {
                    var eventData = LineChartEventData(
                        eventType: evt.runtimeType
                            .toString()
                            .substring(2), // remove "Fl"
                        barSpots: resp != null && resp.lineBarSpots != null
                            ? resp.lineBarSpots!
                                .map((bs) => LineChartEventDataSpot(
                                    barIndex: bs.barIndex,
                                    spotIndex: bs.spotIndex))
                                .toList()
                            : []);
                    if (eventData != _eventData) {
                      _eventData = eventData;
                      widget.control
                          .triggerEvent("chart_event", eventData.toMap());
                    }
                  }
                : null,
          )),
      duration: animate != null
          ? animate.duration
          : const Duration(milliseconds: 150), // Optional
      curve: animate != null ? animate.curve : Curves.linear,
    );

    var lb = LayoutBuilder(
        builder: (BuildContext context, BoxConstraints constraints) {
      return (constraints.maxHeight == double.infinity)
          ? ConstrainedBox(
              constraints: const BoxConstraints(maxHeight: 300),
              child: chart,
            )
          : chart;
    });

    return ConstrainedControl(control: widget.control, child: lb);
  }

  LineChartBarData getBarData(ThemeData theme, Control parent,
      bool interactiveChart, Control chartData) {
    Color? aboveLineBgcolor = chartData.getColor("above_line_bgcolor", context);
    Gradient? aboveLineGradient =
        chartData.getGradient("above_line_gradient", theme);
    Color? belowLineBgcolor = chartData.getColor("below_line_bgcolor", context);
    Gradient? belowLineGradient =
        chartData.getGradient("below_line_gradient", theme);
    var dashPattern = chartData.getString("dashPattern");
    var shadow = parseBoxShadow(chartData.get("shadow"), Theme.of(context));
    Color barColor = chartData.getColor("color", context) ?? Colors.cyan;
    Gradient? barGradient = chartData.getGradient("gradient", theme);
    FlLine? aboveLine =
        parseFlLine(chartData.get("above_line"), Theme.of(context));
    FlLine? belowLine =
        parseFlLine(chartData.get("below_line"), Theme.of(context));
    double? aboveLineCutoffY = chartData.getDouble("above_line_cutoff_y");
    double? belowLineCutoffY = chartData.getDouble("below_line_cutoff_y");

    Map<FlSpot, Control> spots = {
      for (var e in chartData.children("data_points"))
        FlSpot(e.getDouble("x")!, e.getDouble("y")!): e
    };
    return LineChartBarData(
        preventCurveOverShooting:
            chartData.getBool("prevent_curve_over_shooting", false)!,
        preventCurveOvershootingThreshold:
            chartData.getDouble("prevent_curve_over_shooting_threshold", 10.0)!,
        spots: _barSpots[chartData.id]!,
        showingIndicators: chartData
            .children("data_points")
            .asMap()
            .entries
            .where(
                (e) => !interactiveChart && e.value.getBool("selected", false)!)
            .map((e) => e.key)
            .toList(),
        isCurved: chartData.getBool("curved", false)!,
        isStrokeCapRound: chartData.getBool("stroke_cap_round", false)!,
        barWidth: chartData.getDouble("stroke_width") ?? 2.0,
        dashArray: dashPattern != null
            ? (json.decode(dashPattern) as List)
                .map((e) => parseInt(e))
                .nonNulls
                .toList()
            : null,
        shadow: shadow ?? const Shadow(color: Colors.transparent),
        dotData: FlDotData(
            show: true,
            getDotPainter: (spot, percent, barData, index) {
              var allDotsPainter = parseChartDotPainter(chartData.get("point"),
                  theme, barColor, barGradient, percent);
              var dotPainter = parseChartDotPainter(
                  chartData.children("data_points")[index].get("point"),
                  theme,
                  barColor,
                  barGradient,
                  percent);
              return dotPainter ?? allDotsPainter ?? getInvisiblePainter();
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

  AxisTitles getAxisTitles(Control? axis) {
    if (axis == null) {
      return const AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axis.buildWidget("title"),
        axisNameSize: axis.getDouble("title_size") ?? 16,
        sideTitles: SideTitles(
          showTitles: axis.getBool("show_labels", true)!,
          reservedSize: axis.getDouble("labels_size") ?? 22,
          interval: axis.getDouble("labels_interval"),
          getTitlesWidget: axis.children("labels").isEmpty
              ? defaultGetTitle
              : (value, meta) {
                  var label = axis
                      .children("labels")
                      .firstWhereOrNull((l) => l.getDouble("value") == value);
                  return label?.buildWidget("label") ?? const SizedBox.shrink();
                },
        ));
  }
}
