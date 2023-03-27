import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:fl_chart/fl_chart.dart';
import 'package:flet/src/models/linechart_data_point_view_model.dart';
import 'package:flutter/material.dart';
import 'package:flutter_redux/flutter_redux.dart';

import '../flet_app_services.dart';
import '../models/app_state.dart';
import '../models/control.dart';
import '../models/linechart_axis_view_model.dart';
import '../models/linechart_data_view_model.dart';
import '../models/linechart_event_data.dart';
import '../models/linechart_view_model.dart';
import '../utils/animations.dart';
import '../utils/borders.dart';
import '../utils/charts.dart';
import '../utils/colors.dart';
import '../utils/gradient.dart';
import '../utils/numbers.dart';
import '../utils/shadows.dart';
import '../utils/text.dart';
import 'create_control.dart';

class LineChartControl extends StatefulWidget {
  final Control? parent;
  final Control control;
  final List<Control> children;
  final bool parentDisabled;

  const LineChartControl(
      {Key? key,
      this.parent,
      required this.control,
      required this.children,
      required this.parentDisabled})
      : super(key: key);

  @override
  State<LineChartControl> createState() => _LineChartControlState();
}

class _LineChartControlState extends State<LineChartControl> {
  LinechartEventData? _eventData;

  @override
  Widget build(BuildContext context) {
    debugPrint("LineChart build: ${widget.control.id}");

    var animate = parseAnimation(widget.control, "animate");
    var border = parseBorder(Theme.of(context), widget.control, "border");
    bool disabled = widget.control.isDisabled || widget.parentDisabled;

    return StoreConnector<AppState, LineChartViewModel>(
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

          List<LineChartBarData> barsData = [];

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

                //showingTooltipIndicators: [ShowingTooltipIndicators([LineBarSpot(bar, barIndex, spot)])],
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
                lineBarsData: viewModel.dataSeries
                    .map(
                        (d) => getBarData(Theme.of(context), widget.control, d))
                    .toList(),
                lineTouchData: LineTouchData(
                  enabled: viewModel.control.attrBool("interactive", true)!,
                  getTouchedSpotIndicator:
                      (LineChartBarData barData, List<int> spotIndexes) {
                    var barIndex = barsData.indexWhere(
                        (b) => b == barData.copyWith(showingIndicators: []));

                    // if (spotIndexes.isNotEmpty) {
                    //   debugPrint(
                    //       "Bar index: $barIndex, spotIndexes.length: ${spotIndexes.length}, spotIndexes: ${spotIndexes[0]}");
                    // }

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
                            var allDotsPainter = parseChartDotPainter(
                                Theme.of(context),
                                viewModel.dataSeries[barIndex].control,
                                "selectedPoint",
                                barData.color,
                                barData.gradient,
                                percent);
                            var dotPainter = parseChartDotPainter(
                                Theme.of(context),
                                viewModel.dataSeries[barIndex].dataPoints[index]
                                    .control,
                                "selectedPoint",
                                barData.color,
                                barData.gradient,
                                percent);
                            return dotPainter ??
                                allDotsPainter ??
                                getInvisiblePainter();
                          },
                        ),
                      );
                    }).toList();
                  },
                  touchTooltipData: LineTouchTooltipData(
                    tooltipBgColor: HexColor.fromString(Theme.of(context),
                        widget.control.attrString("tooltipBgcolor", "")!),
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
                          var eventData = LinechartEventData(
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
                            FletAppServices.of(context).server.sendPageEvent(
                                eventTarget: widget.control.id,
                                eventName: "chart_event",
                                eventData: json.encode(eventData));
                          }
                        }
                      : null,
                )),
            swapAnimationDuration: animate != null
                ? animate.duration
                : const Duration(milliseconds: 150), // Optional
            swapAnimationCurve: animate != null ? animate.curve : Curves.linear,
          );

          barsData = chart.data.lineBarsData;

          return constrainedControl(
              context, chart, widget.parent, widget.control);
        });
  }

  LineChartBarData getBarData(
      ThemeData theme, Control parent, LineChartDataViewModel dataViewModel) {
    Color? aboveLineBgcolor = HexColor.fromString(
        theme, dataViewModel.control.attrString("aboveLineBgcolor", "")!);
    Gradient? aboveLineGradient =
        parseGradient(theme, dataViewModel.control, "aboveLineGradient");
    Color? belowLineBgcolor = HexColor.fromString(
        theme, dataViewModel.control.attrString("belowLineBgcolor", "")!);
    Gradient? belowLineGradient =
        parseGradient(theme, dataViewModel.control, "belowLineGradient");
    var dashPattern = dataViewModel.control.attrString("dashPattern");
    var shadow =
        parseBoxShadow(Theme.of(context), dataViewModel.control, "shadow");
    Color barColor = HexColor.fromString(
            theme, dataViewModel.control.attrString("color", "")!) ??
        Colors.cyan;
    Gradient? barGradient =
        parseGradient(theme, dataViewModel.control, "gradient");
    FlLine? aboveLine =
        parseFlLine(Theme.of(context), dataViewModel.control, "aboveLine");
    FlLine? belowLine =
        parseFlLine(Theme.of(context), dataViewModel.control, "belowLine");

    Map<FlSpot, LineChartDataPointViewModel> spots = {
      for (var e in dataViewModel.dataPoints) FlSpot(e.x, e.y): e
    };
    return LineChartBarData(
        spots: dataViewModel.dataPoints.map((p) => FlSpot(p.x, p.y)).toList(),
        isCurved: dataViewModel.control.attrBool("curved"),
        isStrokeCapRound: dataViewModel.control.attrBool("strokeCapRound"),
        barWidth: dataViewModel.control.attrDouble("strokeWidth"),
        dashArray: dashPattern != null
            ? (json.decode(dashPattern) as List)
                .map((e) => parseInt(e))
                .toList()
            : null,
        shadow: shadow.isNotEmpty ? shadow[0] : null,
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
                spotsLine: BarAreaSpotsLine(
                  show: true,
                  flLineStyle: aboveLine,
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
                spotsLine: BarAreaSpotsLine(
                  show: true,
                  flLineStyle: belowLine,
                  checkToShowSpotLine: (spot) =>
                      spots[spot]!.control.attrBool("showBelowLine", true)!,
                ))
            : null,
        color: barColor,
        gradient: barGradient);
  }

  AxisTitles getAxisTitles(
      Control parent, LineChartAxisViewModel? axisViewModel, bool disabled) {
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
