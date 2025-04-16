import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/src/extensions/control.dart';
import 'package:flet/src/utils/colors.dart';
import 'package:flet/src/utils/numbers.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/charts.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/text.dart';
import 'base_controls.dart';

TooltipDirection? parseTooltipDirection(String? value,
    [TooltipDirection? defaultValue]) {
  if (value == null) {
    return defaultValue;
  }
  return TooltipDirection.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

class BarChartEventData extends Equatable {
  final String eventType;
  final int? groupIndex;
  final int? rodIndex;
  final int? stackItemIndex;

  const BarChartEventData(
      {required this.eventType,
      required this.groupIndex,
      required this.rodIndex,
      required this.stackItemIndex});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'type': eventType,
        'group_index': groupIndex,
        'rod_index': rodIndex,
        'stack_item_index': stackItemIndex
      };

  @override
  List<Object?> get props => [eventType, groupIndex, rodIndex, stackItemIndex];
}

class BarChartControl extends StatefulWidget {
  final Control control;

  const BarChartControl({super.key, required this.control});

  @override
  State<BarChartControl> createState() => _BarChartControlState();
}

class _BarChartControlState extends State<BarChartControl> {
  BarChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("BarChart build: ${widget.control.id}");

    var animate = widget.control.getAnimation("animate");
    var border = widget.control.getBorder("border", Theme.of(context));

    var leftTitles = getAxisTitles(widget.control.child("left_axis"));
    var topTitles = getAxisTitles(widget.control.child("top_axis"));
    var rightTitles = getAxisTitles(widget.control.child("right_axis"));
    var bottomTitles = getAxisTitles(widget.control.child("bottom_axis"));

    var interactive = widget.control.getBool("interactive", true)!;

    List<BarChartGroupData> barGroups = widget.control
        .children("bar_groups")
        .map((group) => getGroupData(group, interactive, Theme.of(context)))
        .toList();

    var chart = BarChart(
      BarChartData(
        backgroundColor: widget.control.getColor("bgcolor", context),
        minY: widget.control.getDouble("min_y"),
        maxY: widget.control.getDouble("max_y"),
        baselineY: widget.control.getDouble("baseline_y"),
        titlesData: (leftTitles.sideTitles.showTitles ||
                topTitles.sideTitles.showTitles ||
                rightTitles.sideTitles.showTitles ||
                bottomTitles.sideTitles.showTitles)
            ? FlTitlesData(
                show: true,
                leftTitles: leftTitles,
                topTitles: topTitles,
                rightTitles: rightTitles,
                bottomTitles: bottomTitles,
              )
            : const FlTitlesData(show: false),
        borderData: border != null
            ? FlBorderData(show: true, border: border)
            : FlBorderData(show: false),
        gridData: parseChartGridData(Theme.of(context), widget.control,
            "horizontal_grid_lines", "vertical_grid_lines"),
        groupsSpace: widget.control.getDouble("groups_space"),
        barTouchData: BarTouchData(
          enabled: interactive,
          touchTooltipData: BarTouchTooltipData(
            getTooltipColor: (BarChartGroupData group) => widget.control
                .getColor("tooltip_bgcolor", context,
                    Theme.of(context).colorScheme.secondary)!,
            tooltipRoundedRadius:
                widget.control.getDouble("tooltip_rounded_radius"),
            tooltipMargin: widget.control.getDouble("tooltip_margin"),
            tooltipPadding: widget.control.getPadding("tooltip_padding"),
            maxContentWidth: widget.control.getDouble("tooltip_max_width"),
            rotateAngle: widget.control.getDouble("tooltip_rotate_angle"),
            tooltipHorizontalOffset:
                widget.control.getDouble("tooltip_horizontal_offset"),
            tooltipBorder: widget.control
                .getBorderSide("tooltip_border_side", Theme.of(context)),
            fitInsideHorizontally:
                widget.control.getBool("tooltip_fit_inside_horizontally"),
            fitInsideVertically:
                widget.control.getBool("tooltip_fit_inside_vertically"),
            direction: parseTooltipDirection(
                widget.control.getString("tooltip_direction")),
            getTooltipItem: (group, groupIndex, rod, rodIndex) {
              var rod = widget.control
                  .children("bar_groups")[groupIndex]
                  .children("bar_rods")[rodIndex];

              var tooltip = rod.getString(
                  "tooltip", rod.getDouble("to_y", 0)!.toString())!;
              var tooltipStyle =
                  rod.getTextStyle("tooltip_style", Theme.of(context));
              tooltipStyle ??= const TextStyle();
              if (tooltipStyle.color == null) {
                tooltipStyle = tooltipStyle.copyWith(
                    color: rod
                            .getGradient("gradient", Theme.of(context))
                            ?.colors
                            .first ??
                        rod.getColor("color", context) ??
                        Colors.blueGrey);
              }
              TextAlign? tooltipAlign =
                  rod.getTextAlign("tooltip_align", TextAlign.center)!;
              return rod.getBool("show_tooltip", true)!
                  ? BarTooltipItem(tooltip, tooltipStyle,
                      textAlign: tooltipAlign)
                  : null;
            },
          ),
          touchCallback: widget.control.getBool("on_chart_event", false)!
              ? (evt, resp) {
                  var eventData = resp != null && resp.spot != null
                      ? BarChartEventData(
                          eventType: evt.runtimeType
                              .toString()
                              .substring(2), // remove "Fl"
                          groupIndex: resp.spot!.touchedBarGroupIndex,
                          rodIndex: resp.spot!.touchedRodDataIndex,
                          stackItemIndex: resp.spot!.touchedStackItemIndex)
                      : BarChartEventData(
                          eventType: evt.runtimeType
                              .toString()
                              .substring(2), // remove "Fl"
                          groupIndex: null,
                          rodIndex: null,
                          stackItemIndex: null);
                  if (eventData != _eventData) {
                    _eventData = eventData;
                    debugPrint(
                        "BarChart ${widget.control.id} ${eventData.eventType}");
                    widget.control
                        .triggerEvent("chart_event", eventData.toJson());
                  }
                }
              : null,
        ),
        barGroups: barGroups,
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

  BarChartGroupData getGroupData(
      Control group, bool interactiveChart, ThemeData theme) {
    group.notifyParent = true;
    return BarChartGroupData(
      x: group.getInt("x", 0)!,
      barsSpace: group.getDouble("bars_space"),
      groupVertically: group.getBool("group_vertically"),
      showingTooltipIndicators: group
          .children("bar_rods")
          .asMap()
          .entries
          .where(
              (e) => !interactiveChart && e.value.getBool("selected", false)!)
          .map((e) => e.key)
          .toList(),
      barRods: group
          .children("bar_rods")
          .map((rod) => getRodData(rod, interactiveChart, theme))
          .toList(),
    );
  }

  BarChartRodData getRodData(
      Control rod, bool interactiveChart, ThemeData theme) {
    rod.notifyParent = true;

    var bgFromY = rod.getDouble("bg_from_y");
    var bgToY = rod.getDouble("bg_to_y");
    var bgColor = rod.getColor("bg_color", context);
    var bgGradient = rod.getGradient("bg_gradient", theme);

    return BarChartRodData(
        fromY: rod.getDouble("from_y"),
        toY: rod.getDouble("to_y", 0)!,
        width: rod.getDouble("width"),
        color: rod.getColor("color", context),
        gradient: rod.getGradient("gradient", theme),
        borderRadius: rod.getBorderRadius("border_radius"),
        borderSide: rod.getBorderSide("border_side", theme,
            defaultValue: BorderSide.none),
        backDrawRodData: bgFromY != null ||
                bgToY != null ||
                bgColor != null ||
                bgGradient != null
            ? BackgroundBarChartRodData(
                show: true,
                fromY: bgFromY,
                toY: bgToY,
                color: bgColor,
                gradient: bgGradient)
            : null,
        rodStackItems: rod
            .children("rod_stack_items")
            .map((rodStackItem) =>
                getRodStackItem(rodStackItem, interactiveChart, theme))
            .toList());
  }

  BarChartRodStackItem getRodStackItem(
    Control rodStackItem,
    bool interactiveChart,
    ThemeData theme,
  ) {
    rodStackItem.notifyParent = true;
    return BarChartRodStackItem(
        rodStackItem.getDouble("from_y")!,
        rodStackItem.getDouble("to_y", 0)!,
        rodStackItem.getColor("color", context)!,
        rodStackItem.getBorderSide("border_side", theme) ?? BorderSide.none);
  }

  AxisTitles getAxisTitles(Control? axis) {
    if (axis == null) {
      return const AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axis.buildWidget("title"),
        axisNameSize: axis.getDouble("title_size") ?? 16,
        sideTitles: SideTitles(
          showTitles: axis.getBool("show_labels", true)!,
          reservedSize: axis.getDouble("labels_size") ?? 22,
          interval: axis.getDouble("labels_interval"),
          getTitlesWidget: axis.children("labels").isEmpty
              ? defaultGetTitle
              : (value, meta) {
                  var label = axis
                      .children("labels")
                      .firstWhereOrNull((l) => l.getDouble("value") == value);
                  return label?.buildWidget("label") ?? const SizedBox.shrink();
                },
        ));
  }
}
