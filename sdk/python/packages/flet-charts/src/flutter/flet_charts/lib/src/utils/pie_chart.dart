import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

class PieChartEventData extends Equatable {
  final String eventType;
  final int? sectionIndex;
  final Offset? localPosition;

  const PieChartEventData(
      {required this.eventType,
      required this.sectionIndex,
      this.localPosition});

  factory PieChartEventData.fromDetails(
      FlTouchEvent event, PieTouchResponse? response) {
    return PieChartEventData(
      eventType: resolveFlTouchEventType(event),
      sectionIndex: response?.touchedSection?.touchedSectionIndex,
      localPosition: event.localPosition,
    );
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'section_index': sectionIndex,
        "local_x": localPosition?.dx,
        "local_y": localPosition?.dy
      };

  @override
  List<Object?> get props => [eventType, sectionIndex];
}

PieChartSectionData parsePieChartSectionData(
    Control section, BuildContext context) {
  section.notifyParent = true;
  var theme = Theme.of(context);
  var title = section.getString("title");
  return PieChartSectionData(
    value: section.getDouble("value"),
    color: section.getColor("color", context),
    radius: section.getDouble("radius"),
    showTitle: title != null,
    title: title,
    gradient: section.getGradient("gradient", theme),
    titleStyle: section.getTextStyle("title_style", theme),
    borderSide: section.getBorderSide("border_side", theme,
        defaultValue: BorderSide.none)!,
    titlePositionPercentageOffset: section.getDouble("title_position"),
    badgeWidget: section.buildWidget("badge"),
    badgePositionPercentageOffset: section.getDouble("badge_position"),
  );
}
