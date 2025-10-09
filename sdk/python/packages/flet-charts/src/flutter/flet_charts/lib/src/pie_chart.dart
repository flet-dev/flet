import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'utils/pie_chart.dart';

class PieChartControl extends StatefulWidget {
  final Control control;

  PieChartControl({Key? key, required this.control})
      : super(key: ValueKey("control_${control.id}"));

  @override
  State<PieChartControl> createState() => _PieChartControlState();
}

class _PieChartControlState extends State<PieChartControl> {
  PieChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("PieChart build: ${widget.control.id}");

    var animation = widget.control.getAnimation(
        "animation",
        ImplicitAnimationDetails(
            duration: const Duration(milliseconds: 150),
            curve: Curves.linear))!;

    List<PieChartSectionData> sections = widget.control
        .children("sections")
        .map((section) => parsePieChartSectionData(section, context))
        .toList();

    Widget chart = PieChart(
      PieChartData(
        centerSpaceColor:
            widget.control.getColor("center_space_color", context),
        centerSpaceRadius: widget.control.getDouble("center_space_radius"),
        sectionsSpace: widget.control.getDouble("sections_space"),
        startDegreeOffset: widget.control.getDouble("start_degree_offset"),
        pieTouchData: PieTouchData(
          enabled: true,
          touchCallback: widget.control.getBool("on_event", false)!
              ? (FlTouchEvent evt, PieTouchResponse? resp) {
                  var eventData = PieChartEventData.fromDetails(evt, resp);
                  if (eventData != _eventData) {
                    _eventData = eventData;
                    widget.control.triggerEvent("event", eventData.toMap());
                  }
                }
              : null,
        ),
        sections: sections,
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
