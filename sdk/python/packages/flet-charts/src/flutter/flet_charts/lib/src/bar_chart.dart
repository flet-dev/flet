import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/bar_chart.dart';
import 'utils/charts.dart';

class BarChartControl extends StatefulWidget {
  final Control control;

  BarChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<BarChartControl> createState() => _BarChartControlState();
}

class _BarChartControlState extends State<BarChartControl> {
  BarChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("BarChart build: ${widget.control.id}");
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

    List<BarChartGroupData> barGroups = widget.control
        .children("groups")
        .map((group) => parseBarChartGroupData(group, interactive, context))
        .toList();

    var chart = BarChart(
      BarChartData(
        backgroundColor: widget.control.getColor("bgcolor", context),
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
        alignment: parseBarChartAlignment(
            widget.control.getMainAxisAlignment("group_alignment")?.name),
        gridData: parseChartGridData(
            widget.control.get("horizontal_grid_lines"),
            widget.control.get("vertical_grid_lines"),
            theme),
        groupsSpace: widget.control.getDouble("spacing"),
        barGroups: barGroups,
        barTouchData: BarTouchData(
          enabled: interactive,
          touchTooltipData: parseBarTouchTooltipData(context, widget.control),
          touchCallback: widget.control.getBool("on_event", false)!
              ? (FlTouchEvent evt, BarTouchResponse? resp) {
                  var eventData = BarChartEventData.fromDetails(evt, resp);
                  if (eventData != _eventData) {
                    _eventData = eventData;
                    widget.control.triggerEvent("event", eventData.toMap());
                  }
                }
              : null,
        ),
      ),
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
                  child: chart)
              : chart;
        }));
  }
}
