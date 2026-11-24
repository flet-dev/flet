import 'dart:math' as math;

import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
// fl_chart does not export the helper it uses to infer omitted axis bounds.
// ignore: implementation_imports
import 'package:fl_chart/src/chart/line_chart/line_chart_helper.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart' show precisionErrorTolerance;
import 'package:material_ui/material_ui.dart';

import 'utils/charts.dart';
import 'utils/line_chart.dart';

/// 16 units in the last place, relative to the magnitude of a double.
const _ulpTolerance = 16 * 2.220446049250313e-16;

typedef _LineSeries = ({
  Control control,
  List<Control> points,
  List<FlSpot> spots
});

class LineChartControl extends StatefulWidget {
  final Control control;

  LineChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl>
    with SingleTickerProviderStateMixin {
  LineChartEventData? _eventData;

  var _series = <_LineSeries>[];
  var _seriesChanged = true;

  // X bounds the chart settles on: explicit, or inferred from the spots.
  double? _minX;
  double? _maxX;

  // Slides the X axis while a rolling window scrolls.
  late final AnimationController _scroll = AnimationController(vsync: this);
  Curve _scrollCurve = Curves.linear;
  (double, double) _scrollFrom = (0, 0);
  (double, double) _scrollTo = (0, 0);
  // After a scroll, fl_chart already shows the latest data. Animating to it
  // again would only repaint identical frames until the next data update.
  var _scrolled = false;

  @override
  void initState() {
    super.initState();
    widget.control.addListener(_chartUpdated);
  }

  @override
  void didUpdateWidget(covariant LineChartControl oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.control != widget.control) {
      oldWidget.control.removeListener(_chartUpdated);
      widget.control.addListener(_chartUpdated);
      _seriesChanged = true;
    }
  }

  @override
  void dispose() {
    widget.control.removeListener(_chartUpdated);
    _scroll.dispose();
    super.dispose();
  }

  void _chartUpdated() {
    // A single patch can notify separately for point changes and axis bounds.
    // Series are rebuilt once per frame, after all of them have landed.
    setState(() => _seriesChanged = true);
  }

  (double, double) get _scrollBounds {
    final t = _scrollCurve.transform(_scroll.value);
    final (fromMin, fromMax) = _scrollFrom;
    final (toMin, toMax) = _scrollTo;
    return (fromMin + (toMin - fromMin) * t, fromMax + (toMax - fromMax) * t);
  }

  /// Rebuilds the series from the control tree and returns whether the update
  /// scrolls a rolling window: both X bounds shift by the same amount and every
  /// series keeps the samples that remain in view.
  bool _updateSeries(double? minX, double? maxX) {
    final previousSeries = _series;
    final previousMinX = _minX;
    final previousMaxX = _maxX;

    _series = widget.control.children("data_series").map((lineBar) {
      lineBar.notifyParent = true;
      final points = lineBar.children("points");
      for (final point in points) {
        point.notifyParent = true;
      }
      return (
        control: lineBar,
        points: points,
        spots: parseLineChartSpots(points)
      );
    }).toList();

    if (minX == null || minX.isNaN || maxX == null || maxX.isNaN) {
      // Use fl_chart's own inference so the detected shift matches the axis
      // fl_chart renders.
      final (inferredMinX, inferredMaxX, _, _) = LineChartHelper()
          .calculateMaxAxisValues(
              [for (final s in _series) LineChartBarData(spots: s.spots)]);
      if (minX == null || minX.isNaN) minX = inferredMinX;
      if (maxX == null || maxX.isNaN) maxX = inferredMaxX;
    }
    _minX = minX;
    _maxX = maxX;

    if (previousMinX == null ||
        previousMaxX == null ||
        previousSeries.length != _series.length) {
      return false;
    }

    final shift = minX - previousMinX;
    // Rounding error grows with the magnitude of X (epoch timestamps, for
    // example), so allow a few units in the last place of the largest bound.
    final tolerance = math.max(
        precisionErrorTolerance,
        _ulpTolerance *
            [minX, maxX, previousMinX, previousMaxX].map((x) => x.abs()).max);
    if (shift.abs() <= tolerance ||
        (maxX - previousMaxX - shift).abs() > tolerance) {
      return false;
    }

    for (var i = 0; i < _series.length; i++) {
      final previous = previousSeries[i];
      final next = _series[i];
      if (previous.control.id != next.control.id ||
          !(shift > 0
              ? _continues(previous.spots, next.spots)
              : _continues(next.spots, previous.spots))) {
        return false;
      }
    }
    return true;
  }

  /// Whether [after] is [before] with samples dropped from the start and/or
  /// appended to the end.
  bool _continues(List<FlSpot> before, List<FlSpot> after) {
    if (after.isEmpty) return before.isEmpty;
    final dropped = before.indexOf(after.first);
    if (dropped < 0) return false;
    final retained = before.length - dropped;
    if (after.length < retained) return false;
    for (var i = 0; i < retained; i++) {
      if (before[dropped + i] != after[i]) return false;
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
    if (_seriesChanged) {
      _seriesChanged = false;
      final displayed = _scroll.isAnimating ? _scrollBounds : (_minX, _maxX);
      if (_updateSeries(minX, maxX) && animation.duration > Duration.zero) {
        _scrollFrom = (displayed.$1!, displayed.$2!);
        _scrollTo = (_minX!, _maxX!);
        _scrollCurve = animation.curve;
        _scroll.duration = animation.duration;
        _scroll.forward(from: 0);
        _scrolled = true;
      } else {
        _scrolled = false;
        // fl_chart animates other updates from whatever is on screen.
        _scroll.stop();
      }
    }

    List<LineChartBarData> barsData = [];
    List<LineBarSpot> selectedPoints = [];

    var barIndex = 0;
    for (final series in _series) {
      final points = series.points;
      var barData = parseLineChartBarData(
          series.control, interactive, context, points, series.spots);
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

    // Indicator callbacks run after build, so keep this frame's series.
    final series = _series;
    final data = LineChartData(
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
              final lineBar = series[barIndex].control;
              final points = series[barIndex].points;
              final point = index < points.length ? points[index] : null;

              var allDotsLine = parseSelectedFlLine(
                  lineBar.get("selected_below_line"),
                  theme,
                  barData.color,
                  barData.gradient);

              FlLine? dotLine = parseSelectedFlLine(
                  point?.get("selected_below_line"),
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
                        lineBar.get("selected_point"),
                        theme,
                        percent,
                        barData.color,
                        barData.gradient,
                        selected: true);
                    var dotPainter = parseChartDotPainter(
                        index < points.length
                            ? points[index].get("selected_point")
                            : null,
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
        ));

    final chart = AnimatedBuilder(
      animation: _scroll,
      builder: (context, _) {
        if (!_scroll.isAnimating) {
          return LineChart(data,
              duration: _scrolled ? Duration.zero : animation.duration,
              curve: animation.curve);
        }
        // The spots already hold the scrolled window. Sliding only the X
        // bounds moves them along the axis, while fl_chart's own tween would
        // pair different samples by index and morph one into another.
        final (minX, maxX) = _scrollBounds;
        return LineChart(data.copyWith(minX: minX, maxX: maxX),
            duration: Duration.zero);
      },
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
