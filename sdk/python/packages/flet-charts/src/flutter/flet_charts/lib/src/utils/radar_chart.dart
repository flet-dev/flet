import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

RadarShape? parseRadarShape(String? value, [RadarShape? defaultValue]) {
  if (value == null) return defaultValue;
  return RadarShape.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

class RadarChartEventData extends Equatable {
  final String eventType;
  final int? dataSetIndex;
  final int? entryIndex;
  final double? entryValue;

  const RadarChartEventData({
    required this.eventType,
    this.dataSetIndex,
    this.entryIndex,
    this.entryValue,
  });

  factory RadarChartEventData.fromDetails(
      FlTouchEvent event, RadarTouchResponse? response) {
    final touchedSpot = response?.touchedSpot;

    return RadarChartEventData(
      eventType: eventMap[event.runtimeType.toString()] ?? "undefined",
      dataSetIndex: touchedSpot?.touchedDataSetIndex,
      entryIndex: touchedSpot?.touchedRadarEntryIndex,
      entryValue: touchedSpot?.touchedRadarEntry.value,
    );
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'data_set_index': dataSetIndex,
        'entry_index': entryIndex,
        'entry_value': entryValue,
      };

  @override
  List<Object?> get props => [eventType, dataSetIndex, entryIndex, entryValue];
}

RadarDataSet parseRadarDataSet(
    Control dataSet, ThemeData theme, BuildContext context) {
  final fillColor = dataSet.getColor("fill_color", context, Colors.cyan)!;
  final fillGradient = dataSet.getGradient("fill_gradient", theme);
  final borderColor = dataSet.getColor("border_color", context, Colors.cyan)!;
  final borderWidth = dataSet.getDouble("border_width", 2.0)!;
  final entryRadius = dataSet.getDouble("entry_radius", 5.0)!;

  final entries = dataSet
      .children("entries")
      .map((entry) => RadarEntry(value: entry.getDouble("value", 0)!))
      .toList();

  return RadarDataSet(
    dataEntries: entries,
    fillColor: fillColor,
    fillGradient: fillGradient,
    borderColor: borderColor,
    borderWidth: borderWidth,
    entryRadius: entryRadius,
  );
}

RadarChartTitle parseRadarChartTitle(
    Control title, ThemeData theme, double defaultAngle) {
  final spansValue = title.get("text_spans");
  final spans = spansValue != null
      ? parseTextSpans(spansValue, theme, (control, eventName, [eventData]) {
          control.triggerEvent(eventName, eventData);
        })
      : null;

  return RadarChartTitle(
    text: title.getString("text", "")!,
    angle: title.getDouble("angle") ?? defaultAngle,
    positionPercentageOffset: title.getDouble("position_percentage_offset"),
    children: spans,
  );
}
