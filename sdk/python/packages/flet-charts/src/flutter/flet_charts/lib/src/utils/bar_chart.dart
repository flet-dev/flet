import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/flet.dart';
import 'package:flutter/material.dart';

import 'charts.dart';

class BarChartEventData extends Equatable {
  final String eventType;
  final int? groupIndex;
  final int? rodIndex;
  final int? stackItemIndex;

  const BarChartEventData({
    required this.eventType,
    required this.groupIndex,
    required this.rodIndex,
    required this.stackItemIndex,
  });

  factory BarChartEventData.fromDetails(
    FlTouchEvent event,
    BarTouchResponse? response,
  ) {
    return BarChartEventData(
      eventType: resolveFlTouchEventType(event),
      groupIndex: response != null && response.spot != null
          ? response.spot!.touchedBarGroupIndex
          : null,
      rodIndex: response != null && response.spot != null
          ? response.spot!.touchedRodDataIndex
          : null,
      stackItemIndex: response != null && response.spot != null
          ? response.spot!.touchedStackItemIndex
          : null,
    );
  }

  Map<String, dynamic> toMap() => <String, dynamic>{
        'type': eventType,
        'group_index': groupIndex,
        'rod_index': rodIndex,
        'stack_item_index': stackItemIndex,
      };

  @override
  List<Object?> get props => [eventType, groupIndex, rodIndex, stackItemIndex];
}

TooltipDirection? parseTooltipDirection(
  String? value, [
  TooltipDirection? defaultValue,
]) {
  if (value == null) return defaultValue;
  return TooltipDirection.values.firstWhereOrNull(
        (e) => e.name.toLowerCase() == value.toLowerCase(),
      ) ??
      defaultValue;
}

BarTouchTooltipData? parseBarTouchTooltipData(
  BuildContext context,
  Control control, [
  BarTouchTooltipData? defaultValue,
]) {
  var tooltip = control.get("tooltip");
  if (tooltip == null) return defaultValue;

  final theme = Theme.of(context);

  return BarTouchTooltipData(
    getTooltipColor: (BarChartGroupData group) =>
        parseColor(tooltip["bgcolor"], theme, theme.colorScheme.secondary)!,
    tooltipBorderRadius: parseBorderRadius(tooltip["border_radius"]),
    tooltipMargin: parseDouble(tooltip["margin"], 16)!,
    tooltipPadding: parsePadding(
      tooltip["padding"],
      const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
    )!,
    maxContentWidth: parseDouble(tooltip["max_width"]),
    rotateAngle: parseDouble(tooltip["rotation"], 0.0)!,
    tooltipHorizontalOffset: parseDouble(tooltip["horizontal_offset"], 0)!,
    tooltipBorder: parseBorderSide(tooltip["border_side"], theme),
    fitInsideHorizontally: parseBool(
      tooltip["fit_inside_horizontally"],
      false,
    )!,
    fitInsideVertically: parseBool(tooltip["fit_inside_vertically"], false)!,
    direction: parseTooltipDirection(
      tooltip["direction"],
      TooltipDirection.auto,
    )!,
    tooltipHorizontalAlignment: parseFLHorizontalAlignment(
      tooltip["horizontal_alignment"],
      FLHorizontalAlignment.center,
    )!,
    getTooltipItem: (group, groupIndex, rod, rodIndex) {
      var rod =
          control.children("groups")[groupIndex].children("rods")[rodIndex];
      return parseBarTooltipItem(rod, context);
    },
  );
}

BarTooltipItem? parseBarTooltipItem(Control rod, BuildContext context) {
  if (!rod.getBool("show_tooltip", true)!) return null;

  var tooltip = rod.internals?["tooltip"];
  if (tooltip == null) return null;

  final theme = Theme.of(context);
  var tooltipTextStyle = parseTextStyle(
    tooltip["text_style"],
    theme,
    const TextStyle(),
  )!;
  if (tooltipTextStyle.color == null) {
    tooltipTextStyle = tooltipTextStyle.copyWith(
      color: rod.getGradient("gradient", theme)?.colors.first ??
          rod.getColor("color", context, Colors.blueGrey)!,
    );
  }
  return BarTooltipItem(
    tooltip["text"] ?? rod.getDouble("to_y", 0)!.toString(),
    tooltipTextStyle,
    textAlign: parseTextAlign(tooltip["text_align"], TextAlign.center)!,
    textDirection: parseBool(tooltip["rtl"], false)!
        ? TextDirection.rtl
        : TextDirection.ltr,
    children: tooltip["text_spans"] != null
        ? parseTextSpans(tooltip["text_spans"], theme, (
            s,
            eventName, [
            eventData,
          ]) {
            s.triggerEvent(eventName, eventData);
          })
        : null,
  );
}

BarChartGroupData parseBarChartGroupData(
  Control group,
  bool interactiveChart,
  BuildContext context,
) {
  group.notifyParent = true;
  return BarChartGroupData(
    x: group.getInt("x", 0)!,
    barsSpace: group.getDouble("spacing"),
    groupVertically: group.getBool("group_vertically", false)!,
    showingTooltipIndicators: group
        .children("rods")
        .asMap()
        .entries
        .where(
          (rod) => !interactiveChart && rod.value.getBool("selected", false)!,
        )
        .map((rod) => rod.key)
        .toList(),
    barRods: group
        .children("rods")
        .map((rod) => parseBarChartRodData(rod, interactiveChart, context))
        .toList(),
  );
}

BarChartRodData parseBarChartRodData(
  Control rod,
  bool interactiveChart,
  BuildContext context,
) {
  rod.notifyParent = true;

  final theme = Theme.of(context);
  var bgFromY = rod.getDouble("bg_from_y");
  var bgToY = rod.getDouble("bg_to_y");
  var bgcolor = rod.getColor("bgcolor", context);
  var backgroundGradient = rod.getGradient("background_gradient", theme);

  return BarChartRodData(
    fromY: rod.getDouble("from_y"),
    toY: rod.getDouble("to_y", 0)!,
    width: rod.getDouble("width"),
    color: rod.getColor("color", context),
    gradient: rod.getGradient("gradient", theme),
    borderRadius: rod.getBorderRadius("border_radius"),
    borderSide: rod.getBorderSide(
      "border_side",
      theme,
      defaultValue: BorderSide.none,
    ),
    backDrawRodData: BackgroundBarChartRodData(
      show: (bgFromY != null ||
          bgToY != null ||
          bgcolor != null ||
          backgroundGradient != null),
      fromY: bgFromY,
      toY: bgToY,
      color: bgcolor,
      gradient: backgroundGradient,
    ),
    rodStackItems: rod
        .children("stack_items")
        .map(
          (rodStackItem) => parseBarChartRodStackItem(
            rodStackItem,
            interactiveChart,
            context,
          ),
        )
        .toList(),
  );
}

BarChartRodStackItem parseBarChartRodStackItem(
  Control rodStackItem,
  bool interactiveChart,
  BuildContext context,
) {
  rodStackItem.notifyParent = true;
  return BarChartRodStackItem(
    rodStackItem.getDouble("from_y")!,
    rodStackItem.getDouble("to_y", 0)!,
    rodStackItem.getColor("color", context)!,
    borderSide: rodStackItem.getBorderSide(
      "border_side",
      Theme.of(context),
      defaultValue: BorderSide.none,
    )!,
  );
}

BarChartAlignment? parseBarChartAlignment(String? value,
    [BarChartAlignment? defaultValue]) {
  if (value == null) return defaultValue;
  return BarChartAlignment.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}
