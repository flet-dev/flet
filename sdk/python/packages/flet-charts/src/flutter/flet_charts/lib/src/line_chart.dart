import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/charts.dart';
import 'utils/line_chart.dart';

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
    super.initState();
    widget.control.addListener(_chartUpdated);
    _chartUpdated();
  }

  @override
  void dispose() {
    widget.control.removeListener(_chartUpdated);
    super.dispose();
  }

  _chartUpdated() {
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
        for (var spot in lineBar.children("points")) {
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

    List<LineChartBarData> barsData = [];
    List<LineBarSpot> selectedPoints = [];

    var barIndex = 0;
    for (var ds in widget.control.children("data_series")) {
      var barData = parseLineChartBarData(
          widget.control, ds, interactive, context, _barSpots);
      barsData.add(barData);

      var spotIndex = 0;
      for (var p in ds.children("points")) {
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

    return ConstrainedControl(
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
