import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:equatable/equatable.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';
import 'package:redux/redux.dart';

import '../flet_control_backend.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/charts.dart';
import '../utils/edge_insets.dart';
import '../utils/gradient.dart';
import '../utils/text.dart';
import 'charts.dart';
import 'create_control.dart';

TooltipDirection? parseTooltipDirection(String? value,
    [TooltipDirection? defValue]) {
  if (value == null) {
    return defValue;
  }
  return TooltipDirection.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
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

class BarChartGroupViewModel extends Equatable {
  final Control control;
  final List<BarChartRodViewModel> barRods;

  const BarChartGroupViewModel({required this.control, required this.barRods});

  static BarChartGroupViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartGroupViewModel(
        control: control,
        barRods: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .nonNulls
            .where((c) => c.visible)
            .map((c) => BarChartRodViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, barRods];
}

class BarChartRodStackItemViewModel extends Equatable {
  final Control control;

  const BarChartRodStackItemViewModel({required this.control});

  static BarChartRodStackItemViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartRodStackItemViewModel(control: control);
  }

  @override
  List<Object?> get props => [control];
}

class BarChartRodViewModel extends Equatable {
  final Control control;
  final List<BarChartRodStackItemViewModel> rodStackItems;

  const BarChartRodViewModel(
      {required this.control, required this.rodStackItems});

  static BarChartRodViewModel fromStore(
      Store<AppState> store, Control control) {
    return BarChartRodViewModel(
        control: control,
        rodStackItems: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .nonNulls
            .where((c) => c.visible)
            .map((c) => BarChartRodStackItemViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, rodStackItems];
}

class BarChartViewModel extends Equatable {
  final Control control;
  final ChartAxisViewModel? leftAxis;
  final ChartAxisViewModel? topAxis;
  final ChartAxisViewModel? rightAxis;
  final ChartAxisViewModel? bottomAxis;
  final List<BarChartGroupViewModel> barGroups;

  const BarChartViewModel(
      {required this.control,
      required this.leftAxis,
      required this.topAxis,
      required this.rightAxis,
      required this.bottomAxis,
      required this.barGroups});

  static BarChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    var leftAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "l" && c.visible);
    var topAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "t" && c.visible);
    var rightAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "r" && c.visible);
    var bottomAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "b" && c.visible);
    return BarChartViewModel(
        control: control,
        leftAxis: leftAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, leftAxisCtrls.first)
            : null,
        topAxis: topAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, topAxisCtrls.first)
            : null,
        rightAxis: rightAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, rightAxisCtrls.first)
            : null,
        bottomAxis: bottomAxisCtrls.isNotEmpty
            ? ChartAxisViewModel.fromStore(store, bottomAxisCtrls.first)
            : null,
        barGroups: children
            .where((c) => c.type == "group" && c.visible)
            .map((c) => BarChartGroupViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props =>
      [control, leftAxis, rightAxis, topAxis, bottomAxis, barGroups];
}

class BarChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const BarChartControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

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
    bool disabled = widget.control.disabled || widget.parentDisabled;

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

          var interactive = viewModel.control.getBool("interactive", true)!;

          List<BarChartGroupData> barGroups = viewModel.barGroups
              .map((g) => getGroupData(
                  Theme.of(context), widget.control, interactive, g))
              .toList();

          var chart = BarChart(
            BarChartData(
              backgroundColor: widget.control.getColor("bgcolor", context),
              minY: widget.control.getDouble("miny"),
              maxY: widget.control.getDouble("maxy"),
              baselineY: widget.control.getDouble("baseliney"),
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
                  "horizontalGridLines", "verticalGridLines"),
              groupsSpace: widget.control.getDouble("groupsSpace"),
              barTouchData: BarTouchData(
                enabled: interactive,
                touchTooltipData: BarTouchTooltipData(
                  getTooltipColor: (BarChartGroupData group) => widget.control
                      .getColor("tooltipBgColor", context,
                          Theme.of(context).colorScheme.secondary)!,
                  tooltipRoundedRadius:
                      widget.control.getDouble("tooltipRoundedRadius"),
                  tooltipMargin: widget.control.getDouble("tooltipMargin"),
                  tooltipPadding:
                      parseEdgeInsets(widget.control, "tooltipPadding"),
                  maxContentWidth: widget.control.getDouble("tooltipMaxWidth"),
                  rotateAngle: widget.control.getDouble("tooltipRotateAngle"),
                  tooltipHorizontalOffset:
                      widget.control.getDouble("tooltipHorizontalOffset"),
                  tooltipBorder: parseBorderSide(
                      Theme.of(context), widget.control, "tooltipBorderSide"),
                  fitInsideHorizontally:
                      widget.control.getBool("tooltipFitInsideHorizontally"),
                  fitInsideVertically:
                      widget.control.getBool("tooltipFitInsideVertically"),
                  direction: parseTooltipDirection(
                      widget.control.getString("tooltipDirection")),
                  getTooltipItem: (group, groupIndex, rod, rodIndex) {
                    var dp = viewModel.barGroups[groupIndex].barRods[rodIndex];

                    var tooltip = dp.control.getString(
                        "tooltip", dp.control.getDouble("toY", 0)!.toString())!;
                    var tooltipStyle = parseTextStyle(
                        Theme.of(context), dp.control, "tooltipStyle");
                    tooltipStyle ??= const TextStyle();
                    if (tooltipStyle.color == null) {
                      tooltipStyle = tooltipStyle.copyWith(
                          color: rod.gradient?.colors.first ??
                              rod.color ??
                              Colors.blueGrey);
                    }
                    TextAlign? tooltipAlign = parseTextAlign(
                        dp.control.getString("tooltipAlign", ""),
                        TextAlign.center)!;
                    return dp.control.getBool("showTooltip", true)!
                        ? BarTooltipItem(tooltip, tooltipStyle,
                            textAlign: tooltipAlign)
                        : null;
                  },
                ),
                touchCallback: widget.control.getBool("onChartEvent", false)!
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
                          widget.backend.triggerControlEvent(widget.control.id,
                              "chart_event", json.encode(eventData));
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
      x: groupViewModel.control.getInt("x", 0)!,
      barsSpace: groupViewModel.control.getDouble("barsSpace"),
      groupVertically: groupViewModel.control.getBool("groupVertically"),
      showingTooltipIndicators: groupViewModel.barRods
          .asMap()
          .entries
          .where((e) =>
              !interactiveChart && e.value.control.getBool("selected", false)!)
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
    var bgFromY = rodViewModel.control.getDouble("bgFromY");
    var bgToY = rodViewModel.control.getDouble("bgToY");
    var bgColor = rodViewModel.control.getColor("bgColor", context);
    var bgGradient = parseGradient(theme, rodViewModel.control, "bgGradient");

    return BarChartRodData(
        fromY: rodViewModel.control.getDouble("fromY"),
        toY: rodViewModel.control.getDouble("toY", 0)!,
        width: rodViewModel.control.getDouble("width"),
        color: rodViewModel.control.getColor("color", context),
        gradient: parseGradient(theme, rodViewModel.control, "gradient"),
        borderRadius: parseBorderRadius(rodViewModel.control, "borderRadius"),
        borderSide:
            parseBorderSide(theme, rodViewModel.control, "borderSide") ??
                BorderSide.none,
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
        stackItemViewModel.control.getDouble("fromY")!,
        stackItemViewModel.control.getDouble("toY", 0)!,
        stackItemViewModel.control.getColor("color", context)!,
        parseBorderSide(theme, stackItemViewModel.control, "borderSide") ??
            BorderSide.none);
  }

  AxisTitles getAxisTitles(
      Control parent, ChartAxisViewModel? axisViewModel, bool disabled) {
    if (axisViewModel == null) {
      return const AxisTitles(sideTitles: SideTitles(showTitles: false));
    }

    return AxisTitles(
        axisNameWidget: axisViewModel.title != null
            ? createControl(parent, axisViewModel.title!.id, disabled)
            : null,
        axisNameSize: axisViewModel.control.getDouble("titleSize") ?? 16,
        sideTitles: SideTitles(
          showTitles: axisViewModel.control.getBool("showLabels", true)!,
          reservedSize: axisViewModel.control.getDouble("labelsSize") ?? 22,
          interval: axisViewModel.control.getDouble("labelsInterval"),
          getTitlesWidget: axisViewModel.labels.isEmpty
              ? defaultGetTitle
              : (value, meta) {
                  return axisViewModel.labels.containsKey(value)
                      ? createControl(
                          parent, axisViewModel.labels[value]!.id, disabled)
                      : const SizedBox.shrink();
                },
        ));
  }
}
