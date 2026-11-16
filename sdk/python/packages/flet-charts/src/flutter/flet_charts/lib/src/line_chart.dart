import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show precisionErrorTolerance;
import 'package:material_ui/material_ui.dart';

import 'utils/charts.dart';
import 'utils/line_chart.dart';

typedef _LineSeries = ({List<Control> points, List<FlSpot> spots});

class LineChartControl extends StatefulWidget {
  final Control control;

  LineChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl> {
  LineChartEventData? _eventData;

  final _series = <int, _LineSeries>{};
  double? _minX;
  double? _maxX;

  @override
  void initState() {
    super.initState();
    widget.control.addListener(_chartUpdated);
  }

  @override
  void dispose() {
    widget.control.removeListener(_chartUpdated);
    super.dispose();
  }

  void _chartUpdated() {
    setState(() {});
  }

  void _updateSeries(List<Control> dataSeries, double? minX, double? maxX) {
    // A single patch can notify separately for point changes and axis bounds.
    // Compare complete frames after all of those operations have landed.
    final nextSeries = <int, _LineSeries>{};
    for (final lineBar in dataSeries) {
      lineBar.notifyParent = true;
      final points = lineBar.children("points");
      final spots = points.map((spot) {
        spot.notifyParent = true;
        return FlSpot(spot.getDouble("x")!, spot.getDouble("y")!);
      }).toList();
      nextSeries[lineBar.id] = (points: points, spots: spots);
    }

    // When a bound is omitted, fl_chart uses the X extent of the series.
    final inferMinX = minX?.isNaN ?? true;
    final inferMaxX = maxX?.isNaN ?? true;
    if (inferMinX || inferMaxX) {
      final xs = nextSeries.values
          .expand((series) => series.spots)
          .map((spot) => spot.x)
          .where((x) => x.isFinite);
      if (inferMinX) minX = xs.minOrNull;
      if (inferMaxX) maxX = xs.maxOrNull;
    }

    final previousMinX = _minX;
    final previousMaxX = _maxX;
    final shift =
        minX != null && previousMinX != null ? minX - previousMinX : 0.0;
    final scrolls = shift != 0 &&
        maxX != null &&
        previousMaxX != null &&
        (maxX - previousMaxX - shift).abs() < precisionErrorTolerance;

    for (final MapEntry(key: id, value: next) in nextSeries.entries) {
      final previous = _series[id];
      if (scrolls &&
          previous != null &&
          (shift > 0
              ? _hasRollingOverlap(previous.spots, next.spots)
              : _hasRollingOverlap(next.spots, previous.spots))) {
        // Use the same samples on both ends of the tween while the X axis
        // slides. fl_chart otherwise interpolates by index, which would
        // morph each retained sample into a different one.
        previous.spots.setAll(0, next.spots);
        previous.points.setAll(0, next.points);
      } else {
        // Preserve the previous coordinates for ordinary point animations.
        _series[id] = next;
      }
    }
    _series.removeWhere((id, _) => !nextSeries.containsKey(id));
    _minX = minX;
    _maxX = maxX;
  }

  bool _hasRollingOverlap(List<FlSpot> previous, List<FlSpot> next) {
    if (previous.length != next.length || next.isEmpty) return false;
    final dropped = previous.indexOf(next.first);
    if (dropped <= 0) return false;

    for (var i = dropped; i < previous.length; i++) {
      if (previous[i] != next[i - dropped]) return false;
    }
    return true;
  }

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart build: ${widget.control.id}");
    final theme = Theme.of(context);
    var animation = widget.control.getAnimation(
        "animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 150),
            curve: Curves.linear))!;
    var border = widget.control.getBorder("border", theme);
    var leftTitles = parseAxisTitles(widget.control.child("left_axis"));
    var topTitles = parseAxisTitles(widget.control.child("top_axis"));
    var rightTitles = parseAxisTitles(widget.control.child("right_axis"));
    var bottomTitles = parseAxisTitles(widget.control.child("bottom_axis"));
    var interactive = widget.control.getBool("interactive", true)!;
    var pointLineStart = widget.control.getDouble("point_line_start");
    var pointLineEnd = widget.control.getDouble("point_line_end");
    final minX = widget.control.getDouble("min_x");
    final maxX = widget.control.getDouble("max_x");
    final dataSeries = widget.control.children("data_series");
    _updateSeries(dataSeries, minX, maxX);

    List<LineChartBarData> barsData = [];
    List<LineBarSpot> selectedPoints = [];

    var barIndex = 0;
    for (var ds in dataSeries) {
      final series = _series[ds.id]!;
      final points = series.points;
      var barData = parseLineChartBarData(
          ds, interactive, context, points, series.spots);
      barsData.add(barData);

      var spotIndex = 0;
      for (var p in points) {
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
          minX: minX,
          maxX: maxX,
          minY: widget.control.getDouble("min_y"),
          maxY: widget.control.getDouble("max_y"),
          baselineX: widget.control.getDouble("baseline_x"),
          baselineY: widget.control.getDouble("baseline_y"),
          showingTooltipIndicators: groupBy(selectedPoints, (p) => p.x)
              .values
              .map((e) => ShowingTooltipIndicators(e))
              .toList(),
          titlesData: FlTitlesData(
            show: (leftTitles.sideTitles.showTitles ||
                topTitles.sideTitles.showTitles ||
                rightTitles.sideTitles.showTitles ||
                bottomTitles.sideTitles.showTitles),
            leftTitles: leftTitles,
            topTitles: topTitles,
            rightTitles: rightTitles,
            bottomTitles: bottomTitles,
          ),
          borderData: FlBorderData(show: border != null, border: border),
          gridData: parseChartGridData(
              widget.control.get("horizontal_grid_lines"),
              widget.control.get("vertical_grid_lines"),
              theme),
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
                if (barIndex == -1) return null;

                var allDotsLine = parseSelectedFlLine(
                    widget.control
                        .children("data_series")[barIndex]
                        .get("selected_below_line"),
                    theme,
                    barData.color,
                    barData.gradient);

                FlLine? dotLine = parseSelectedFlLine(
                    widget.control
                        .children("data_series")[barIndex]
                        .children("points")[index]
                        .get("selected_below_line"),
                    theme,
                    barData.color,
                    barData.gradient);

                return TouchedSpotIndicatorData(
                  dotLine ??
                      allDotsLine ??
                      FlLine(
                          color: getDefaultPointColor(
                              0, barData.color, barData.gradient),
                          strokeWidth: 3),
                  FlDotData(
                    show: true,
                    getDotPainter: (spot, percent, barData, index) {
                      var allDotsPainter = parseChartDotPainter(
                          widget.control
                              .children("data_series")[barIndex]
                              .get("selected_point"),
                          theme,
                          percent,
                          barData.color,
                          barData.gradient,
                          selected: true);
                      var dotPainter = parseChartDotPainter(
                          widget.control
                              .children("data_series")[barIndex]
                              .children("points")[index]
                              .get("selected_point"),
                          theme,
                          percent,
                          barData.color,
                          barData.gradient,
                          selected: true);
                      return dotPainter ??
                          allDotsPainter ??
                          getDefaultDotPainter(
                              percent, barData.color, barData.gradient,
                              selected: true);
                    },
                  ),
                );
              }).toList();
            },
            touchTooltipData: parseLineTouchTooltipData(
                context, widget.control, const LineTouchTooltipData())!,
            touchCallback: widget.control.getBool("on_event", false)!
                ? (evt, resp) {
                    var eventData = LineChartEventData.fromDetails(evt, resp);
                    if (eventData != _eventData) {
                      _eventData = eventData;
                      widget.control.triggerEvent("event", eventData.toMap());
                    }
                  }
                : null,
          )),
      duration: animation.duration, // Optional
      curve: animation.curve,
    );

    return LayoutControl(
        control: widget.control,
        child: LayoutBuilder(
            builder: (BuildContext context, BoxConstraints constraints) {
          return (constraints.maxHeight == double.infinity)
              ? ConstrainedBox(
                  constraints: const BoxConstraints(maxHeight: 300),
                  child: chart,
                )
              : chart;
        }));
  }
}
