import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:material_ui/material_ui.dart';

import 'charts.dart';

class GaugeChartEventData extends Equatable {
  final String eventType;
  final int? ringIndex;
  final int? zoneIndex;
  final double? value;
  final double? angle;
  final double? radius;
  final bool onValue;

  const GaugeChartEventData({
    required this.eventType,
    this.ringIndex,
    this.zoneIndex,
    this.value,
    this.angle,
    this.radius,
    this.onValue = false,
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
      onValue: touchedRing?.isOnValue ?? false,
    );
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'ring_index': ringIndex,
        'zone_index': zoneIndex,
        'value': value,
        'angle': angle,
        'radius': radius,
        'on_value': onValue,
      };

  @override
  List<Object?> get props =>
      [eventType, ringIndex, zoneIndex, value, angle, radius, onValue];
}

GaugeRing? parseGaugeRing(Control ring, BuildContext context) {
  ring.notifyParent = true;
  final width = ring.getDouble("width");
  switch (ring.type) {
    case "GaugeProgressRing":
      return GaugeProgressRing(
        value: ring.getDouble("value", 0)!,
        color: ring.getColor(
            "color", context, Theme.of(context).colorScheme.primary)!,
        backgroundColor: ring.getColor("bgcolor", context),
        strokeCap:
            parseStrokeCap(ring.getString("stroke_cap"), StrokeCap.butt)!,
        width: width,
      );
    case "GaugeZonesRing":
      return GaugeZonesRing(
        zones: ring.children("zones").map((zone) {
          zone.notifyParent = true;
          return GaugeZone(
            from: zone.getDouble("start", 0)!,
            to: zone.getDouble("end", 0)!,
            color: zone.getColor("color", context, Colors.transparent)!,
            strokeCap:
                parseStrokeCap(zone.getString("stroke_cap"), StrokeCap.butt)!,
          );
        }).toList(),
        zonesSpace: ring.getDouble("zones_space", 0)!,
        width: width,
      );
  }
  return null;
}

/// Python can't pass a label builder, so labels arrive as a list with one entry
/// per tick and each tick's value is mapped back to its index.
GaugeTicks? parseGaugeTicks(
    Control? ticks, double minValue, double maxValue, BuildContext context) {
  if (ticks == null) return null;
  ticks.notifyParent = true;
  final theme = Theme.of(context);
  final defaultColor = theme.colorScheme.onSurface;
  final count = ticks.getInt("count", 3)!;
  final labels = ticks.get<List>("labels")?.map((e) => e.toString()).toList();

  final GaugeTickPainter painter;
  switch (ticks.type) {
    case "GaugeCircleTicks":
      painter = GaugeTickCirclePainter(
        radius: ticks.getDouble("radius", 3)!,
        color: ticks.getColor("color", context, defaultColor)!,
        strokeWidth: ticks.getDouble("stroke_width", 0)!,
        strokeColor: ticks.getColor("stroke_color", context, defaultColor)!,
      );
    default:
      painter = GaugeTickLinePainter(
        length: ticks.getDouble("length", 6)!,
        thickness: ticks.getDouble("thickness", 2)!,
        color: ticks.getColor("color", context, defaultColor)!,
      );
  }

  return GaugeTicks(
    count: count,
    position: parseEnum(GaugeTickPosition.values, ticks.getString("position"),
        GaugeTickPosition.outer)!,
    offset: ticks.getDouble("offset", 0)!,
    painter: painter,
    checkToShowTick: ticks.getBool("show_endpoints", true)!
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
    labelStyle: ticks.getTextStyle("label_style", theme),
    labelOffset: ticks.getDouble("label_offset", 0)!,
  );
}

GaugePointer? parseGaugePointer(Control pointer, BuildContext context) {
  pointer.notifyParent = true;
  final defaultColor = Theme.of(context).colorScheme.onSurface;
  final value = pointer.getDouble("value", 0)!;
  switch (pointer.type) {
    case "GaugeNeedlePointer":
      return GaugePointer(
        value: value,
        painter: GaugePointerNeedlePainter(
          length: pointer.getDouble("length", 60)!,
          width: pointer.getDouble("width", 8)!,
          tailLength: pointer.getDouble("tail_length", 0)!,
          color: pointer.getColor("color", context, defaultColor)!,
        ),
      );
    case "GaugeCirclePointer":
      return GaugePointer(
        value: value,
        painter: GaugePointerCirclePainter(
          radius: pointer.getDouble("radius", 6)!,
          anchorRadius: pointer.getDouble("anchor_radius", 0)!,
          color: pointer.getColor("color", context, defaultColor)!,
          strokeWidth: pointer.getDouble("stroke_width", 0)!,
          strokeColor: pointer.getColor("stroke_color", context, defaultColor)!,
        ),
      );
  }
  return null;
}

/// fl_chart draws a marker label only when it has a style, so a label without
/// one gets small text in the marker's color.
GaugeMarker parseGaugeMarker(Control marker, BuildContext context) {
  marker.notifyParent = true;
  final theme = Theme.of(context);
  final color = marker.getColor("color", context, theme.colorScheme.onSurface)!;

  return GaugeMarker(
    value: marker.getDouble("value", 0)!,
    position: parseEnum(GaugeTickPosition.values, marker.getString("position"),
        GaugeTickPosition.outer)!,
    offset: marker.getDouble("offset", 0)!,
    painter: GaugeMarkerLinePainter(
      length: marker.getDouble("length", 10)!,
      thickness: marker.getDouble("thickness", 2)!,
      color: color,
      strokeCap:
          parseStrokeCap(marker.getString("stroke_cap"), StrokeCap.round)!,
      alignment: parseEnum(GaugeMarkerLineAlignment.values,
          marker.getString("alignment"), GaugeMarkerLineAlignment.centered)!,
      label: marker.getString("label"),
      labelStyle: marker.getTextStyle(
          "label_style", theme, TextStyle(color: color, fontSize: 12)),
      labelOffset: marker.getDouble("label_offset", 6)!,
      labelSide: parseEnum(GaugeMarkerLabelSide.values,
          marker.getString("label_side"), GaugeMarkerLabelSide.outward)!,
    ),
  );
}
