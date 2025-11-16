import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

class ScatterChartEventData extends Equatable {
  final String eventType;
  final int? spotIndex;

  const ScatterChartEventData({required this.eventType, this.spotIndex});

  factory ScatterChartEventData.fromDetails(
      FlTouchEvent event, ScatterTouchResponse? response) {
    return ScatterChartEventData(
        eventType: resolveFlTouchEventType(event),
        spotIndex: response?.touchedSpot?.spotIndex);
  }

  Map<String, dynamic> toMap() => {'type': eventType, 'spot_index': spotIndex};

  @override
  List<Object?> get props => [eventType, spotIndex];
}

ScatterTouchTooltipData parseScatterTouchTooltipData(
    BuildContext context, Control control, List<ScatterSpot> spots) {
  var tooltip = control.get("tooltip") ?? {};

  final theme = Theme.of(context);

  return ScatterTouchTooltipData(
    tooltipBorder: parseBorderSide(tooltip["border_side"], theme,
        defaultValue: BorderSide.none)!,
    rotateAngle: parseDouble(tooltip["rotation"], 0.0)!,
    maxContentWidth: parseDouble(tooltip["max_width"], 120)!,
    tooltipPadding: parsePadding(tooltip["padding"],
        const EdgeInsets.symmetric(horizontal: 16, vertical: 8))!,
    tooltipHorizontalAlignment: parseFLHorizontalAlignment(
        tooltip["horizontal_alignment"], FLHorizontalAlignment.center)!,
    tooltipHorizontalOffset: parseDouble(tooltip["horizontal_offset"], 0),
    tooltipBorderRadius: parseBorderRadius(tooltip["border_radius"]),
    fitInsideHorizontally:
        parseBool(tooltip["fit_inside_horizontally"], false)!,
    fitInsideVertically: parseBool(tooltip["fit_inside_vertically"], false)!,
    getTooltipColor: (ScatterSpot touchedSpot) {
      return parseColor(
          tooltip["bgcolor"], theme, const Color.fromRGBO(96, 125, 139, 1))!;
    },
    getTooltipItems: (ScatterSpot touchedSpot) {
      var spotIndex = spots.indexWhere(
          (spot) => spot.x == touchedSpot.x && spot.y == touchedSpot.y);
      return parseScatterTooltipItem(
          control.children("spots")[spotIndex], touchedSpot, context);
    },
  );
}

ScatterTooltipItem? parseScatterTooltipItem(
    Control dataPoint, ScatterSpot spot, BuildContext context) {
  if (!dataPoint.getBool("show_tooltip", true)!) return null;

  var tooltip = dataPoint.internals?["tooltip"];
  if (tooltip == null) return null;

  final theme = Theme.of(context);
  var style = parseTextStyle(tooltip["text_style"], theme, const TextStyle())!;
  if (style.color == null) {
    style = style.copyWith(color: spot.dotPainter.mainColor);
  }
  return ScatterTooltipItem(
      tooltip["text"] ?? dataPoint.getDouble("y").toString(),
      textStyle: style,
      textAlign: parseTextAlign(tooltip["text_align"], TextAlign.center)!,
      textDirection: parseBool(tooltip["rtl"], false)!
          ? TextDirection.rtl
          : TextDirection.ltr,
      bottomMargin: parseDouble(tooltip["bottom_margin"]),
      children: tooltip["text_spans"] != null
          ? parseTextSpans(tooltip["text_spans"], theme, (s, eventName,
              [eventData]) {
              s.triggerEvent(eventName, eventData);
            })
          : null);
}
