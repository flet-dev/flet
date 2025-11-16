import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/charts.dart';
import 'utils/scatter_chart.dart';

class ScatterChartControl extends StatefulWidget {
  final Control control;

  ScatterChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<ScatterChartControl> createState() => _ScatterChartControlState();
}

class _ScatterChartControlState extends State<ScatterChartControl> {
  @override
  Widget build(BuildContext context) {
    debugPrint("ScatterChart build: ${widget.control.id}");

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

    // Build list of ScatterSpotData
    final spotsAsControls = widget.control.children('spots');
    final spots = spotsAsControls.map((spot) {
      spot.notifyParent = true;
      var x = spot.getDouble('x', 0)!;
      var y = spot.getDouble('y', 0)!;
      return ScatterSpot(x, y,
          show: spot.visible,
          renderPriority: spot.getInt('render_priority', 0)!,
          xError: spot.get('x_error'),
          yError: spot.get('y_error'),
          dotPainter: spot.get("point") != null
              ? parseChartDotPainter(spot.get("point"), theme, 0, null, null)
              : FlDotCirclePainter(
                  radius: spot.getDouble("radius"),
                  color: spot.getColor(
                      "color",
                      context,
                      Colors.primaries[
                          ((x * y) % Colors.primaries.length).toInt()])!,
                ));
    }).toList();

    final chart = ScatterChart(
      ScatterChartData(
        scatterSpots: spots,
        backgroundColor: widget.control.getColor("bgcolor", context),
        minX: widget.control.getDouble("min_x"),
        maxX: widget.control.getDouble("max_x"),
        minY: widget.control.getDouble("min_y"),
        maxY: widget.control.getDouble("max_y"),
        baselineX: widget.control.getDouble("baseline_x"),
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
        scatterTouchData: ScatterTouchData(
          enabled: interactive && !widget.control.disabled,
          touchCallback: widget.control.getBool("on_event", false)!
              ? (evt, resp) {
                  var eventData = ScatterChartEventData.fromDetails(evt, resp);
                  widget.control.triggerEvent("event", eventData.toMap());
                }
              : null,
          longPressDuration: widget.control.getDuration("long_press_duration"),
          handleBuiltInTouches: !widget.control
              .getBool("show_tooltips_for_selected_spots_only", false)!,
          touchTooltipData:
              parseScatterTouchTooltipData(context, widget.control, spots),
        ),
        scatterLabelSettings: ScatterLabelSettings(
          showLabel: true,
          getLabelFunction: (spotIndex, spot) {
            var dp = spotsAsControls[spotIndex];
            return dp.getString("label_text", "")!;
          },
          getLabelTextStyleFunction: (spotIndex, spot) {
            var dp = spotsAsControls[spotIndex];
            var labelStyle =
                dp.getTextStyle("label_text_style", theme, const TextStyle())!;
            if (labelStyle.color == null) {
              labelStyle =
                  labelStyle.copyWith(color: spot.dotPainter.mainColor);
            }
            return labelStyle;
          },
        ),
        showingTooltipIndicators: spotsAsControls
            .asMap()
            .entries
            .where((e) => e.value.getBool("selected", false)!)
            .map((e) => e.key)
            .toList(),
        rotationQuarterTurns:
            widget.control.getInt('rotation_quarter_turns', 0)!,
        //errorIndicatorData: widget.control.get('error_indicator_data'),
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
                  child: chart)
              : chart;
        }));
  }
}
