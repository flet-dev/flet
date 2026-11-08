import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';

import 'charts.dart';

GaugeDirection? parseGaugeDirection(String? value,
    [GaugeDirection? defaultValue]) {
  return parseEnum(GaugeDirection.values, value, defaultValue);
}

GaugeTickPosition? parseGaugeTickPosition(String? value,
    [GaugeTickPosition? defaultValue]) {
  return parseEnum(GaugeTickPosition.values, value, defaultValue);
}

GaugeMarkerLineAlignment? parseGaugeMarkerLineAlignment(String? value,
    [GaugeMarkerLineAlignment? defaultValue]) {
  return parseEnum(GaugeMarkerLineAlignment.values, value, defaultValue);
}

GaugeMarkerLabelSide? parseGaugeMarkerLabelSide(String? value,
    [GaugeMarkerLabelSide? defaultValue]) {
  return parseEnum(GaugeMarkerLabelSide.values, value, defaultValue);
}

class GaugeChartEventData extends Equatable {
  final String eventType;
  final int? ringIndex;
  final int? zoneIndex;
  final double? value;
  final double? angle;
  final double? radius;
  final bool isOnValue;

  const GaugeChartEventData({
    required this.eventType,
    this.ringIndex,
    this.zoneIndex,
    this.value,
    this.angle,
    this.radius,
    this.isOnValue = false,
  });

  factory GaugeChartEventData.fromDetails(
      FlTouchEvent event, GaugeTouchResponse? response) {
    final touchedRing = response?.touchedRing;
    final ringIndex = touchedRing?.touchedRingIndex;
    final zoneIndex = touchedRing?.touchedZoneIndex;

    return GaugeChartEventData(
      eventType: resolveFlTouchEventType(event),
      ringIndex: ringIndex == null || ringIndex < 0 ? null : ringIndex,
      zoneIndex: zoneIndex == null || zoneIndex < 0 ? null : zoneIndex,
      value: touchedRing?.touchValue,
      angle: touchedRing?.touchAngle,
      radius: touchedRing?.touchRadius,
      isOnValue: touchedRing?.isOnValue ?? false,
    );
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'ring_index': ringIndex,
        'zone_index': zoneIndex,
        'value': value,
        'angle': angle,
        'radius': radius,
        'is_on_value': isOnValue,
      };

  @override
  List<Object?> get props =>
      [eventType, ringIndex, zoneIndex, value, angle, radius, isOnValue];
}

GaugeRing? parseGaugeRing(dynamic ring, ThemeData theme) {
  if (ring == null) return null;
  final width = parseDouble(ring["width"]);
  switch (ring["_type"]) {
    case "GaugeProgressRing":
      return GaugeProgressRing(
        value: parseDouble(ring["value"], 0)!,
        color: parseColor(ring["color"], theme, theme.colorScheme.primary)!,
        backgroundColor: parseColor(ring["bgcolor"], theme),
        strokeCap: parseStrokeCap(ring["stroke_cap"], StrokeCap.butt)!,
        width: width,
      );
    case "GaugeZonesRing":
      return GaugeZonesRing(
        zones: (ring["zones"] as List? ?? [])
            .map((zone) => GaugeZone(
                  from: parseDouble(zone["start"], 0)!,
                  to: parseDouble(zone["end"], 0)!,
                  color: parseColor(zone["color"], theme, Colors.transparent)!,
                  strokeCap:
                      parseStrokeCap(zone["stroke_cap"], StrokeCap.butt)!,
                ))
            .toList(),
        zonesSpace: parseDouble(ring["zones_space"], 0)!,
        width: width,
      );
  }
  return null;
}

/// Python can't pass a label builder, so labels arrive as a list with one entry
/// per tick and each tick's value is mapped back to its index.
GaugeTicks? parseGaugeTicks(
    dynamic ticks, double minValue, double maxValue, ThemeData theme) {
  if (ticks == null) return null;
  final defaultColor = theme.colorScheme.onSurface;
  final count = parseInt(ticks["count"], 3)!;
  final labels = (ticks["labels"] as List?)?.map((e) => e.toString()).toList();

  final GaugeTickPainter painter;
  switch (ticks["_type"]) {
    case "GaugeCircleTicks":
      painter = GaugeTickCirclePainter(
        radius: parseDouble(ticks["radius"], 3)!,
        color: parseColor(ticks["color"], theme, defaultColor)!,
        strokeWidth: parseDouble(ticks["stroke_width"], 0)!,
        strokeColor: parseColor(ticks["stroke_color"], theme, defaultColor)!,
      );
    default:
      painter = GaugeTickLinePainter(
        length: parseDouble(ticks["length"], 6)!,
        thickness: parseDouble(ticks["thickness"], 2)!,
        color: parseColor(ticks["color"], theme, defaultColor)!,
      );
  }

  return GaugeTicks(
    count: count,
    position:
        parseGaugeTickPosition(ticks["position"], GaugeTickPosition.outer)!,
    offset: parseDouble(ticks["offset"], 0)!,
    painter: painter,
    checkToShowTick: parseBool(ticks["show_endpoints"], true)!
        ? GaugeTicks.showAll
        : GaugeTicks.hideEndpoints,
    labelBuilder: labels == null
        ? null
        : (value) {
            final index =
                ((value - minValue) / (maxValue - minValue) * (count - 1))
                    .round();
            return index >= 0 && index < labels.length ? labels[index] : "";
          },
    labelStyle: parseTextStyle(ticks["label_style"], theme),
    labelOffset: parseDouble(ticks["label_offset"], 0)!,
  );
}

GaugePointer? parseGaugePointer(dynamic pointer, ThemeData theme) {
  if (pointer == null) return null;
  final defaultColor = theme.colorScheme.onSurface;
  final value = parseDouble(pointer["value"], 0)!;
  switch (pointer["_type"]) {
    case "GaugeNeedlePointer":
      return GaugePointer(
        value: value,
        painter: GaugePointerNeedlePainter(
          length: parseDouble(pointer["length"], 60)!,
          width: parseDouble(pointer["width"], 8)!,
          tailLength: parseDouble(pointer["tail_length"], 0)!,
          color: parseColor(pointer["color"], theme, defaultColor)!,
        ),
      );
    case "GaugeCirclePointer":
      return GaugePointer(
        value: value,
        painter: GaugePointerCirclePainter(
          radius: parseDouble(pointer["radius"], 6)!,
          anchorRadius: parseDouble(pointer["anchor_radius"], 0)!,
          color: parseColor(pointer["color"], theme, defaultColor)!,
          strokeWidth: parseDouble(pointer["stroke_width"], 0)!,
          strokeColor:
              parseColor(pointer["stroke_color"], theme, defaultColor)!,
        ),
      );
  }
  return null;
}

/// fl_chart draws a marker label only when it has a style, so a label without
/// one gets small text in the marker's color.
GaugeMarker? parseGaugeMarker(dynamic marker, ThemeData theme) {
  if (marker == null) return null;
  final color =
      parseColor(marker["color"], theme, theme.colorScheme.onSurface)!;

  return GaugeMarker(
    value: parseDouble(marker["value"], 0)!,
    position:
        parseGaugeTickPosition(marker["position"], GaugeTickPosition.outer)!,
    offset: parseDouble(marker["offset"], 0)!,
    painter: GaugeMarkerLinePainter(
      length: parseDouble(marker["length"], 10)!,
      thickness: parseDouble(marker["thickness"], 2)!,
      color: color,
      strokeCap: parseStrokeCap(marker["stroke_cap"], StrokeCap.round)!,
      alignment: parseGaugeMarkerLineAlignment(
          marker["alignment"], GaugeMarkerLineAlignment.centered)!,
      label: marker["label"],
      labelStyle: parseTextStyle(
          marker["label_style"], theme, TextStyle(color: color, fontSize: 12)),
      labelOffset: parseDouble(marker["label_offset"], 6)!,
      labelSide: parseGaugeMarkerLabelSide(
          marker["label_side"], GaugeMarkerLabelSide.outward)!,
    ),
  );
}
