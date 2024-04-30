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
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/numbers.dart';
import '../utils/shadows.dart';
import '../utils/text.dart';
import 'charts.dart';
import 'create_control.dart';

class LineChartDataPointViewModel extends Equatable {
  final Control control;
  final double x;
  final double y;
  final String? tooltip;

  const LineChartDataPointViewModel(
      {required this.control,
      required this.x,
      required this.y,
      required this.tooltip});

  static LineChartDataPointViewModel fromStore(
      Store<AppState> store, Control control) {
    return LineChartDataPointViewModel(
        control: control,
        x: control.attrDouble("x")!,
        y: control.attrDouble("y")!,
        tooltip: control.attrString("tooltip"));
  }

  @override
  List<Object?> get props => [control];
}

class LineChartDataViewModel extends Equatable {
  final Control control;
  final List<LineChartDataPointViewModel> dataPoints;

  const LineChartDataViewModel(
      {required this.control, required this.dataPoints});

  static LineChartDataViewModel fromStore(
      Store<AppState> store, Control control) {
    return LineChartDataViewModel(
        control: control,
        dataPoints: store.state.controls[control.id]!.childIds
            .map((childId) => store.state.controls[childId])
            .whereNotNull()
            .where((c) => c.isVisible)
            .map((c) => LineChartDataPointViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props => [control, dataPoints];
}

class LineChartEventData extends Equatable {
  final String eventType;
  final List<LineChartEventDataSpot> barSpots;

  const LineChartEventData({required this.eventType, required this.barSpots});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'type': eventType,
        'spots': barSpots,
      };

  @override
  List<Object?> get props => [eventType, barSpots];
}

class LineChartEventDataSpot extends Equatable {
  final int barIndex;
  final int spotIndex;

  const LineChartEventDataSpot(
      {required this.barIndex, required this.spotIndex});

  Map<String, dynamic> toJson() => <String, dynamic>{
        'bar_index': barIndex,
        'spot_index': spotIndex,
      };

  @override
  List<Object?> get props => [barIndex, spotIndex];
}

class LineChartViewModel extends Equatable {
  final Control control;
  final ChartAxisViewModel? leftAxis;
  final ChartAxisViewModel? topAxis;
  final ChartAxisViewModel? rightAxis;
  final ChartAxisViewModel? bottomAxis;
  final List<LineChartDataViewModel> dataSeries;

  const LineChartViewModel(
      {required this.control,
      required this.leftAxis,
      required this.topAxis,
      required this.rightAxis,
      required this.bottomAxis,
      required this.dataSeries});

  static LineChartViewModel fromStore(
      Store<AppState> store, Control control, List<Control> children) {
    var leftAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "l" && c.isVisible);
    var topAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "t" && c.isVisible);
    var rightAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "r" && c.isVisible);
    var bottomAxisCtrls =
        children.where((c) => c.type == "axis" && c.name == "b" && c.isVisible);
    return LineChartViewModel(
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
        dataSeries: children
            .where((c) => c.type == "data" && c.isVisible)
            .map((c) => LineChartDataViewModel.fromStore(store, c))
            .toList());
  }

  @override
  List<Object?> get props =>
      [control, leftAxis, rightAxis, topAxis, bottomAxis, dataSeries];
}

class LineChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;
  final FletControlBackend backend;

  const LineChartControl(
      {super.key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled,
      required this.backend});

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl> {
  LineChartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart build: ${widget.control.id}");

    var animate = parseAnimation(widget.control, "animate");
    var border = parseBorder(Theme.of(context), widget.control, "border");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    var result = StoreConnector<AppState, LineChartViewModel>(
        distinct: true,
        converter: (store) => LineChartViewModel.fromStore(
            store, widget.control, widget.children),
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
          var pointLineStart = viewModel.control.attrDouble("pointLineStart");
          var pointLineEnd = viewModel.control.attrDouble("pointLineEnd");

          List<LineChartBarData> barsData = [];
          List<LineBarSpot> selectedPoints = [];

          var barIndex = 0;
          for (var ds in viewModel.dataSeries) {
            var barData =
                getBarData(Theme.of(context), widget.control, interactive, ds);
            barsData.add(barData);

            if (!interactive) {
              var spotIndex = 0;
              for (var p in ds.dataPoints) {
                if (p.control.attrBool("selected", false)!) {
                  selectedPoints.add(
                      LineBarSpot(barData, barIndex, barData.spots[spotIndex]));
                }
                spotIndex++;
              }
            }

            barIndex++;
          }

          var chart = LineChart(
            LineChartData(
                backgroundColor: HexColor.fromString(Theme.of(context),
                    widget.control.attrString("bgcolor", "")!),
                minX: widget.control.attrDouble("minx"),
                maxX: widget.control.attrDouble("maxx"),
                minY: widget.control.attrDouble("miny"),
                maxY: widget.control.attrDouble("maxy"),
                baselineX: widget.control.attrDouble("baselinex"),
                baselineY: widget.control.attrDouble("baseliney"),
                showingTooltipIndicators: groupBy(selectedPoints, (p) => p.x)
                    .values
                    .map((e) => ShowingTooltipIndicators(e))
                    .toList(),
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
                lineBarsData: barsData,
                lineTouchData: LineTouchData(
                  enabled: interactive,
                  getTouchLineStart: pointLineStart != null
                      ? (barData, spotIndex) => pointLineStart
                      : defaultGetTouchLineStart,
                  getTouchLineEnd: pointLineEnd != null
                      ? (barData, spotIndex) => pointLineEnd
                      : defaultGetTouchLineEnd,
                  getTouchedSpotIndicator:
                      (LineChartBarData barData, List<int> spotIndexes) {
                    var barIndex = interactive
                        ? barsData.indexWhere(
                            (b) => b == barData.copyWith(showingIndicators: []))
                        : barsData.indexWhere((b) => b == barData);

                    return spotIndexes.map((index) {
                      if (barIndex == -1) {
                        return null;
                      }

                      FlLine? allDotsLine = parseSelectedFlLine(
                          Theme.of(context),
                          viewModel.dataSeries[barIndex].control,
                          "selectedBelowLine",
                          barData.color,
                          barData.gradient);

                      FlLine? dotLine = parseSelectedFlLine(
                          Theme.of(context),
                          viewModel
                              .dataSeries[barIndex].dataPoints[index].control,
                          "selectedBelowLine",
                          barData.color,
                          barData.gradient);

                      return TouchedSpotIndicatorData(
                        dotLine ??
                            allDotsLine ??
                            FlLine(
                                color: defaultGetPointColor(
                                    barData.color, barData.gradient, 0),
                                strokeWidth: 3),
                        FlDotData(
                          show: true,
                          getDotPainter: (spot, percent, barData, index) {
                            var allDotsPainter = parseChartSelectedDotPainter(
                                Theme.of(context),
                                viewModel.dataSeries[barIndex].control,
                                "selectedPoint",
                                barData.color,
                                barData.gradient,
                                percent);
                            var dotPainter = parseChartSelectedDotPainter(
                                Theme.of(context),
                                viewModel.dataSeries[barIndex].dataPoints[index]
                                    .control,
                                "selectedPoint",
                                barData.color,
                                barData.gradient,
                                percent);
                            return dotPainter ??
                                allDotsPainter ??
                                getDefaultSelectedPainter(
                                    barData.color, barData.gradient, percent);
                          },
                        ),
                      );
                    }).toList();
                  },
                  touchTooltipData: LineTouchTooltipData(
                    tooltipBgColor:
                        widget.control.attrColor("tooltipBgColor", context) ??
                            const Color.fromRGBO(96, 125, 139, 1),
                    getTooltipItems: (touchedSpots) {
                      return touchedSpots.map((spot) {
                        var dp = viewModel.dataSeries[spot.barIndex]
                            .dataPoints[spot.spotIndex];
                        var tooltip = dp.tooltip ?? dp.y.toString();
                        var tooltipStyle = parseTextStyle(
                            Theme.of(context), dp.control, "tooltipStyle");
                        tooltipStyle ??= const TextStyle();
                        if (tooltipStyle.color == null) {
                          tooltipStyle = tooltipStyle.copyWith(
                              color: spot.bar.gradient?.colors.first ??
                                  spot.bar.color ??
                                  Colors.blueGrey);
                        }
                        TextAlign? tooltipAlign = TextAlign.values
                            .firstWhereOrNull((a) =>
                                a.name.toLowerCase() ==
                                dp.control
                                    .attrString("tooltipAlign", "")!
                                    .toLowerCase());
                        return dp.control.attrBool("showTooltip", true)!
                            ? LineTooltipItem(tooltip, tooltipStyle,
                                textAlign: tooltipAlign ?? TextAlign.center)
                            : null;
                      }).toList();
                    },
                  ),
                  touchCallback: widget.control.attrBool("onChartEvent", false)!
                      ? (evt, resp) {
                          var eventData = LineChartEventData(
                              eventType: evt.runtimeType
                                  .toString()
                                  .substring(2), // remove "Fl"
                              barSpots:
                                  resp != null && resp.lineBarSpots != null
                                      ? resp.lineBarSpots!
                                          .map((bs) => LineChartEventDataSpot(
                                              barIndex: bs.barIndex,
                                              spotIndex: bs.spotIndex))
                                          .toList()
                                      : []);
                          if (eventData != _eventData) {
                            _eventData = eventData;
                            debugPrint(
                                "LineChart ${widget.control.id} ${eventData.eventType}");
                            widget.backend.triggerControlEvent(
                                widget.control.id,
                                "chart_event",
                                json.encode(eventData));
                          }
                        }
                      : null,
                )),
            duration: animate != null
                ? animate.duration
                : const Duration(milliseconds: 150), // Optional
            curve: animate != null ? animate.curve : Curves.linear,
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

  LineChartBarData getBarData(ThemeData theme, Control parent,
      bool interactiveChart, LineChartDataViewModel dataViewModel) {
    Color? aboveLineBgcolor =
        dataViewModel.control.attrColor("aboveLineBgcolor", context);
    Gradient? aboveLineGradient =
        parseGradient(theme, dataViewModel.control, "aboveLineGradient");
    Color? belowLineBgcolor =
        dataViewModel.control.attrColor("belowLineBgcolor", context);
    Gradient? belowLineGradient =
        parseGradient(theme, dataViewModel.control, "belowLineGradient");
    var dashPattern = dataViewModel.control.attrString("dashPattern");
    var shadow =
        parseBoxShadow(Theme.of(context), dataViewModel.control, "shadow");
    Color barColor =
        dataViewModel.control.attrColor("color", context) ?? Colors.cyan;
    Gradient? barGradient =
        parseGradient(theme, dataViewModel.control, "gradient");
    FlLine? aboveLine =
        parseFlLine(Theme.of(context), dataViewModel.control, "aboveLine");
    FlLine? belowLine =
        parseFlLine(Theme.of(context), dataViewModel.control, "belowLine");
    double? aboveLineCutoffY =
        dataViewModel.control.attrDouble("aboveLineCutoffY");
    double? belowLineCutoffY =
        dataViewModel.control.attrDouble("belowLineCutoffY");

    Map<FlSpot, LineChartDataPointViewModel> spots = {
      for (var e in dataViewModel.dataPoints) FlSpot(e.x, e.y): e
    };
    return LineChartBarData(
        preventCurveOverShooting:
            dataViewModel.control.attrBool("preventCurveOverShooting", false)!,
        preventCurveOvershootingThreshold: dataViewModel.control
            .attrDouble("preventCurveOverShootingThreshold", 10.0)!,
        spots: dataViewModel.dataPoints.map((p) => FlSpot(p.x, p.y)).toList(),
        showingIndicators: dataViewModel.dataPoints
            .asMap()
            .entries
            .where((e) =>
                !interactiveChart &&
                e.value.control.attrBool("selected", false)!)
            .map((e) => e.key)
            .toList(),
        isCurved: dataViewModel.control.attrBool("curved", false)!,
        isStrokeCapRound:
            dataViewModel.control.attrBool("strokeCapRound", false)!,
        barWidth: dataViewModel.control.attrDouble("strokeWidth") ?? 2.0,
        dashArray: dashPattern != null
            ? (json.decode(dashPattern) as List)
                .map((e) => parseInt(e))
                .toList()
            : null,
        shadow: shadow.isNotEmpty
            ? shadow[0]
            : const Shadow(color: Colors.transparent),
        dotData: FlDotData(
            show: true,
            getDotPainter: (spot, percent, barData, index) {
              var allDotsPainter = parseChartDotPainter(
                  theme,
                  dataViewModel.control,
                  "point",
                  barColor,
                  barGradient,
                  percent);
              var dotPainter = parseChartDotPainter(
                  theme,
                  dataViewModel.dataPoints[index].control,
                  "point",
                  barColor,
                  barGradient,
                  percent);
              return dotPainter ?? allDotsPainter ?? getInvisiblePainter();
            }),
        aboveBarData: aboveLineBgcolor != null ||
                aboveLineGradient != null ||
                aboveLine != null
            ? BarAreaData(
                show: true,
                color: aboveLineBgcolor,
                gradient: aboveLineGradient,
                applyCutOffY: aboveLineCutoffY != null,
                cutOffY: aboveLineCutoffY ?? 0,
                spotsLine: BarAreaSpotsLine(
                  show: aboveLine != null,
                  flLineStyle: aboveLine ?? const FlLine(),
                  checkToShowSpotLine: (spot) =>
                      spots[spot]!.control.attrBool("showAboveLine", true)!,
                ))
            : null,
        belowBarData: belowLineBgcolor != null ||
                belowLineGradient != null ||
                belowLine != null
            ? BarAreaData(
                show: true,
                color: belowLineBgcolor,
                gradient: belowLineGradient,
                applyCutOffY: belowLineCutoffY != null,
                cutOffY: belowLineCutoffY ?? 0,
                spotsLine: BarAreaSpotsLine(
                  show: belowLine != null,
                  flLineStyle: belowLine ?? const FlLine(),
                  checkToShowSpotLine: (spot) =>
                      spots[spot]!.control.attrBool("showBelowLine", true)!,
                ))
            : null,
        color: barColor,
        gradient: barGradient);
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
        axisNameSize: axisViewModel.control.attrDouble("titleSize") ?? 16,
        sideTitles: SideTitles(
          showTitles: axisViewModel.control.attrBool("showLabels", true)!,
          reservedSize: axisViewModel.control.attrDouble("labelsSize") ?? 22,
          interval: axisViewModel.control.attrDouble("labelsInterval"),
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
