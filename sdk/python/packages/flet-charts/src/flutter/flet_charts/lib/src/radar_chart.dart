import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/radar_chart.dart';

class RadarChartControl extends StatefulWidget {
  final Control control;

  RadarChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<RadarChartControl> createState() => _RadarChartControlState();
}

class _RadarChartControlState extends State<RadarChartControl> {
  RadarChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("RadarChart build: ${widget.control.id}‚");

    final theme = Theme.of(context);
    final animation = widget.control.getAnimation(
        "animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 150),
            curve: Curves.linear))!;
    final interactive = widget.control.getBool("interactive", true)! &&
        !widget.control.disabled;
    final border = widget.control.getBorder("border", theme);
    final titleControls = widget.control.children("titles", visibleOnly: false);

    final chart = RadarChart(
      RadarChartData(
        dataSets: widget.control
            .children("data_sets")
            .map((ds) => parseRadarDataSet(ds, theme, context))
            .toList(),

        // Radar and borders
        radarBackgroundColor: widget.control
            .getColor("radar_bgcolor", context, Colors.transparent)!,
        radarBorderData: widget.control.getBorderSide(
            "radar_border_side", theme,
            defaultValue: const BorderSide(width: 2))!,
        radarShape: parseRadarShape(
            widget.control.get("radar_shape"), RadarShape.polygon)!,
        borderData: FlBorderData(show: border != null, border: border),
        gridBorderData: widget.control.getBorderSide("grid_border_side", theme,
            defaultValue: const BorderSide(width: 2))!,

        // Titles
        titleTextStyle: widget.control.getTextStyle("title_text_style", theme),
        titlePositionPercentageOffset:
            widget.control.getDouble("title_position_percentage_offset", 0.2)!,
        getTitle: titleControls.isNotEmpty
            ? (int index, double angle) {
                if (index >= titleControls.length) {
                  return RadarChartTitle(text: '', angle: angle);
                }
                final ctrl = titleControls[index];
                return parseRadarChartTitle(ctrl, theme, angle);
              }
            : null,

        // Ticks
        tickCount: widget.control.getInt("tick_count", 1)!,
        ticksTextStyle: widget.control.getTextStyle("ticks_text_style", theme),
        tickBorderData: widget.control.getBorderSide("tick_border_side", theme,
            defaultValue: const BorderSide(width: 2))!,
        isMinValueAtCenter: widget.control.getBool("center_min_value", false)!,

        // Interaction
        radarTouchData: RadarTouchData(
          enabled: interactive,
          longPressDuration: widget.control.getDuration("long_press_duration"),
          touchSpotThreshold: widget.control.getDouble("touch_spot_threshold"),
          touchCallback: (event, response) {
            final eventData = RadarChartEventData.fromDetails(event, response);
            if (eventData != _eventData) {
              _eventData = eventData;
              widget.control.triggerEvent("event", eventData.toMap());
            }
          },
        ),
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
