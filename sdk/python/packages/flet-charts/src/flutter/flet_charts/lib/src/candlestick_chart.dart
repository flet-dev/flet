import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/candlestick_chart.dart';
import 'utils/charts.dart';

class CandlestickChartControl extends StatefulWidget {
  final Control control;

  CandlestickChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<CandlestickChartControl> createState() =>
      _CandlestickChartControlState();
}

class _CandlestickChartControlState extends State<CandlestickChartControl> {
  CandlestickChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("CandlestickChart build: ${widget.control.id}");

    final theme = Theme.of(context);
    final animation = widget.control.getAnimation(
        "animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 150),
            curve: Curves.linear))!;
    final border = widget.control.getBorder("border", theme);

    final leftTitles = parseAxisTitles(widget.control.child("left_axis"));
    final topTitles = parseAxisTitles(widget.control.child("top_axis"));
    final rightTitles = parseAxisTitles(widget.control.child("right_axis"));
    final bottomTitles = parseAxisTitles(widget.control.child("bottom_axis"));

    final interactive = widget.control.getBool("interactive", true)!;

    final spotControls = widget.control.children("spots");
    final candlestickSpots = spotControls.map((spot) {
      spot.notifyParent = true;
      return CandlestickSpot(
        x: spot.getDouble("x", 0)!,
        open: spot.getDouble("open", 0)!,
        high: spot.getDouble("high", 0)!,
        low: spot.getDouble("low", 0)!,
        close: spot.getDouble("close", 0)!,
        show: spot.visible,
      );
    }).toList();

    final candlestickTouchData = CandlestickTouchData(
      enabled: interactive && !widget.control.disabled,
      handleBuiltInTouches: !widget.control
          .getBool("show_tooltips_for_selected_spots_only", false)!,
      longPressDuration: widget.control.getDuration("long_press_duration"),
      touchSpotThreshold: widget.control.getDouble("touch_spot_threshold", 4)!,
      touchTooltipData: parseCandlestickTouchTooltipData(
        context,
        widget.control,
        spotControls,
      ),
      touchCallback: widget.control.getBool("on_event", false)!
          ? (event, response) {
              final eventData =
                  CandlestickChartEventData.fromDetails(event, response);
              if (eventData != _eventData) {
                _eventData = eventData;
                widget.control.triggerEvent("event", eventData.toMap());
              }
            }
          : null,
    );

    final chart = CandlestickChart(
      CandlestickChartData(
        candlestickSpots: candlestickSpots,
        backgroundColor: widget.control.getColor("bgcolor", context),
        minX: widget.control.getDouble("min_x"),
        maxX: widget.control.getDouble("max_x"),
        baselineX: widget.control.getDouble("baseline_x"),
        minY: widget.control.getDouble("min_y"),
        maxY: widget.control.getDouble("max_y"),
        baselineY: widget.control.getDouble("baseline_y"),
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
        candlestickTouchData: candlestickTouchData,
        showingTooltipIndicators: spotControls
            .asMap()
            .entries
            .where((e) => e.value.getBool("selected", false)!)
            .map((e) => e.key)
            .toList(),
        rotationQuarterTurns:
            widget.control.getInt("rotation_quarter_turns", 0)!,
      ),
      duration: animation.duration,
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
      }),
    );
  }
}
