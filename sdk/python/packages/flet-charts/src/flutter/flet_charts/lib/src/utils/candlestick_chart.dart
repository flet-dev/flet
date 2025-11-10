import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

class CandlestickChartEventData extends Equatable {
  final String eventType;
  final int? spotIndex;

  const CandlestickChartEventData({
    required this.eventType,
    required this.spotIndex,
  });

  factory CandlestickChartEventData.fromDetails(
    FlTouchEvent event,
    CandlestickTouchResponse? response,
  ) {
    return CandlestickChartEventData(
      eventType: resolveFlTouchEventType(event),
      spotIndex: response?.touchedSpot?.spotIndex,
    );
  }

  Map<String, dynamic> toMap() => {
        "type": eventType,
        "spot_index": spotIndex,
      };

  @override
  List<Object?> get props => [eventType, spotIndex];
}

CandlestickTouchTooltipData parseCandlestickTouchTooltipData(
    BuildContext context, Control control, List<Control> spotControls) {
  final tooltip = control.get("tooltip") ?? {};
  final theme = Theme.of(context);

  return CandlestickTouchTooltipData(
    tooltipBorder: parseBorderSide(tooltip["border_side"], theme,
        defaultValue: BorderSide.none)!,
    rotateAngle: parseDouble(tooltip["rotation"], 0.0)!,
    tooltipBorderRadius:
        parseBorderRadius(tooltip["border_radius"], BorderRadius.circular(4))!,
    tooltipPadding: parsePadding(tooltip["padding"],
        const EdgeInsets.symmetric(horizontal: 16, vertical: 8))!,
    tooltipHorizontalAlignment: parseFLHorizontalAlignment(
        tooltip["horizontal_alignment"], FLHorizontalAlignment.center)!,
    tooltipHorizontalOffset: parseDouble(tooltip["horizontal_offset"], 0)!,
    maxContentWidth: parseDouble(tooltip["max_width"], 120)!,
    fitInsideHorizontally:
        parseBool(tooltip["fit_inside_horizontally"], false)!,
    fitInsideVertically: parseBool(tooltip["fit_inside_vertically"], false)!,
    showOnTopOfTheChartBoxArea:
        parseBool(tooltip["show_on_top_of_chart_box_area"], false)!,
    getTooltipColor: (spot) =>
        parseColor(tooltip["bgcolor"], theme, const Color(0xFFFFECEF))!,
    getTooltipItems: (painter, touchedSpot, spotIndex) {
      if (spotIndex < 0 || spotIndex >= spotControls.length) {
        return null;
      }
      return parseCandlestickTooltipItem(
        spotControls[spotIndex],
        painter,
        touchedSpot,
        spotIndex,
        context,
      );
    },
  );
}

CandlestickTooltipItem? parseCandlestickTooltipItem(
  Control spotControl,
  FlCandlestickPainter painter,
  CandlestickSpot touchedSpot,
  int spotIndex,
  BuildContext context,
) {
  if (!spotControl.getBool("show_tooltip", true)!) {
    return null;
  }

  final tooltip = spotControl.internals?["tooltip"];
  if (tooltip == null) {
    return null;
  }

  final theme = Theme.of(context);
  var textStyle =
      parseTextStyle(tooltip["text_style"], theme, const TextStyle())!;
  if (textStyle.color == null) {
    textStyle = textStyle.copyWith(
      color: painter.getMainColor(
        spot: touchedSpot,
        spotIndex: spotIndex,
      ),
    );
  }

  return CandlestickTooltipItem(
    tooltip["text"] ?? "",
    textStyle: textStyle,
    bottomMargin: parseDouble(tooltip["bottom_margin"], 8)!,
    textAlign: parseTextAlign(tooltip["text_align"], TextAlign.center)!,
    textDirection: parseBool(tooltip["rtl"], false)!
        ? TextDirection.rtl
        : TextDirection.ltr,
    children: tooltip["text_spans"] != null
        ? parseTextSpans(tooltip["text_spans"], theme, (s, eventName,
            [eventData]) {
            s.triggerEvent(eventName, eventData);
          })
        : null,
  );
}
