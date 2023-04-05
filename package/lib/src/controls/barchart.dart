import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/barchart_event_data.dart';
import '../models/barchart_group_view_model.dart';
import '../models/barchart_rod_stack_item_view_model.dart';
import '../models/barchart_rod_view_model.dart';
import '../models/barchart_view_model.dart';
import '../models/chart_axis_view_model.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/charts.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/text.dart';
import 'create_control.dart';

class BarChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const BarChartControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<BarChartControl> createState() => _BarChartControlState();
}

class _BarChartControlState extends State<BarChartControl> {
  BarChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("BarChart build: ${widget.control.id}");

    var animate = parseAnimation(widget.control, "animate");
    var border = parseBorder(Theme.of(context), widget.control, "border");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var result = StoreConnector<AppState, BarChartViewModel>(
        distinct: true,
        converter: (store) =>
            BarChartViewModel.fromStore(store, widget.control, widget.children),
        builder: (context, viewModel) {
          var leftTitles =
              getAxisTitles(widget.control, viewModel.leftAxis, disabled);
          var topTitles =
              getAxisTitles(widget.control, viewModel.topAxis, disabled);
          var rightTitles =
              getAxisTitles(widget.control, viewModel.rightAxis, disabled);
          var bottomTitles =
              getAxisTitles(widget.control, viewModel.bottomAxis, disabled);

          var interactive = viewModel.control.attrBool("interactive", true)!;

          List<BarChartGroupData> barGroups = viewModel.barGroups
              .map((g) => getGroupData(
                  Theme.of(context), widget.control, interactive, g))
              .toList();

          var chart = BarChart(
            BarChartData(
              backgroundColor: HexColor.fromString(
                  Theme.of(context), widget.control.attrString("bgcolor", "")!),
              minY: widget.control.attrDouble("miny"),
              maxY: widget.control.attrDouble("maxy"),
              baselineY: widget.control.attrDouble("baseliney"),
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
                  : FlTitlesData(show: false),
              borderData: border != null
                  ? FlBorderData(show: true, border: border)
                  : FlBorderData(show: false),
              gridData: parseChartGridData(Theme.of(context), widget.control,
                  "horizontalGridLines", "verticalGridLines"),
              groupsSpace: widget.control.attrDouble("groupsSpace"),
              barTouchData: BarTouchData(
                enabled: interactive,
                touchTooltipData: BarTouchTooltipData(
                  tooltipBgColor: HexColor.fromString(Theme.of(context),
                      widget.control.attrString("tooltipBgcolor", "")!),
                  getTooltipItem: (group, groupIndex, rod, rodIndex) {
                    var dp = viewModel.barGroups[groupIndex].barRods[rodIndex];

                    var tooltip = dp.control.attrString("tooltip") ??
                        dp.control.attrDouble("toY", 0)!.toString();
                    var tooltipStyle = parseTextStyle(
                        Theme.of(context), dp.control, "tooltipStyle");
                    tooltipStyle ??= const TextStyle();
                    if (tooltipStyle.color == null) {
                      tooltipStyle = tooltipStyle.copyWith(
                          color: rod.gradient?.colors.first ??
                              rod.color ??
                              Colors.blueGrey);
                    }
                    TextAlign? tooltipAlign = TextAlign.values.firstWhereOrNull(
                        (a) =>
                            a.name.toLowerCase() ==
                            dp.control
                                .attrString("tooltipAlign", "")!
                                .toLowerCase());
                    return dp.control.attrBool("showTooltip", true)!
                        ? BarTooltipItem(tooltip, tooltipStyle,
                            textAlign: tooltipAlign ?? TextAlign.center)
                        : null;
                  },
                ),
                touchCallback: widget.control.attrBool("onChartEvent", false)!
                    ? (evt, resp) {
                        var eventData = resp != null && resp.spot != null
                            ? BarChartEventData(
                                eventType: evt.runtimeType
                                    .toString()
                                    .substring(2), // remove "Fl"
                                groupIndex: resp.spot!.touchedBarGroupIndex,
                                rodIndex: resp.spot!.touchedRodDataIndex,
                                stackItemIndex:
                                    resp.spot!.touchedStackItemIndex)
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
                          FletAppServices.of(context).server.sendPageEvent(
                              eventTarget: widget.control.id,
                              eventName: "chart_event",
                              eventData: json.encode(eventData));
                        }
                      }
                    : null,
              ),
              barGroups: barGroups,
            ),
            swapAnimationDuration: animate != null
                ? animate.duration
                : const Duration(milliseconds: 150), // Optional
            swapAnimationCurve: animate != null ? animate.curve : Curves.linear,
          );

          return LayoutBuilder(
              builder: (BuildContext context, BoxConstraints constraints) {
            return (constraints.maxHeight == double.infinity)
                ? ConstrainedBox(
                    constraints: const BoxConstraints(maxHeight: 300),
                    child: chart,
                  )
                : chart;
          });
        });

    return constrainedControl(context, result, widget.parent, widget.control);
  }

  BarChartGroupData getGroupData(ThemeData theme, Control parent,
      bool interactiveChart, BarChartGroupViewModel groupViewModel) {
    return BarChartGroupData(
      x: groupViewModel.control.attrInt("x", 0)!,
      barsSpace: groupViewModel.control.attrDouble("barsSpace"),
      groupVertically: groupViewModel.control.attrBool("groupVertically"),
      showingTooltipIndicators: groupViewModel.barRods
          .asMap()
          .entries
          .where((e) =>
              !interactiveChart && e.value.control.attrBool("selected", false)!)
          .map((e) => e.key)
          .toList(),
      barRods: groupViewModel.barRods
          .map((r) =>
              getRodData(theme, groupViewModel.control, interactiveChart, r))
          .toList(),
    );
  }

  BarChartRodData getRodData(ThemeData theme, Control parent,
      bool interactiveChart, BarChartRodViewModel rodViewModel) {
    var bgFromY = rodViewModel.control.attrDouble("bgFromY");
    var bgToY = rodViewModel.control.attrDouble("bgToY");
    var bgColor = HexColor.fromString(
        theme, rodViewModel.control.attrString("bgColor", "")!);
    var bgGradient = parseGradient(theme, rodViewModel.control, "bgGradient");

    return BarChartRodData(
        fromY: rodViewModel.control.attrDouble("fromY"),
        toY: rodViewModel.control.attrDouble("toY", 0)!,
        width: rodViewModel.control.attrDouble("width"),
        color: HexColor.fromString(
            theme, rodViewModel.control.attrString("color", "")!),
        gradient: parseGradient(theme, rodViewModel.control, "gradient"),
        borderRadius: parseBorderRadius(rodViewModel.control, "borderRadius"),
        borderSide: parseBorderSide(theme, rodViewModel.control, "borderSide"),
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
        rodStackItems: rodViewModel.rodStackItems
            .map((item) => getRodStackItem(
                theme, rodViewModel.control, interactiveChart, item))
            .toList());
  }

  BarChartRodStackItem getRodStackItem(ThemeData theme, Control parent,
      bool interactiveChart, BarChartRodStackItemViewModel stackItemViewModel) {
    return BarChartRodStackItem(
        stackItemViewModel.control.attrDouble("fromY")!,
        stackItemViewModel.control.attrDouble("toY", 0)!,
        HexColor.fromString(
            theme, stackItemViewModel.control.attrString("color", "")!)!,
        parseBorderSide(theme, stackItemViewModel.control, "borderSide"));
  }

  AxisTitles getAxisTitles(
      Control parent, ChartAxisViewModel? axisViewModel, bool disabled) {
    if (axisViewModel == null) {
      return AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axisViewModel.title != null
            ? createControl(parent, axisViewModel.title!.id, disabled)
            : null,
        axisNameSize: axisViewModel.control.attrDouble("titleSize"),
        sideTitles: SideTitles(
          showTitles: axisViewModel.control.attrBool("showLabels", true),
          reservedSize: axisViewModel.control.attrDouble("labelsSize"),
          interval: axisViewModel.control.attrDouble("labelsInterval"),
          getTitlesWidget: axisViewModel.labels.isEmpty
              ? null
              : (value, meta) {
                  return axisViewModel.labels.containsKey(value)
                      ? createControl(
                          parent, axisViewModel.labels[value]!.id, disabled)
                      : const SizedBox.shrink();
                },
        ));
  }
}
