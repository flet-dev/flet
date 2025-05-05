import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

const eventMap = {
  "FlPointerEnterEvent": "pointerEnter",
  "FlPointerExitEvent": "pointerExit",
  "FlPointerHoverEvent": "pointerHover",
  "FlPanCancelEvent": "panCancel",
  "FlPanDownEvent": "panDown",
  "FlPanEndEvent": "panEnd",
  "FlPanStartEvent": "panStart",
  "FlPanUpdateEvent": "panUpdate",
  "FlLongPressEnd": "longPressEnd",
  "FlLongPressMoveUpdate": "longPressMoveUpdate",
  "FlLongPressStart": "longPressStart",
  "FlTapCancelEvent": "tapCancel",
  "FlTapDownEvent": "tapDown",
  "FlTapUpEvent": "tapUp",
};

class PieChartEventData extends Equatable {
  final String eventType;
  final int? sectionIndex;
  final Offset? localPosition;

  const PieChartEventData(
      {required this.eventType,
      required this.sectionIndex,
      this.localPosition});

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'section_index': sectionIndex,
        "local_x": localPosition?.dx,
        "local_y": localPosition?.dy
      };

  @override
  List<Object?> get props => [eventType, sectionIndex];
}

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

    var animate = widget.control.getAnimation("animate");

    List<PieChartSectionData> sections = widget.control
        .children("sections")
        .map((section) => getSectionData(section))
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
          touchCallback: widget.control.getBool("on_chart_event", false)!
              ? (FlTouchEvent evt, PieTouchResponse? resp) {
                  var type = evt.toString();
                  var eventData = PieChartEventData(
                    // grab the event type found in between '' quotes
                    eventType: eventMap[type.substring(
                            type.indexOf("'") + 1, type.lastIndexOf("'"))] ??
                        "undefined",
                    sectionIndex: resp?.touchedSection?.touchedSectionIndex,
                    localPosition: evt.localPosition,
                  );
                  if (eventData != _eventData) {
                    _eventData = eventData;
                    widget.control
                        .triggerEvent("chart_event", eventData.toMap());
                  }
                }
              : null,
        ),
        sections: sections,
      ),
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

  PieChartSectionData getSectionData(Control section) {
    section.notifyParent = true;
    var theme = Theme.of(context);
    return PieChartSectionData(
      value: section.getDouble("value"),
      color: section.getColor("color", context),
      radius: section.getDouble("radius"),
      showTitle: section.getString("title", "")! != "",
      title: section.getString("title"),
      titleStyle: section.getTextStyle("title_style", theme),
      borderSide: section.getBorderSide("border_side", theme,
          defaultValue: BorderSide.none),
      titlePositionPercentageOffset: section.getDouble("title_position"),
      badgeWidget: section.buildWidget("badge_content"),
      badgePositionPercentageOffset: section.getDouble("badge_position"),
    );
  }
}
